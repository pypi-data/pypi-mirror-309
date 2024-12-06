import json
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union  # noqa

import numpy as np
import pandas as pd
from pydantic import BaseModel, Field
from tecton import (
    Attribute,
    FeatureService,
    FeatureView,
    RealtimeFeatureView,
    RequestSource,
    realtime_feature_view,
)
from tecton.types import String

from tecton_gen_ai.constants import _DEV_MODE_AGENT_KEY
from tecton_gen_ai.utils._agent_context import agent_context
from tecton_gen_ai.utils._internal import get_local_source_attrs, is_local_source

from ..constants import _INPUT_JSON_FIELD, _OUTPUT_JSON_FIELD
from ..deco import _get_from_metastore, _get_source_names, prompt, tool
from ..utils._internal import (
    _REQUEST,
    entity_to_pydantic,
    make_request_source,
    set_serialization,
)
from ..utils._serialization import serialize_pydantic, to_openai_function
from ..utils.config_utils import Configs
from ..utils.config_wrapper import to_json_config
from .base import AgentBase, _get_connection_info
from .factory import make_llm

_DEFINED_SERVICES: Dict[str, "Agent"] = {}


def _get_defined_service(name: str) -> "Agent":
    return _DEFINED_SERVICES[name]


class AgentInputModel(BaseModel):
    query: str = Field(description="The query to the agent")
    chat_history: List[Tuple[str, str]] = Field(
        description="The chat history in a list of role message pairs.", default=[]
    )


