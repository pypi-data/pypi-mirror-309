from typing import Any, Callable, Dict, List, Optional, TypeVar

from tecton import FeatureView, RequestSource
from typing_extensions import ParamSpec

from .utils._serialization import to_openai_function

from .utils._internal import FuncWrapper
from .utils.config_utils import Configs

_METASTORE: Dict[str, Any] = {}

T = TypeVar("T")
P = ParamSpec("P")


def _get_from_metastore(obj: Any, register: Any = None) -> Dict[str, Any]:
    key = id(obj)
    if key not in _METASTORE:
        if register is not None:
            register()
            return _get_from_metastore(obj)
        raise ValueError(
            f"{obj} not found in metastore, did you forget to decorate it?"
        )
    return _METASTORE[key]


def _set_metastore(key: Any, value: Any) -> None:
    _METASTORE[id(key)] = value


def _get_source_names(sources: Optional[List[FeatureView]]) -> List[str]:
    if sources is None:
        return []
    return [source.name for source in sources if not isinstance(source, RequestSource)]


def prompt(
    func: Optional[Callable[P, T]] = None,
    name: Optional[str] = None,
    sources: Optional[List[FeatureView]] = None,
    timeout: Any = None,
    **prompt_kwargs: Any,
) -> Callable[P, T]:
    """
    Decorator for creating a prompt.

    Args:

        func: The function to decorate.
        name: The name of the prompt.
        sources: The sources of the prompt.
        timeout: The timeout expression of the tool, defaults to None (use the default timeout).
            The expression must be accepted by `pandas.to_timedelta`.
        **prompt_kwargs: Other keyword arguments for Tecton's prompt.

    Examples:

        ```python
        # You don't need to use the decorator if you don't need to change any parameter

        def simple_prompt() -> str:
            return "Hello, world!"

        # With parameters but not a feature

        def prompt_with_params(zip:str) -> str:
            return "Hello, you zip code " + zip

        # When you need to customize the properties of the prompt
        from tecton_gen_ai.api import prompt

        @prompt(name="simple_prompt_2", timeout="10s")
        def simple_prompt() -> str:
            return "Hello, world!"

        # With a feature dependency
        from tecton_gen_ai.testing import make_local_batch_feature_view

        my_bfv = make_local_batch_feature_view(
            "my_data",
            {"user_id":"u1", "name":"Bob"},
            ["user_id"],
            description="User information",
        )

        @prompt(sources=[my_bfv])
        def sys_prompt(zip:str, my_data) -> str:  # the parameter name of the bfv must match the name of the bfv
            return "Hello, " + my_data["name"] + " with zip code " + zip

        # Serve the prompt
        from tecton_gen_ai.api import Agent

        agent = Agent(
            name="my_service",
            prompt=sys_prompt,
        )

        # Test locally
        with agent.set_context({"zip": "10065", "user_id": "u1"}):
            res = agent.invoke_prompt()
        ```
    """

    def wrapper(
        _func: Callable[P, T],
        _name: Optional[str],
        _features: Optional[List[FeatureView]],
    ) -> Callable[P, T]:
        if _name is None:
            _name = _func.__name__
        wrapper = FuncWrapper(_name, _func, _features)
        fv = wrapper.make_prompt(**prompt_kwargs)
        _set_metastore(
            _func,
            {
                "name": _name,
                "fv": fv,
                "type": "prompt",
                "llm_args": wrapper.llm_args,
                "entity_args": wrapper.entity_args,
                "feature_args": wrapper.feature_args,
                "source_names": _get_source_names(_features),
                "timeout_sec": Configs.get_default().get_timeout_sec(timeout),
            },
        )
        return _func

    if func is None:
        return lambda _func: wrapper(_func, name, sources)
    return wrapper(func, name, sources)


