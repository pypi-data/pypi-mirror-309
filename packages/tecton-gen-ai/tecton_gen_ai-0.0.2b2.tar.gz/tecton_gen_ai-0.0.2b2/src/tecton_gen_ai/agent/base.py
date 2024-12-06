import json
import logging
import os
from contextlib import contextmanager
from contextvars import ContextVar
from functools import singledispatch
from typing import Any, Dict, List, Optional, Tuple, Type, Union

import pandas as pd
from pydantic import BaseModel

from tecton_gen_ai.agent.factory import _load_dependencies, make_llm

from ..utils._serialization import openai_function_to_pydantic
from ..utils.log import NOOP_LOGGER

_DEFAULT_TOP_K = 5
_SEARCH_TOOL_PREFIX = "search_"


@singledispatch
def invoke_agent(
    llm,
    client: "AgentBase",
    message: str,
    chat_history: Any = None,
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    **kwargs: Any,
) -> Any:
    """
    Invoke an agent. This is not for users to call directly.

    Args:

        llm: The language model object in a specific framework (e.g. LangChain)
        client: The agent client
        message: The message (question)
        chat_history: The chat history
        output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
        **kwargs: Additional arguments for the agent

    Returns:

        Any: The response in the format of `output_schema`
    """
    raise NotImplementedError(f"Unsupported type {type(llm)}")  # pragma: no cover


@singledispatch
def make_agent(
    llm,
    client: "AgentBase",
    output_schema: Union[Type[str], Type[BaseModel]] = str,
    **kwargs: Any,
) -> Any:
    """
    Make an agent. This is not for users to call directly.

    Args:

        llm: The language model object in a specific framework (e.g. LangChain)
        client: The agent client
        output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
        **kwargs: Additional arguments for creating the agent

    Returns:

        Any: The agent object
    """
    raise NotImplementedError(f"Unsupported type {type(llm)}")  # pragma: no cover


