import json
from contextlib import contextmanager
from contextvars import ContextVar
from functools import lru_cache
from typing import Any, Dict

from tecton_gen_ai.constants import _DEV_MODE_AGENT_KEY

_AGENT_CONTEXT = ContextVar("agent_context", default=None)


def get_agent_context() -> Dict[str, Any]:
    return _AGENT_CONTEXT.get() or {}


@contextmanager
def agent_context(context: Dict[str, Any], mode="overwrite"):
    if mode == "overwrite":
        ctx = dict(context)
    elif mode == "update":
        ctx = dict(get_agent_context())
        ctx.update(context)
    else:
        raise ValueError(f"Invalid mode {mode}")
    token = _AGENT_CONTEXT.set(ctx)
    try:
        yield
    finally:
        _AGENT_CONTEXT.reset(token)


def make_agent_client_in_rtfv(service_name, connection_json=None):
    ctx = get_agent_context()
    dev_agent = ctx.get(_DEV_MODE_AGENT_KEY)
    if dev_agent is not None:
        return dev_agent
    else:
        return _make_remote_agent_client_in_rtfv(service_name, connection_json)


@lru_cache
def _make_remote_agent_client_in_rtfv(name, connection_json):
    from tecton_gen_ai.agent.client import get_agent

    address = {} if connection_json is None else json.loads(connection_json)

    return get_agent(
        name=name,
        url=address.get("url"),
        workspace=address.get("workspace"),
        # TODO: When secrets in rtfv is available, we should remove api_key
        api_key=address.get("api_key"),
    )