def tool(
    func: Optional[Callable[P, T]] = None,
    name: Optional[str] = None,
    sources: Optional[List[FeatureView]] = None,
    description: Optional[str] = None,
    timeout: Any = None,
    **rtfv_kwargs: Any,
) -> Callable[P, T]:
    """
    Decorator for creating a tool. The tool can be used by different LLMs and
    frameworks such as Langchain and LlamaIndex.

    Args:

        func: The function to decorate.
        name: The name of the tool.
        sources: The sources of the tool.
        description: The description of the tool, defaults to None (the docstring of the function).
        timeout: The timeout expression of the tool, defaults to None (use the default timeout).
            The expression must be acceptable by `pandas.to_timedelta`.
        **rtfv_kwargs: Other keyword arguments for Tecton's realtime feature view.

    Note:

        The definition of tool is different from prompt:

        - The name of the tool should represent what the function does.
        - The docstring of the tool is required and it should contain the description and instructions of the tool.
        - If a feature view is a dependency, then the entity ids must be defined in the function signature.
        - All the arguments excluding feature view arguments must have type annotations.
        - The return type annotation is required.

    Examples:

        ```python
        # In many cases you don't need to use the decorator, `@tool` can be omitted
        def get_months_in_a_year() -> int:
            '''The total number months of a year'''
            return 12

        # With parameters but not a feature
        def add(a: int, b: int) -> int:
            '''Add two numbers

            Args:
                a (int): The first number
                b (int): The second number

            Returns:
                int: The sum of the two numbers
            '''
            return a + b

        # Serve the tool
        from tecton_gen_ai.api import Agent

        agent = Agent(name="my_service", tools=[get_months_in_a_year, add])
        agent.invoke_tool("get_months_in_a_year")
        agent.invoke_tool("add", dict(a=1, b=2))

        # With a feature dependency
        from tecton_gen_ai.api import tool
        from tecton_gen_ai.testing import make_local_batch_feature_view

        my_bfv = make_local_batch_feature_view(
            "my_bfv",
            {"user_id":"u1", "name":"Bob"},
            ["user_id"],
            description="User information",
        )

        @tool(sources=[my_bfv], timeout="10s")
        def get_name(prefix:str, user_id:str, my_bfv) -> str:
            '''Get the name of a user with a prefix

            Args:

                prefix (str): The prefix of the name
                user_id (str): The user ID

            Returns:

                str: The name of the user with the prefix
            '''
            return prefix + " " + my_bfv["name"]

        # Serve the tool
        from tecton_gen_ai.api import Agent

        agent = Agent(name="my_service", tools=[get_name])

        with agent.set_context({"user_id": "u1", "prefix": "Hello"}):
            res = agent.invoke_tool("get_name")
        ```
    """

    return _internal_tool(
        func=func,
        name=name,
        sources=sources,
        description=description,
        subtype="tool",
        timeout=timeout,
        **rtfv_kwargs,
    )


def _internal_tool(
    func: Optional[Callable[P, T]] = None,
    name: Optional[str] = None,
    sources: Optional[List[FeatureView]] = None,
    description: Optional[str] = None,
    subtype: str = "tool",
    source_names: Optional[List[str]] = None,
    extra_metadata: Optional[Dict[str, Any]] = None,
    extra_exluded_args: Optional[List[str]] = None,
    update_params: Any = None,
    timeout: Any = None,
    **rtfv_kwargs: Any,
) -> Callable[P, T]:
    def wrapper(
        _func: Callable[P, T],
        _name: Optional[str],
        _features: Optional[List[FeatureView]],
    ) -> Callable[P, T]:
        if _name is None:
            _name = _func.__name__
        wrapper = FuncWrapper(
            _name,
            _func,
            _features,
            assert_entity_defined=True,
        )
        fv = wrapper.make_feature_view(update_params=update_params, **rtfv_kwargs)
        excluded_args = wrapper.feature_args
        if extra_exluded_args is not None:
            excluded_args += extra_exluded_args
        metadata = {
            "name": _name,
            "fv": fv,
            "type": "tool",
            "subtype": subtype,
            "llm_args": wrapper.llm_args,
            "entity_args": wrapper.entity_args,
            "feature_args": wrapper.feature_args,
            "function": to_openai_function(
                _func,
                name=_name,
                exclude_args=excluded_args,
                description=description or _func.__doc__,
            ),
            "source_names": source_names or _get_source_names(_features),
            "timeout_sec": Configs.get_default().get_timeout_sec(timeout),
        }
        if extra_metadata is not None:
            metadata.update(extra_metadata)
        _set_metastore(_func, metadata)
        return _func

    if func is None:
        return lambda _func: wrapper(_func, name, sources)
    return wrapper(func, name, sources)
