from functools import singledispatch
from logging import Logger
from typing import Any, List, Type, Union, Dict, Tuple

from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain.chains.base import Chain
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.documents import Document
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, BaseMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.vectorstores import VectorStore
from pydantic import BaseModel

from ..agent.factory import make_llm_model, make_llm_model_conf

from ..agent.base import (
    AgentBase,
    _IntegratedAgent,
    invoke_agent,
    make_agent,
)
from ..utils.config_wrapper import as_config


@make_llm_model.register(BaseChatModel)
def make_langchain_model(obj: BaseChatModel) -> BaseChatModel:
    return obj


@make_llm_model.register(dict)
def make_langchain_model_from_dict(model_conf: dict) -> BaseChatModel:
    model, conf = _parse_dict(model_conf)
    return model(**conf)


@make_llm_model_conf.register(dict)
def make_langchain_model_conf_from_dict(model_conf: dict) -> dict:
    model, conf = _parse_dict(model_conf)
    return as_config(model)(**conf)


def _parse_dict(data: Dict[str, Any]) -> Tuple[Type[BaseChatModel], Dict]:
    conf = dict(data)
    parts = conf.pop("model").split("/", 1)
    provider, model_name = parts[0], parts[1]
    conf["model"] = model_name
    if provider == "openai":
        from langchain_openai import ChatOpenAI

        return ChatOpenAI, conf
    raise NotImplementedError(f"{provider} not supported")


@invoke_agent.register(BaseChatModel)
def _invoke_langchain(
    llm: BaseChatModel,
    client: AgentBase,
    message: str,
    chat_history: Any = None,
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    **kwargs: Any,
) -> Any:
    callbacks = list(kwargs.pop("callbacks", []))
    cb = _ExecutionCallback(client.logger, client)
    callbacks.append(cb)
    executor = make_langchain_agent_executor(llm, client, output_schema, **kwargs)
    client.logger.debug(
        "Invoking LangChain agent with message: %s, chat_history: %s",
        message,
        chat_history,
    )
    input = {"input": message}
    if chat_history:
        input["chat_history"] = chat_history
    return executor.invoke(input, {"callbacks": callbacks})


@make_agent.register(BaseChatModel)
def make_langchain_agent_executor(
    llm: BaseChatModel,
    client: AgentBase,
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    **executor_kwargs: Any,
) -> Chain:
    agent = _LangChainAgent(client, llm)
    return agent.make_executor(output_schema=output_schema, **executor_kwargs)


@singledispatch
def unified_langchain_vector_search(
    vdb: VectorStore, query: str, top_k: int, **params: Any
) -> List[Document]:
    return vdb.similarity_search(query, top_k, **params)


def langchain_vector_search(
    vdb: VectorStore, query: str, top_k: int, **params: Any
) -> List[Document]:
    try:
        from .lancedb import _lancedb_vector_search  # noqa
    except ImportError:
        pass

    return unified_langchain_vector_search(vdb, query, top_k, **params)


class _LangChainAgent(_IntegratedAgent):
    def make_executor(self, output_schema: Any, **kwargs: Any) -> Chain:
        templates = [
            MessagesPlaceholder("system_prompt"),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", "{input}"),
        ]
        if len(self.tools) > 0:
            templates.append(MessagesPlaceholder("agent_scratchpad"))
        prompt = ChatPromptTemplate.from_messages(templates)
        prompt = prompt.partial(
            system_prompt=lambda: [("system", self.client.invoke_system_prompt())]
        )
        if len(self.tools) > 0:
            agent = create_tool_calling_agent(self.llm, self.tools, prompt)

            def parse(message: Dict[str, Any]) -> Any:
                input = message["input"]
                output = message["output"]
                if isinstance(output, list):
                    output = output[0]["text"]
                if issubclass(output_schema, BaseModel):
                    from langchain_core.utils.function_calling import (
                        convert_pydantic_to_openai_function,
                    )

                    js = convert_pydantic_to_openai_function(output_schema)
                    llm = self.llm.with_structured_output(js)
                    res = llm.invoke(
                        [
                            ("user", input),
                            ("assistant", output),
                            ("user", "convert the response to json"),
                        ]
                    )
                    return res
                else:
                    return output

            return AgentExecutor(agent=agent, tools=self.tools, **kwargs) | parse
        else:
            if issubclass(output_schema, BaseModel):
                llm = self.llm.with_structured_output(output_schema)

                return prompt | llm

            def parse(message: AIMessage) -> str:
                return message.content

            return prompt | self.llm | parse

    def _make_messages(self, question, history):
        history = history or []
        history = self._add_sys_prompt(history)
        return history + [("human", question)]

    def _make_tool(self, name):
        from langchain_core.tools import StructuredTool

        model = self._get_tool_schema(name)

        def f(**kwargs):
            pass

        _tool = StructuredTool.from_function(
            name=name,
            func=f,
            args_schema=model,
            infer_schema=False,
            description=model.__doc__,
        )
        _tool.func = lambda **kwargs: self.client.invoke_tool(name, kwargs)
        return _tool


class _ExecutionCallback(BaseCallbackHandler):
    def __init__(self, logger: Logger, client: AgentBase):
        self.metastore = client.metastore
        self.logger = logger

    def on_chat_model_start(
        self, serialized: Dict[str, Any], messages: List[List[BaseMessage]], **kwargs
    ) -> None:
        self.logger.debug("Chat model started", extra={"flow_event": {"type": "llm"}})

    def on_tool_start(
        self, serialized: Dict[str, Any], input_str: str, **kwargs: Any
    ) -> Any:
        name = serialized.get("name")
        extra = {"flow_event": {"type": "tool", "value": name}}
        tool = self.metastore.get("tools", {}).get(name, {})
        if tool.get("subtype") == "search":
            extra["flow_event"]["knowledge"] = tool.get("source_names", [])
        else:
            extra["flow_event"]["features"] = tool.get("source_names", [])
        self.logger.debug(f"Tool {name} started", extra=extra)