class Agent(AgentBase):
    """
    The Tecton agent. The instantiated agent can either be deployed to Tecton
    or used locally for testing.

    Args:

        name: The name of the agent
        description: The description of the agent, default to None. The
            description will be required when this agent is used as a tool by
            other agents, and in this case the description is the tool description.
            If the description is provided, it will always be the first part of system
            prompt when this agent instructs its own LLM.
        prompt: the prompt for this agent to instruct its own LLM. It defaults to None.
        tools: A list of tools, agents and features views can be used as tools directly
        knowledge: A list of knowledge bases
        input_schema: The input schema of the agent, default to `str`. The input schema
            must be `str` or a subclass of `AgentInputModel`. The input schema is used to
            validate the input context of the agent. It is required when this agent is used
            as a tool by other agents and its prompt and tools need parameters.
        output_schema: The output schema of the agent, default to `str`. The output schema
            must be `str` or a subclass of pydantic BaseModel. The output schema is used to
            define the structure of the output of the agent. When it is `str` the output
            of the `invoke` method will be a string. When it is a subclass of `BaseModel`,
            the output of the `invoke` method will be a python dict following the schema.
        llm: The language model to use for this agent, default to None. It can be a string, a dict or a
            ConfigWrapper of a LLM object from Langchain or LlamaIndex.
        allow_undefined_context: Whether to allow undefined context keys in the input context.
            It defaults to True. When it is set to False, the input context must have only the keys
            defined in the `input_schema`.
        entrypoint_timeout: The timeout expression for the entrypoint, default to None. The value must be
            acceptable by `pandas.to_timedelta`. If it is None, the default timeout will be used.

    Returns:

        An Agent object

    Note:

        * The system prompt of this agent consists of `description`, `context` and `prompt`.
        * It is a good practice to define the input schema if there are extra parameters to use the agent
        * It is a good practice to set `allow_undefined_context` to False
        * It is a good practice to provide a string expression or a dict as the `llm`

    Example:

        Hello world

        ```python
        from tecton_gen_ai.api import Agent

        agent = Agent(name="hello", llm="openai/gpt-4o-mini")
        agent.invoke("Hello world")
        ```

        With a simple prompt (you don't need the prompt decorator)

        ```python
        from tecton_gen_ai.api import Agent, Configs

        # Set the default language model globally,
        # so you don't need to provide it for each agent
        Configs(llm="openai/gpt-4o-mini").set_default()

        agent = Agent(
            name="hello",
            prompt="You are talking to a 4 years old child",
        )

        agent.invoke("Hello")
        ```

        With simple tools (you don't need the tool decorator)

        ```python
        from tecton_gen_ai.api import Agent

        def get_special_message() -> str:
            return "This is a special message"

        agent = Agent(
            name="hello",
            tools=[get_special_message],
            llm="openai/gpt-4o-mini",
        )

        agent.invoke("What is the special message?")
        ```

        Prompt and tools with parameters

        ```python
        from tecton_gen_ai.api import Agent

        def sys_prompt(age:int) -> str:
            return f"You are talking to a {age} years old child"

        def get_special_message(name:str) -> str:
            '''Get a special message for a person

            Args:

                name (str): The name of the person

            Returns:

                str: The special message for the person
            '''
            return f"Hello {name}, this is magic"

        agent = Agent(
            name="hello",
            prompt=sys_prompt,
            tools=[get_special_message],
            llm="openai/gpt-4o-mini",
        )

        agent.invoke("What is the special message?", context={"name":"Jim", "age":4})

        # notice the parameters of prompts are required, but the parameters of tools are optional
        # so if you don't provide the parameters for the tools, the LLM will generate the parameters
        agent.invoke("My name is Tom, what is the special message?", context={"age":4})

        # If you want to use this agent as a tool by other agents, then you must
        # define `name` and `age` in the input schema, otherwise they will not be passed to the agent
        from pydantic import BaseModel, Field
        from tecton_gen_ai.api import AgentInputModel

        # It must inherit from `AgentInputModel`
        # The field description will be very helpful to describe the agent as a tool
        class Input(AgentInputModel):
            name: str = Field(description="The name of the person")
            age: int = Field(description="The age of the person")

        agent = Agent(
            name="hello",
            prompt=sys_prompt,
            tools=[get_special_message],
            llm="openai/gpt-4o-mini",
            input_schema=Input,
        )

        agent.invoke("What is the special message?", context={"name":"Jim", "age":4})
        ```

        It is always a good practice (no matter if you want to use the agent as a tool)
        to define all parameters required by the prompt and tools in the input schema.

        Use pydantic models to control output schema

        ```python
        from pydantic import BaseModel, Field
        from tecton_gen_ai.api import Agent, AgentInputModel, Configs

        Configs(llm="openai/gpt-4o-mini", default_timeout="20s").set_default()

        class Input(AgentInputModel):
            age: int = Field(description="The age of the person")

        # The output fields should have descriptions
        # The field description will be very helpful to help the agent generate the expected output
        class Output(BaseModel):
            title: str = Field(description="Title of the story")
            story: str = Field(description="The story")

        story_teller = Agent(
            name="story_teller",
            # description is required to describe the agent as a tool
            description="Tell a story for a person given the topic (query)",
            # prompt is to instruct this agent's LLM how to respond
            prompt="You are a story teller",

            output_schema=Output,

            # this enforces the input context to only have the keys in input schema
            # it is optional, but it is recommended to set it to False
            allow_undefined_context=False,
        )

        # the output will be a python dict following the output schema
        story_teller.invoke("Tell me a story")
        ```

        To continue, now let's use agents as tools

        ```python
        # Input must be defined and provided to the agent: poem_writer
        # because `sys_prompt` uses the `age` parameter
        # and the parameter `age` will be a part of the agent as a tool

        class Input(AgentInputModel):
            age: int = Field(description="The age of the person")

        def sys_prompt(age:int) -> str:
            return f"You are talking to a {age} years old child"

        poem_writer = Agent(
            name="song_writer",
            description="Write a poem for a person given a topic (query)",
            prompt=sys_prompt,
            input_schema=Input,
        )

        agent = Agent(
            name="general",
            tools=[story_teller, poem_writer],
        )

        agent.invoke("I am 5 years old, tell me a story and then write a song")
        ```

        Let's build a chatbot helping a student to shop for items.

        ```python
        from tecton_gen_ai.testing import make_local_source, make_local_batch_feature_view, set_dev_mode
        from tecton_gen_ai.testing.utils import make_local_vector_db_config

        set_dev_mode()  # Set the dev mode to avoid tecton login

        student = make_local_batch_feature_view(
            "student",
            {"student_id": 1, "name": "Jim", "teacher": "Mr. Smith", "preference": "fruit"},
            ["student_id"],
            description="Student information including name, teacher and shopping preference",
        )

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
        from tecton_gen_ai.api import prompt, source_as_knowledge

        @prompt(sources=[student])
        def sys_prompt(student) -> str:
            return "You are serving a 4 years old child "+student["name"]

        knowledge = source_as_knowledge(
            src,
            vector_db_config=vdb_conf,
            vectorize_column="description",
            filter = [("zip", str, "the zip code of the item for sale")]
        )

        # Serve the knowledge base
        from tecton_gen_ai.api import Agent

        agent = Agent(
            name="app",
            prompt=sys_prompt,
            tools=[student],  # student is a feature view but can be used as a tool directly
            knowledge=[knowledge],
            llm = {"model": "openai/gpt-4o", "temperature": 0},
        )

        # Test locally
        with agent.set_context({"zip":"98005", "student_id":1}):
            print(agent.invoke("Suggest something for me to buy"))
        with agent.set_context({"zip":"10065", "student_id":1}):
            print(agent.invoke("Suggest something for me to buy"))
        ```
    """

    def __init__(
        self,
        name: str,
        description: Optional[str] = None,
        prompt: Any = None,
        tools: Optional[List[Any]] = None,
        knowledge: Optional[List[Any]] = None,
        input_schema: Union[str, Type[AgentInputModel]] = str,
        output_schema: Union[str, Type[BaseModel]] = str,
        llm: Any = None,
        allow_undefined_context: bool = True,
        entrypoint_timeout: Any = None,
    ):
        super().__init__(name=name)
        self._metastore: Dict[str, Any] = {}

        self.allow_undefined_context = allow_undefined_context
        self.description = description
        self.tools: List[Any] = []
        self.prompts: List[Any] = []
        self._metastore["entrypoint_timeout_sec"] = (
            Configs.get_default().get_timeout_sec(entrypoint_timeout)
        )

        self.knowledge_bfvs: List[FeatureView] = []
        llm = llm or Configs.get_default().llm
        self.llm = None if llm is None else make_llm(llm, conf=True)
        self.input_schema = AgentInputModel if input_schema is str else input_schema
        if not issubclass(self.input_schema, AgentInputModel):
            raise ValueError(
                "input_schema must be str or a subclass of AgentInputModel"
            )
        self.output_schema = output_schema
        if description:
            self._metastore["description"] = description

        if prompt:
            self._add_prompt(prompt)
        if tools:
            for _tool in tools:
                if isinstance(_tool, FeatureView):
                    self._add_fv_tool(fv_as_tool(_tool, queryable=False))
                elif isinstance(_tool, FeatureViewTool):
                    self._add_fv_tool(_tool)
                elif isinstance(_tool, AgentBase):
                    self._add_agent_tool(AgentTool(_tool))
                elif isinstance(_tool, AgentTool):
                    self._add_agent_tool(_tool)
                else:
                    self._add_tool(_tool)
        if knowledge:
            for k in knowledge:
                self._add_knowledge(k)
        self.online_fvs: List[RealtimeFeatureView] = [
            *self.tools,
            *self.prompts,
            self._make_metastore(),
        ]
        self.entrypoint_fv = self._make_entrypoint()
        self._run(name)
        _DEFINED_SERVICES[name] = self

        self.tool_map = {tool.name: tool for tool in self.online_fvs}
        for bfv in self.knowledge_bfvs:
            source = bfv.sources[0]
            if is_local_source(source):
                attrs = get_local_source_attrs(source)
                start = attrs["start_time"]
                end = attrs["end_time"]
                bfv.run_transformation(start, end).to_pandas()
                self.logger.info("Ingested knowledge %s to vector db", bfv.name)

    def _make_entrypoint(self) -> RealtimeFeatureView:
        request = make_request_source(input_json=str)
        # TODO: remove include_api_key when secrets in rtfv is supported
        connection_json = json.dumps(_get_connection_info(include_api_key=True))
        allow_undefined_context = self.allow_undefined_context
        input_plan = serialize_pydantic(self.input_schema)
        output_plan = (
            "str"
            if self.output_schema is str
            else serialize_pydantic(self.output_schema)
        )
        service_name = self.name
        llm_json = None if self.llm is None else to_json_config(self.llm)

        with set_serialization():

            @realtime_feature_view(
                name=self.name,
                sources=[request],
                mode="python",
                features=[Attribute(_OUTPUT_JSON_FIELD, String)],
                **Configs.get_default().get_rtfv_config(),
            )
            def entrypoint(request_context) -> str:
                import json

                try:
                    if llm_json is None:
                        raise ValueError("No language model instance provided")

                    from tecton_gen_ai.utils._agent_context import (
                        make_agent_client_in_rtfv,
                    )
                    from tecton_gen_ai.utils._serialization import deserialize_pydantic
                    from tecton_gen_ai.utils.config_wrapper import from_json_config

                    input_schema = deserialize_pydantic(input_plan)
                    output_schema = (
                        str
                        if output_plan == "str"
                        else deserialize_pydantic(output_plan)
                    )

                    input = json.loads(request_context[_INPUT_JSON_FIELD])
                    if not allow_undefined_context:
                        old = input
                        input = input_schema.model_validate(old).model_dump()
                        extra = set(old.keys()) - set(input.keys())
                        if len(extra) > 0:
                            raise ValueError(
                                f"Undefined context is not allowed: {extra}"
                            )

                    client = make_agent_client_in_rtfv(
                        service_name=service_name, connection_json=connection_json
                    )
                    query = input.pop("query")
                    chat_history = input.pop("chat_history", [])
                    local_llm = from_json_config(llm_json)
                    res = client.invoke_locally(
                        query,
                        chat_history=chat_history,
                        context=input,
                        output_schema=output_schema,
                        local_llm=local_llm,
                    )
                    response = {
                        "result": res if isinstance(res, (str, dict)) else res.dict()
                    }
                except Exception:
                    import traceback

                    error = traceback.format_exc()

                    response = {"error": error}
                return {_OUTPUT_JSON_FIELD: json.dumps(response)}

            return entrypoint

    def _add_tool(self, func: Any) -> None:
        meta = dict(_get_from_metastore(func, lambda: tool(func)))
        if meta.get("type") != "tool":
            raise ValueError(f"Function {func} is not a tool")
        name = meta.pop("name")
        self.tools.append(meta.pop("fv"))
        if "tools" not in self._metastore:
            self._metastore["tools"] = {}
        self._metastore["tools"][name] = meta

    def _add_fv_tool(self, fvt: "FeatureViewTool") -> None:
        if "tools" not in self._metastore:
            self._metastore["tools"] = {}
        self._metastore["tools"][fvt.fv.name] = fvt.make_metadata()
        self.tools.append(fvt.make_rtfv())

    def _add_agent_tool(self, at: "AgentTool") -> None:
        if "tools" not in self._metastore:
            self._metastore["tools"] = {}
        self._metastore["tools"][at.agent.name] = at.make_metadata()

    def _add_prompt(self, func: Any) -> None:
        with set_serialization():
            if isinstance(func, str):
                message = func

                @prompt
                def system_prompt() -> str:
                    return message

                func = system_prompt
            meta = dict(_get_from_metastore(func, lambda: prompt(func)))
            if meta.get("type") != "prompt":
                raise ValueError(f"Function {func} is not a prompt")
            self.prompts.append(meta.pop("fv"))
            self._metastore["prompt"] = meta

    def _add_knowledge(self, funcs: Any) -> None:
        self.knowledge_bfvs.append(funcs[0])
        self._add_tool(funcs[1])

    def _make_metastore(self) -> FeatureView:
        _metastore = self.metastore
        name = self.name + "_metastore"

        with set_serialization():

            @realtime_feature_view(
                name=name,
                sources=[_REQUEST],
                mode="python",
                features=[Attribute(_OUTPUT_JSON_FIELD, String)],
                **Configs.get_default().get_rtfv_config(),
            )
            def metastore(request_context):
                import json

                from tecton_gen_ai.constants import _OUTPUT_JSON_FIELD

                return {_OUTPUT_JSON_FIELD: json.dumps({"result": _metastore})}

            return metastore

    def _run(self, name: str) -> List[FeatureService]:
        kwargs = Configs.get_default().feature_service_config
        fs = [
            FeatureService(
                name=name + "_" + tool.name,
                features=[tool],
                **kwargs,
            )
            for tool in self.online_fvs
        ]
        for fv in self.knowledge_bfvs:
            fs.append(
                FeatureService(
                    name=name + "_" + fv.name,
                    **kwargs,
                    features=[fv],
                    online_serving_enabled=False,
                )
            )
        fs.append(FeatureService(name=name, **kwargs, features=[self.entrypoint_fv]))
        return fs

    @property
    def metastore(self) -> Dict[str, Any]:
        return self._metastore

    def _invoke_entrypoint(
        self,
        message: str,
        timeout_sec: float,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None,
    ) -> Any:
        agent = self if agent_name is None else _get_defined_service(agent_name)
        with agent_context({_DEV_MODE_AGENT_KEY: agent}):
            req = {
                "query": message,
                "chat_history": (
                    [list(pair) for pair in chat_history]
                    if chat_history is not None
                    else []
                ),
            }
            if context is not None:
                req.update(context)
            output_df = self.entrypoint_fv.get_features_for_events(
                pd.DataFrame([{_INPUT_JSON_FIELD: json.dumps(req)}])
            ).to_pandas()
            resp = json.loads(output_df[self.name + "__" + _OUTPUT_JSON_FIELD].iloc[0])
            if "error" in resp:
                raise Exception(resp["error"])
            return resp["result"]

    def _get_feature_value(
        self,
        name: str,
        key_map: Dict[str, Any],
        request_map: Dict[str, Any],
        feature_type: str,
        timeout_sec: float,
    ):
        fv = self.tool_map[name]
        res = dict(key_map)
        now = datetime.now()
        for source in fv.sources:
            if not isinstance(source, RequestSource):
                src = source.feature_definition
                res[src.get_timestamp_field()] = now
        if feature_type == "prompt":
            res.update(request_map)
            if len(res) == 0:
                res["dummy"] = 0
            output_df = fv.get_prompts_for_events(pd.DataFrame([res])).to_pandas()
            return output_df[name + "__prompt"].iloc[0]
        else:
            res.update(
                {
                    "name": name,
                    "input": json.dumps(request_map),
                }
            )
            output_df = fv.get_features_for_events(pd.DataFrame([res])).to_pandas()
            resp = json.loads(output_df[name + "__" + _OUTPUT_JSON_FIELD].iloc[0])
            if "error" in resp:
                raise Exception(resp["error"])
            result = resp["result"]
            return result


