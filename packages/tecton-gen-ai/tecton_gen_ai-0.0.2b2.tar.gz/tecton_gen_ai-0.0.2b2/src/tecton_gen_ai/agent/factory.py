from tecton_gen_ai.utils.config_wrapper import ConfigWrapper


from functools import singledispatch
from typing import Any


def _load_dependencies():
    try:
        from tecton_gen_ai.integrations import langchain  # noqa
    except ImportError:
        pass

    try:
        from tecton_gen_ai.integrations import llama_index  # noqa
    except ImportError:
        pass


@singledispatch
def make_llm_model(obj: Any) -> Any:
    """
    Make a LLM object. This is not for users to call directly.

    Args:

        obj: The object
    """
    if isinstance(obj, ConfigWrapper):
        return make_llm_model(obj.instantiate())
    if isinstance(obj, str):
        return make_llm_model({"model": obj})
    raise NotImplementedError(f"Unsupported type {type(obj)}")  # pragma: no cover


@singledispatch
def make_llm_model_conf(obj: Any) -> ConfigWrapper:
    """
    Make a config wrapper of a LLM object. This is not for users to call directly.

    Args:

        obj: The object
    """
    if isinstance(obj, ConfigWrapper):
        return obj
    if isinstance(obj, str):
        return make_llm_model_conf({"model": obj})
    raise NotImplementedError(f"Unsupported type {type(obj)}")  # pragma: no cover


def make_llm(obj: Any, conf: bool) -> Any:
    """
    Make a LLM object or the config wrapper. This is not for users to call directly.

    Args:

        obj: The object
        conf: whether to make a config wrapper
    """
    _load_dependencies()
    if conf:
        return make_llm_model_conf(obj)
    return make_llm_model(obj)
