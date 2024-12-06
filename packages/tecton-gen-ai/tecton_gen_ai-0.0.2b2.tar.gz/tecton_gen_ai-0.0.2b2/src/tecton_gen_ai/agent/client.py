import json
from functools import lru_cache
from time import time

# for executing function declarations
from typing import Any, Dict, List, Optional, Tuple, Union  # noqa

import pandas as pd
from httpx import Client as HttpClient

from ..constants import _INPUT_JSON_FIELD, _OUTPUT_JSON_FIELD
from .base import AgentBase, _get_connection_info


@lru_cache
def _get_tecton_client(
    url: Any, api_key: Any, workspace: Any, timeout_sec: float
) -> Any:
    from tecton_client import TectonClient

    http_client = HttpClient(timeout=timeout_sec)
    return TectonClient(
        url=url, api_key=api_key, default_workspace_name=workspace, client=http_client
    )


def get_agent(
    name: str,
    url: Optional[str] = None,
    workspace: Optional[str] = None,
    api_key: Optional[str] = None,
    metastore_update_interval: Any = "60s",
) -> AgentBase:
    """
    Create a client connecting to a deployed agent service.

    Args:

        name: The agent name
        url: The Tecton URL, defaults to None (will use the default tecton url from the environment)
        workspace: The workspace name, defaults to None (will use the environment variable TECTON_WORKSPACE)
        api_key: The API key defaults to None (will use the environment variable TECTON_API_KEY)
        metastore_update_interval: The interval expression to update the metastore, defaults to "60s"

    Returns:

        Agent: The client agent
    """
    return _AgentClientRemote(
        name=name,
        url=url,
        workspace=workspace,
        api_key=api_key,
        metastore_update_interval=metastore_update_interval,
    )


class _AgentClientRemote(AgentBase):
    def __init__(
        self,
        name: str,
        url: Optional[str] = None,
        workspace: Optional[str] = None,
        api_key: Optional[str] = None,
        metastore_update_interval: Any = "60s",
    ):
        super().__init__(name=name)

        self.address = _get_connection_info(
            url=url,
            workspace=workspace,
            api_key=api_key,
            service=name,
            include_api_key=True,
        )
        self.interval = pd.to_timedelta(metastore_update_interval).total_seconds()
        self.last_check = 0
        self._static_metastore = None

    @property
    def metastore(self) -> Dict[str, Any]:
        current = time()
        if self._static_metastore is None or current - self.last_check > self.interval:
            self._static_metastore = self._invoke(
                self.name + "_metastore",
                [],
                [],
                {},
                feature_type="metastore",
                timeout_sec=5,
            )
            self.last_check = current
        return self._static_metastore

    def _get_tecton_client(self, timeout_sec: float) -> Any:
        return _get_tecton_client(
            url=self.address["url"],
            api_key=self.address["api_key"],
            workspace=self.address["workspace"],
            timeout_sec=timeout_sec,
        )

    def _invoke_entrypoint(
        self,
        message: str,
        timeout_sec: float,
        chat_history: Optional[List[Tuple[str, str]]] = None,
        context: Optional[Dict[str, Any]] = None,
        agent_name: Optional[str] = None,
    ) -> Union[str, Dict[str, Any]]:
        target_name = agent_name or self.name
        ctx = {
            "query": message,
            "chat_history": [list(x) for x in (chat_history or [])],
        }
        if context:
            ctx.update(context)
        input_json = json.dumps(ctx)
        client = self._get_tecton_client(timeout_sec=timeout_sec)
        gf = client.get_features(
            feature_service_name=target_name,
            request_context_map={_INPUT_JSON_FIELD: input_json},
        )
        fd = gf.get_features_dict()
        key = target_name + "." + _OUTPUT_JSON_FIELD
        resp = json.loads(fd[key])
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
        if feature_type == "prompt":
            request_context_map = {
                "name": name,
                **request_map,
            }
        else:
            request_context_map = {
                "name": name,
                "input": json.dumps(request_map),
            }
        client = self._get_tecton_client(timeout_sec=timeout_sec)
        gf = client.get_features(
            feature_service_name=self.name + "_" + name,
            join_key_map=key_map,
            request_context_map=request_context_map,
        )
        fd = gf.get_features_dict()
        if feature_type == "prompt":
            return fd[name + ".prompt"]
        else:
            resp = json.loads(fd[name + "." + _OUTPUT_JSON_FIELD])
            if "error" in resp:
                raise Exception(resp["error"])
            result = resp["result"]
            return result
