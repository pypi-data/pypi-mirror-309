from datetime import datetime, timedelta
from typing import Any, Dict, List, Optional, Union

from pydantic import BaseModel, Field
from tecton import Attribute, DataSource, Entity, batch_feature_view
from tecton.framework.data_source import FilteredSource

from .utils import _schema_utils, structured_outputs
from .utils._internal import assert_param_not_null_or_get_from_mock, set_serialization


class LlmExtractionConfig(BaseModel):
    column: str
    output_schema: type[BaseModel] = Field(alias="schema")
    model: Optional[str] = None
    local_concurrency: int = 5


def llm_extraction(
    source: Union[DataSource, FilteredSource],
    extraction_config: List[Union[LlmExtractionConfig, Dict[str, Any]]],
    feature_start_time: Optional[datetime] = None,
    batch_schedule: timedelta = timedelta(days=1),
    timestamp_field: Optional[str] = None,
    name: Optional[str] = None,
    description: Optional[str] = None,
    entities: Optional[List[Entity]] = None,
    offline: bool = False,
    online: bool = False,
    secrets: Optional[Dict[str, Any]] = None,
    default_model: Optional[str] = None,
    **fv_kwargs: Any,
) -> Any:
    """
    Run LLM Feature Extraction on a Tecton data source and output to a batch feature view.
    This function will create an ingestion pipeline to call LLM transformations
    to extract structured data from a text column according to the provided schema.

    Args:

        source: The data source
        extraction_config: The LLM extraction configuration
        feature_start_time: The feature start time, defaults to None.
            When None, it requires the source to be a mock source created for testing purpose.
        batch_schedule: The batch schedule, defaults to timedelta(days=1)
        timestamp_field: The timestamp field, defaults to None.
            When None, it requires the source to be a mock source created for testing purpose.
        name: The name of the knowledge base, defaults to None.
            When None, it will use the name of the source.
        description: The description of the knowledge base, defaults to None.
            When None, it will use the description of the source.
        secrets: The configured secrets
        default_model: The default model to use for extraction.
        fv_kwargs: Additional kwargs to pass to the batch feature view decorator

    Returns: The batch feature view containing the output

    """

    # TODO: refactor this configuration resolution to be shared with
    # logic for `source_as_knowledge`
    feature_start_time = assert_param_not_null_or_get_from_mock(
        feature_start_time, source, "start_time"
    )
    timestamp_field = assert_param_not_null_or_get_from_mock(
        timestamp_field, source, "timestamp_field"
    )
    if name is None:
        if isinstance(source, FilteredSource):
            name = source.source.name
        else:
            name = source.name
    if name is None or name == "":
        raise ValueError("name is required")
    if description is None:
        if isinstance(source, FilteredSource):
            description = source.source.description
        else:
            description = source.description

    if len(extraction_config) == 0:
        raise ValueError("extraction_config is required")
    if len(extraction_config) > 1:
        raise ValueError("extraction_config must be length 1")

    extraction_config_objs = [
        (
            config
            if isinstance(config, LlmExtractionConfig)
            else LlmExtractionConfig.parse_obj(config)
        )
        for config in extraction_config
    ]

    for config in extraction_config_objs:
        if config.model is None:
            if default_model:
                config.model = default_model
            else:
                raise ValueError(
                    "Please set `default_model` in llm_extraction, or `model` in the extraction config"
                )

    schema = structured_outputs.StructuredOutputSchema.from_pydantic(
        extraction_config_objs[0].output_schema
    )

    tecton_fields = _schema_utils.get_tecton_fields_from_json_schema(schema.json_schema)
    features = [
        Attribute(name=field.name, dtype=field.dtype) for field in tecton_fields
    ]

    entities = entities or schema.get_tecton_entities()

    config = (
        extraction_config_objs[0].model,
        extraction_config_objs[0].column,
        extraction_config_objs[0].local_concurrency,
        schema.model_dump_json(),
    )

    kwargs = dict(
        name=name + "_batch",
        sources=[source],
        entities=entities,
        mode="pandas",
        offline=offline,
        online=online,
        features=features,
        feature_start_time=feature_start_time,
        batch_schedule=batch_schedule,
        timestamp_field=timestamp_field,
        description=description,
        secrets=secrets,
    )
    kwargs.update(fv_kwargs)
    batch_deco = batch_feature_view(**kwargs)

    def extract(bs, context):
        import os

        import pandas as pd

        if "openai_api_key" in context.secrets:
            os.environ["OPENAI_API_KEY"] = context.secrets["openai_api_key"]

        model, column, local_concurrency, serialized_schema = config

        schema = structured_outputs.StructuredOutputSchema.parse_raw(serialized_schema)

        extraction_out = structured_outputs.batch_generate_dicts(
            model,
            bs[column],
            schema,
            concurrency=local_concurrency,
        )
        extraction_df = pd.DataFrame(extraction_out, index=bs.index)
        out_df = pd.concat([bs.drop(columns=column), extraction_df], axis=1)
        return out_df

    with set_serialization():

        def extract_0(bs, context):
            return extract(bs, context)

        batch_fv = batch_deco(extract_0)

    return batch_fv