def fv_as_tool(
    fv: FeatureView,
    queryable: bool,
    description: Optional[str] = None,
    timeout: Any = None,
) -> "FeatureViewTool":
    """Convert a feature view to a tool

    Args:

        fv: The feature view
        queryable: Whether the tool is queryable using its entity ids
        description: The description of the tool, default to None. If provided,
            it will be used as the description of the tool
        timeout: The timeout expression for the tool, default to None. The value must be
            acceptable by `pandas.to_timedelta`. If it is None, the default timeout will be used.

    Returns:

        A FeatureViewTool object
    """
    return FeatureViewTool(fv, queryable, description=description, timeout=timeout)


class FeatureViewTool:
    def __init__(
        self,
        fv: FeatureView,
        queryable: bool,
        description: Optional[str] = None,
        timeout: Any = None,
    ):
        if not isinstance(fv, FeatureView):
            raise ValueError(f"Expected FeatureView, got {type(fv)}")
        if not hasattr(fv, "entities") or len(fv.entities) != 1:
            raise ValueError(f"FeatureView {fv} must have exactly one entity")
        self.description = description or fv.description
        if not self.description:
            raise ValueError(
                f"FeatureView {fv} must have a description or you "
                "should provide the description from `fv_as_tool`"
            )

        self.fv = fv
        self.queryable = queryable
        self.tool_name = "fv_tool_" + fv.name
        self.timeout = timeout

    def make_metadata(self):
        fv = self.fv
        # notice transformation_schema doesn't consider aggregation, so this is not the final schema
        # gettting entity schema from it is fine
        model = entity_to_pydantic(fv.entities[0], fv.transformation_schema())
        func = to_openai_function(
            model, name=self.tool_name, description=self.description
        )
        args = list(model.model_fields.keys())
        return {
            "name": self.tool_name,
            "type": "tool",
            "subtype": "fv",
            "queryable": self.queryable,
            "args": args,
            "function": func,
            "source_names": _get_source_names([fv]),
            "timeout_sec": Configs.get_default().get_timeout_sec(self.timeout),
        }

    def make_rtfv(self) -> RealtimeFeatureView:
        fv = self.fv
        tool_name = self.tool_name
        with set_serialization():

            @realtime_feature_view(
                name=tool_name,
                sources=[_REQUEST, fv],
                mode="python",
                features=[Attribute(_OUTPUT_JSON_FIELD, String)],
                **Configs.get_default().get_rtfv_config(),
            )
            def fv_tool(request_context, _fv) -> str:
                import json

                from tecton_gen_ai.constants import _OUTPUT_JSON_FIELD

                if tool_name != request_context["name"]:
                    return {_OUTPUT_JSON_FIELD: "{}"}
                res = _transform_group_result(_fv)
                return {_OUTPUT_JSON_FIELD: json.dumps({"result": res})}

            return fv_tool