class AgentBase:
    """
    The Tecton Agent. This class should not be used directly. Use `Agent` if
    you want to declare the agent or develop the agent locally. Use `get_agent`
    if you want to connect to a deployed agent.
    """

    def __init__(self, name: str):
        self.name = name
        self._current_context = ContextVar("current_context", default=None)
        self._current_logger = ContextVar("current_logger", default=NOOP_LOGGER)
        self.default_system_prompt: Optional[str] = None

    @property
    def logger(self) -> logging.Logger:
        """
        Get the current logger of the client. The logger can be controlled
        using the context manager `set_logger`.

        Returns:

            logging.Logger: The logger
        """
        return self._current_logger.get()

    @contextmanager
    def set_logger(self, logger: Optional[logging.Logger]):
        """
        Set the logger for the client. This is a context manager.

        Args:

            logger: The new logger, or None to use the no-op logger

        Example:

            ```python
            with client.set_logger(logger):
                # do something
            ```
        """
        _logger = logger or NOOP_LOGGER
        token = self._current_logger.set(_logger)
        try:
            yield
        finally:
            self._current_logger.reset(token)

    @contextmanager
    def set_context(self, context: Optional[Dict[str, Any]]):
        """
        Set the context for the client. This is a context manager. The context
        will be used as the arguments for the prompts, tools and knowledge.

        Args:

            context: The new context, or None to clear the context

        Example:

            ```python
            conext = {"a":1, "b":2}
            new_args = {"b":3, "c":4}
            with client.set_context(context):
                # the context will be used as the arguments of my_tool
                # new_args will override the context
                # the final arguments for my_tool will be {"a":1, "b":3, "c":4}
                client.invoke_tool("my_tool", new_args)
            ```

        """
        self.logger.debug("Setting context to %s", context)
        token = self._current_context.set(context or {})
        try:
            yield
        finally:
            self._current_context.reset(token)

    @property
    def metastore(self) -> Dict[str, Any]:
        """
        Get the metastore of the client. The metastore contains the metadata of
        the tools, prompts, knowledge and other resources. This function should
        not be used directly.
        """
        raise NotImplementedError

    @property
    def entrypoint_timeout_sec(self) -> float:
        """
        Get the request timeout in seconds for the entrypoint. This is used for the entrypoint
        of the agent.
        """
        return self.metastore["entrypoint_timeout_sec"]

    def make_local_agent(
        self,
        llm: Any,
        output_schema: Union[Type[str], Type[BaseModel]] = str,
        **kwargs: Any,
    ) -> Any:
        """
        Make an agent for a specific LLM framework (Langchain or LLamaIndex). This
        agent will run the workflow locally using the local `llm`, but its prompt
        and tools may be from the service.

        Args:

            llm: The language model object in a specific framework (e.g. LangChain or LLamaIndex).
            output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
            **kwargs: Additional arguments for creating the agent

        Returns:

            Any: The agent object

        Example:

            ```python
            from tecton_gen_ai.api import Agent
            from tecton_gen_ai.utils.tecton_utils import make_request_source

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            service = Agent(name="app", prompt=sys_prompt)

            agent = service.make_local_agent({"model":"openai/gpt-4o", "temperature":0})
            with client.set_context({"age": 3}):
                print(agent.invoke({"input":"why sky is blue"}))
            with client.set_context({"age": 30}):
                print(agent.invoke({"input":"why sky is blue"}))
            ```
        """
        llm = make_llm(llm, conf=False)
        if llm is None:
            raise ValueError("No LLM provided")
        _load_dependencies()
        return make_agent(
            llm,
            self,
            output_schema=output_schema,
            **kwargs,
        )

    def invoke(
        self,
        message: str,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        timeout: Any = None,
    ) -> Union[str, Dict[str, Any]]:
        """
        Invoke an agent. When developing the agent locally, this
        will use the LLM and output schema defined by `Agent`. When connecting to
        a deployed agent, this will use the agent's entrypoint.

        Args:

            message: The message (question)
            chat_history: The chat history in the format of [(role, message)], defaults to None
            context: The context variables to run the agent, this will override the context set by `set_context`
            timeout: The timeout expression, if None, it will use the entrypoint's timeout setting

        Returns:

            Union[str, Dict[str, Any]]: The response which can be a string or a python dict.

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt, llm="openai/gpt-4o", entrypoint_timeout=10)

            with agent.set_context({"age": 3}):
                print(agent.invoke("why sky is blue"))

            print(agent.invoke("why sky is blue", context={"age": 30}))

            # With structured output
            from pydantic import BaseModel, Field

            class Response(BaseModel):
                answer: str = Field(description="The answer to the question")

            agent = Agent(
                name="app",
                prompt=sys_prompt,
                llm="openai/gpt-4o",
                output_schema=Response
            )

            # The response will be a python dict {"answer": "..."}
            # It also overwrites the entrypoint's timeout
            agent.invoke("why sky is blue", context={"age": 30}, timeout="10s")
            ```

        """
        if timeout is None:
            timeout_sec = self.entrypoint_timeout_sec
        else:
            timeout_sec = pd.to_timedelta(timeout).total_seconds()
        return self._invoke_entrypoint(
            message=message,
            chat_history=chat_history,
            context=context,
            timeout_sec=timeout_sec,
        )

    def invoke_locally(
        self,
        message: str,
        local_llm: Any,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        output_schema: Union[Type[str], Type[BaseModel]] = str,
        **kwargs: Any,
    ) -> Union[str, Dict[str, Any]]:
        """
        Invoke an agent for a specific LLM framework. Compared to `make_local_agent`, this
        function is simpler, but it is less flexible than getting the agent object of the
        specific framework to invoke.

        Args:

            message: The message (question)
            local_llm: The language model object in a specific framework (e.g. LangChain or LLamaIndex).
                It will invoke the agent locally using the local LLM with the remote prompt and tools.
            chat_history: The chat history in the format of [(role, message)], defaults to None
            context: The context variables to run the agent, this will override the context set by `set_context`
            output_schema: The output schema, can be `str` or a pydantic model, defaults to `str`
            **kwargs: Additional arguments for invoking the agent

        Returns:

            The response, it is a string if `output_schema` is `str`, otherwise it is a python dict
            following the pydantic model.

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt)

            with agent.set_context({"age": 3}):
                print(agent.invoke_locally("why sky is blue", llm="openai/gpt-4o"))

            # With structured output
            from pydantic import BaseModel, Field

            class Response(BaseModel):
                answer: str = Field(description="The answer to the question")

            # The response will be a python dict {"answer": "..."}
            agent.invoke_locally("why sky is blue", llm="openai/gpt-4o", output_schema=Response)
            ```

        """
        _load_dependencies()
        local_llm = make_llm(local_llm, conf=False)
        func = lambda: invoke_agent(  # noqa
            local_llm,
            self,
            message=message,
            chat_history=chat_history,
            output_schema=output_schema,
            **kwargs,
        )

        if context is not None:
            with self.set_context(context):
                res = func()
        else:
            res = func()
        self.logger.debug("Result of invoking agent: %s", res)
        return res

    def _invoke_entrypoint(
        self,
        message: str,
        timeout_sec: float,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None,
    ) -> Union[str, Dict[str, Any]]:
        raise NotImplementedError

    def invoke_tool(self, name: str, kwargs: Optional[Dict[str, Any]] = None) -> Any:
        """
        Invoke a tool in the service.

        Args:

            name: The name of the tool
            kwargs: The arguments for the tool

        Returns:

            Any: The result of the tool

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def get_price_of_fruit(fruit:str) -> int:
                '''
                Get the price of a fruit

                Args:

                    fruit: The name of the fruit

                Returns:

                    int: The price of the fruit
                '''
                return 10 if fruit == "apple" else 5

            agent = Agent(name="app", tools=[get_price_of_fruit])

            print(atent.invoke_tool("get_price_of_fruit", {"fruit":"apple"}))
            ```
        """
        kwargs = kwargs or {}
        self.logger.debug("Invoking tool %s with %s", name, kwargs)
        meta = self.metastore["tools"][name]
        if meta["subtype"] == "fv":
            return self.invoke_feature_view(name, kwargs)
        ctx = self._get_context()
        ctx.update(kwargs)
        if meta["subtype"] == "agent":
            query = ctx.pop("query", None)
            ctx.pop("chat_history", None)  # chat_history is not used in agent as tool
            return self._invoke_entrypoint(
                query,
                context=ctx,
                agent_name=meta["agent_name"],
                timeout_sec=meta["timeout_sec"],
            )
        if meta["subtype"] == "search":
            _filters = json.loads(kwargs.pop("filter", None) or "{}")
            _fctx = self._get_context()
            _fctx.update(_filters)
            kwargs["filter"] = json.dumps(_fctx)
        entity_args = meta.get("entity_args", [])
        llm_args = meta.get("llm_args", [])
        return self._invoke(
            name,
            entity_args,
            llm_args,
            ctx,
            feature_type="tool",
            timeout_sec=meta["timeout_sec"],
        )

    def invoke_feature_view(
        self, name: str, kwargs: Optional[Dict[str, Any]] = None
    ) -> Any:
        """
        Invoke a feature view in the service.

        Args:

            name: The name of the feature view
            kwargs: The arguments for the feature view, the keys should match the entity
                schema of the feature view.

        Returns:

            Any: The result of the feature view

        Example:

            ```python
            from tecton_gen_ai.testing import make_local_feature_view, set_dev_mode

            set_dev_mode()

            bfv = make_local_feature_view(
                "user_age",
                {"user_id": 1, "age": 30},
                ["user_id"],
                description="The age of a user",
            )

            from tecton_gen_ai.api import Agent
            agent = Agent(name="app", tools=[bfv])

            print(agent.invoke_feature_view("user_age", {"user_id":1}))
            ```

        """
        kwargs = kwargs or {}
        self.logger.debug("Invoking feature view as tool %s with %s", name, kwargs)
        tool_name = "fv_tool_" + name
        tool = self.metastore["tools"][name]

        ctx = self._get_context()
        ctx.update(kwargs)
        key_map = {k: ctx[k] for k in tool["args"]}

        return self._get_feature_value(
            tool_name, key_map, {}, feature_type="tool", timeout_sec=tool["timeout_sec"]
        )

    def invoke_prompt(self, kwargs: Optional[Dict[str, Any]] = None) -> str:
        """
        Invoke the prompt of the agent.

        Args:

            kwargs: The arguments for the prompt, it overrides the context set by `set_context`

        Returns:

            str: The result of the prompt

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt)

            print(agent.invoke_prompt({"age": 3}))
            ```
        """
        context = self._get_context()
        context.update(kwargs or {})
        metadata = self._get_sys_prompt()
        if metadata is None:
            return ""
        name = metadata["name"]
        match = all(key in context for key in metadata.get("keys", [])) and all(
            key in context for key in metadata.get("args", [])
        )
        if not match:
            raise ValueError(
                f"Context does not have all required keys for system prompt {name}."
            )
        entity_args = metadata.get("entity_args", [])
        llm_args = metadata.get("llm_args", [])
        self.logger.debug(
            "Invoking prompt %s with %s",
            name,
            context,
            extra={"flow_event": metadata},
        )
        return self._invoke(
            name,
            entity_args,
            llm_args,
            context,
            feature_type="prompt",
            timeout_sec=metadata["timeout_sec"],
        )

    def invoke_system_prompt(self, kwargs: Optional[Dict[str, Any]] = None) -> str:
        """
        Combine agent description, context variables and the prompt of the agent.

        Args:

            kwargs: The arguments for the prompt, it overrides the context set by `set_context`

        Returns:

            str: The result of the prompt

        Example:

            ```python
            from tecton_gen_ai.api import Agent

            def sys_prompt(age:int):
                return f"You are talking to a {age} years old person."

            agent = Agent(name="app", prompt=sys_prompt)

            print(agent.invoke_system_prompt({"age": 3}))
            ```
        """
        lines: List[str] = []
        context = self._get_context()
        context.update(kwargs or {})
        description = self.metastore.get("description", "").strip()
        if description != "":
            lines.append(f"Agent Description: {description}")
        if len(context) > 0:
            lines.append(f"All context for the conversation: {context}")
        lines.append(self.invoke_prompt(kwargs=kwargs))
        return "\n\n".join(lines)

    def search(
        self,
        name: str,
        query: str,
        top_k: int = _DEFAULT_TOP_K,
        filter: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """
        Search a tool in the service.

        Args:

            name: The name of the search tool
            query: The query string
            top_k: The number of results to return, defaults to 5
            filter: The filter for the search, default to None (no filter)

        Returns:

            List[Dict[str, Any]]: The search results

        Example:

            ```python
            from tecton_gen_ai.testing import make_local_source
            from tecton_gen_ai.testing.utils import make_local_vector_db_config

            df = [
                {"zip":"98005", "item_id":1, "description":"pencil"},
                {"zip":"98005", "item_id":2, "description":"car"},
                {"zip":"98005", "item_id":3, "description":"paper"},
                {"zip":"10065", "item_id":4, "description":"boat"},
                {"zip":"10065", "item_id":5, "description":"cheese"},
                {"zip":"10065", "item_id":6, "description":"apple"},
            ]

            src = make_local_source(
                "for_sale",
                df,
                description="Items information",  # required for source_as_knowledge
            )
            vdb_conf = make_local_vector_db_config()

            # Create a knowledge base from the source
            from tecton_gen_ai.api import source_as_knowledge

            knowledge = source_as_knowledge(
                src,
                vector_db_config=vdb_conf,
                vectorize_column="description",
                filter = [("zip", str, "the zip code of the item for sale")]
            )

            # Serve the knowledge base
            from tecton_gen_ai.api import Agent

            service = Agent(name="app", knowledge=[knowledge])

            # Test locally

            # search without filter
            print(agent.search("for_sale", query="fruit"))
            # search with filter
            print(agent.search("for_sale", query="fruit", top_k=3, filter={"zip": "27001"}))
            print(agent.search("for_sale", query="fruit", top_k=3, filter={"zip": "10065"}))
            ```
        """
        self.logger.debug("Searching %s with query %s filter %s", name, query, filter)
        if query == "":
            return []
        return self.invoke_tool(
            _SEARCH_TOOL_PREFIX + name,
            dict(query=query, top_k=top_k, filter=json.dumps(filter or {})),
        )

    def _invoke(
        self,
        name: str,
        entity_args: List[str],
        llm_args: List[str],
        kwargs: Dict[str, Any],
        feature_type: str,
        timeout_sec: float,
    ):
        ctx_map = {}
        key_map = {}
        for k, v in kwargs.items():
            if k in entity_args:
                key_map[k] = v
            # elif k not in llm_args:
            #    raise ValueError(f"Unknown argument {k}")
            if k in llm_args:
                ctx_map[k] = v

        result = self._get_feature_value(
            name, key_map, ctx_map, feature_type=feature_type, timeout_sec=timeout_sec
        )
        self.logger.debug("Result of %s: %s", name, result)
        return result

    def _get_context(self) -> Dict[str, Any]:
        return (self._current_context.get() or {}).copy()

    def _get_feature_value(
        self,
        name: str,
        key_map: Dict[str, Any],
        request_map: Dict[str, Any],
        feature_type: str,
        timeout_sec: float,
    ):
        raise NotImplementedError

    def _get_sys_prompt(self) -> Optional[Dict[str, Any]]:
        return self.metastore.get("prompt")


class _IntegratedAgent:
    def __init__(self, client: AgentBase, llm) -> None:
        self.client = client
        self.llm = llm
        self.tools = self._make_tools()

    def invoke(self, question, history=None, context=None, kwargs=None) -> str:
        raise NotImplementedError  # pragma: no cover

    def _add_sys_prompt(self, history):
        sys_prompt = ("system", self.client.invoke_system_prompt())
        history.insert(0, sys_prompt)
        return history

    def _get_tool_schema(self, name) -> BaseModel:
        meta = self.client.metastore["tools"][name]
        return openai_function_to_pydantic(meta["function"])

    def _make_tool(self, name):
        raise NotImplementedError

    def _make_tools(self):
        return [
            self._make_tool(name)
            for name, value in self.client.metastore.get("tools", {}).items()
            if value["type"] == "tool"
        ]


def _get_connection_info(
    url: Optional[str] = None,
    workspace: Optional[str] = None,
    service: Optional[str] = None,
    api_key: Optional[str] = None,
    include_api_key: bool = True,
) -> Dict[str, Any]:
    from tecton import conf

    if url is None:
        url = conf.tecton_url()
    if workspace is None:
        workspace = conf.get_or_raise("TECTON_WORKSPACE")

    if (
        api_key is None
        and include_api_key
        and os.environ.get("TECTON_GEN_AI_DEV_MODE") != "true"
    ):
        api_key = conf.get_or_raise("TECTON_API_KEY")

    res = {"url": url, "workspace": workspace}
    if include_api_key:
        res["api_key"] = api_key
    if service is not None:
        res["service"] = service
    return res
