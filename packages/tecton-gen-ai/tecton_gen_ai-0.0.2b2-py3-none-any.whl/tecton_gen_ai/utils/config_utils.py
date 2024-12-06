from contextlib import contextmanager
from contextvars import ContextVar
from typing import Any, Dict, Iterator

import pandas as pd
from pydantic import BaseModel, Field

from ..constants import DEFAULT_TIMEOUT


class Configs(BaseModel):
    """
    The base configs for the feature view, LLM model, and feature service
    """

    llm: Any = Field(description="The LLM model", default=None)
    default_timeout: str = Field(
        description="The default timeout", default=DEFAULT_TIMEOUT
    )
    fv_base_config: Dict[str, Any] = Field(
        description="The base config for the feature view", default={}
    )
    bfv_config: Dict[str, Any] = Field(
        description="The config for the batch feature view", default={}
    )
    sfv_config: Dict[str, Any] = Field(
        description="The config for the stream feature view", default={}
    )
    rtfv_config: Dict[str, Any] = Field(
        description="The config for the realtime feature view", default={}
    )
    feature_service_config: Dict[str, Any] = Field(
        description="The config for the feature service", default={}
    )

    def update(self, other: "Configs") -> "Configs":
        """
        Update the configs with the other configs

        Args:

            other: The other configs

        Returns:

                The updated configs
        """
        return Configs(
            llm=other.llm or self.llm,
            fv_base_config=self.fv_base_config | other.fv_base_config,
            bfv_config=self.bfv_config | other.bfv_config,
            sfv_config=self.sfv_config | other.sfv_config,
            rtfv_config=self.rtfv_config | other.rtfv_config,
            feature_service_config=self.feature_service_config
            | other.feature_service_config,
        )

    def get_bfv_config(self) -> Dict[str, Any]:
        """
        Get the config for the batch feature view merged with the base config

        Returns:

            The config for the batch feature view
        """
        return self.fv_base_config | self.bfv_config

    def get_rtfv_config(self) -> Dict[str, Any]:
        """
        Get the config for the realtime feature view merged with the base config

        Returns:

            The config for the realtime feature view
        """
        return self.fv_base_config | self.rtfv_config

    def get_sfv_config(self) -> Dict[str, Any]:
        """
        Get the config for the stream feature view merged with the base config

        Returns:

            The config for the stream feature view
        """
        return self.fv_base_config | self.sfv_config

    def get_timeout_sec(self, timeout: Any) -> float:
        """
        Get the timeout in seconds

        Args:

            timeout: The timeout, if None, it will use the default timeout

        Returns:

            The timeout in seconds
        """
        return pd.to_timedelta(timeout or self.default_timeout).total_seconds()

    def set_default(self) -> None:
        """
        Set this config set to be the the default for the feature view,
        LLM model, and feature service

        Examples:

            ```python
            from tecton_gen_ai.api import Configs

            Configs(llm="openai/gpt-4o").set_default()
            ```
        """
        _TECTON_GEN_AI_CONFIG.set(self)

    @contextmanager
    def update_default(self) -> Iterator["Configs"]:
        """
        Update the default configs for the feature view, LLM model, and feature service

        Examples:

            ```python
            from tecton_gen_ai.api import Configs

            Configs(llm="openai/gpt-4o").set_default()

            with Configs(fv_base_config={"name": "my_fv"}).update_default():
                conf = Configs.get_default()
                assert conf.fv_base_config["name"] == "my_fv"
                assert conf.llm == "openai/gpt-4o"

            conf = Configs.get_default()
            assert len(conf.fv_base_config)==0
            ```
        """
        old_config = _TECTON_GEN_AI_CONFIG.get()
        try:
            token = _TECTON_GEN_AI_CONFIG.set(old_config.update(self))
            yield
        finally:
            _TECTON_GEN_AI_CONFIG.reset(token)

    @staticmethod
    def get_default() -> "Configs":
        """
        Get the current default configs for the feature view, LLM model, and feature service

        Returns:

            The default configs

        Examples:

            Examples:

            ```python
            from tecton_gen_ai.api import Configs

            Configs(llm="openai/gpt-4o").set_default()

            with Configs(fv_base_config={"name": "my_fv"}).update_default():
                conf = Configs.get_default()
                assert conf.fv_base_config["name"] == "my_fv"
                assert conf.llm == "openai/gpt-4o"

            conf = Configs.get_default()
            assert len(conf.fv_base_config)==0
            ```
        """
        return _TECTON_GEN_AI_CONFIG.get()


_TECTON_GEN_AI_CONFIG = ContextVar("tecton_gen_ai_config", default=Configs())