class AgentTool:
    def __init__(self, agent: AgentBase):
        if not isinstance(agent, Agent):
            raise ValueError("You can only use a locally defined agent")
        if agent.description is None or agent.description == "":
            raise ValueError("Agent must have a description")
        self.agent = agent
        self.tool_name = "agent_tool_" + agent.name

    def make_metadata(self):
        func = to_openai_function(
            self.agent.input_schema,
            name=self.agent.name,
            description=self.agent.description,
            exclude_args=["chat_history"],
        )
        return {
            "name": self.tool_name,
            "type": "tool",
            "subtype": "agent",
            "agent_name": self.agent.name,
            "function": func,
            "timeout_sec": self.agent.entrypoint_timeout_sec,
        }


def _transform_group_result(fv: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Transform the group result to a list of dictionaries

    Args:

        fv: a dict of single value or arrays

    Returns:

        List[Dict[str, Any]]: a list of dictionaries
    """
    cols: List[List[Any]] = [
        v.tolist() for v in fv.values() if isinstance(v, np.ndarray)
    ]
    if len(cols) == 0:
        return fv
    elif len(cols) < len(fv):
        raise ValueError("All columns must be numpy arrays or none")
    blobs = []
    keys = list(fv.keys())
    step = len(fv) // 2
    for i in range(step):
        key_name = keys[i].rsplit("_keys_", 1)[0]
        val_name = keys[i + step]
        blob = [{key_name: x, val_name: y} for x, y in zip(cols[i], cols[i + step])]
        blobs.extend(blob)
    return blobs
