import asyncio
import hashlib
import json
from typing import Any, TypeVar, Union

import instructor
import openai
from openai.types.chat import ChatCompletion
from pydantic import BaseModel

from . import _cache, _coroutine, _schema_utils

T_OutputType = TypeVar("T_OutputType", bound=BaseModel)


class StructuredOutputSchema(BaseModel):
    json_schema: dict[str, Any]
    instructor_kwargs: dict[str, Any]

    @classmethod
    def from_pydantic(cls, model_cls: type[BaseModel]):
        schema_dict = json.loads(model_cls.schema_json())
        _, kwargs = instructor.process_response.handle_response_model(model_cls)
        return cls(json_schema=schema_dict, instructor_kwargs=kwargs)


def generate(model: str, text: str, schema: type[T_OutputType]) -> T_OutputType:
    if model.startswith("openai/"):
        openai_model = model[len("openai/") :]
        return _generate_openai(openai_model, text, schema)
    raise ValueError(f"Model {model} not supported")


def generate_dict(model: str, text: str, schema: StructuredOutputSchema) -> dict:
    if model.startswith("openai/"):
        openai_model = model[len("openai/") :]
        return _generate_openai_dict(openai_model, text, schema)
    raise ValueError(f"Model {model} not supported")


def _generate_openai_dict(openai_model: str, text: str, schema: StructuredOutputSchema):
    client = instructor.from_openai(openai.OpenAI())
    out = client.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "user", "content": text},
        ],
        response_model=None,
        **schema.instructor_kwargs,
    )
    return _parse_tools(schema, out)


def _parse_tools(
    schema: StructuredOutputSchema,
    completion: ChatCompletion,
):
    message = completion.choices[0].message

    if hasattr(message, "refusal") and message.refusal is not None:
        raise ValueError(f"Unable to generate a response due to {message.refusal}")
    if len(message.tool_calls or []) != 1:
        raise ValueError(
            "Tecton does not support multiple tool calls, use list[Model] instead"
        )

    tool_call = message.tool_calls[0]
    if tool_call.function.name != schema.json_schema["title"]:
        raise ValueError("Tool name does not match")

    return _schema_utils.load_to_rich_dict(
        tool_call.function.arguments, schema.json_schema
    )


def _generate_openai(openai_model: str, text: str, schema: type[T_OutputType]):
    client = instructor.from_openai(openai.OpenAI())
    out = client.chat.completions.create(
        model=openai_model,
        messages=[
            {"role": "user", "content": text},
        ],
        response_model=schema,
    )
    return out


def batch_generate(
    model: str,
    texts: list[str],
    schema: type[T_OutputType],
    concurrency: int = 5,
) -> list[T_OutputType]:
    if model.startswith("openai/"):
        openai_model = model[len("openai/") :]
        return _batch_generate_openai(
            openai_model, texts, schema, concurrency=concurrency
        )
    raise ValueError(f"Model {model} not supported")


def batch_generate_dicts(
    model: str, texts: list[str], schema: StructuredOutputSchema, concurrency: int = 5
) -> list[dict]:
    if model.startswith("openai/"):
        openai_model = model[len("openai/") :]
        return _batch_generate_dicts_openai(
            openai_model, texts, schema, concurrency=concurrency
        )
    raise ValueError(f"Model {model} not supported")


def _batch_generate_dicts_openai(
    openai_model: str,
    texts: list[str],
    schema: StructuredOutputSchema,
    concurrency: int = 5,
) -> list[dict]:
    cache = _cache.get_cache("tecton-gen-ai", "structured_outputs")

    async def fn(sem, async_client, text: str) -> T_OutputType:
        async with sem:
            key = _cache_key(text, schema)
            if (cached := await cache.aget(key)) is not None:
                return cached

            response = await async_client.chat.completions.create(
                model=openai_model,
                messages=[
                    {"role": "user", "content": text},
                ],
                response_model=None,
                **schema.instructor_kwargs,
            )
            result = _parse_tools(schema, response)

            await cache.aset(key, result)
            return result

    async def _gather():
        sem = asyncio.Semaphore(concurrency)
        async_client = instructor.from_openai(openai.AsyncOpenAI())
        _jobs = [fn(sem, async_client, text) for text in texts]
        return await asyncio.gather(*_jobs)

    return _coroutine.run(_gather())


def _cache_key(text: str, schema: Union[StructuredOutputSchema, type[T_OutputType]]):
    text_hash = hashlib.sha1(text.encode("utf-8")).hexdigest()
    if isinstance(schema, StructuredOutputSchema):
        schema_hash = hashlib.sha1(schema.model_dump_json().encode("utf-8")).hexdigest()
    else:
        schema_hash = hashlib.sha1(schema.schema_json().encode("utf-8")).hexdigest()
    return f"{text_hash}_{schema_hash}"


def _batch_generate_openai(
    openai_model: str,
    texts: list[str],
    schema: type[T_OutputType],
    concurrency: int = 5,
) -> list[T_OutputType]:
    # NOTE: default size limit of 1GB (https://grantjenks.com/docs/diskcache/api.html#constants)
    cache = _cache.get_cache("tecton-gen-ai", "structured_outputs")

    async def fn(sem, async_client, text: str) -> T_OutputType:
        async with sem:
            key = _cache_key(text, schema)
            if (cached := await cache.aget(key)) is not None:
                # Deserialize from JSON based on the return type
                return schema.model_validate_json(cached)

            result = await async_client.chat.completions.create(
                model=openai_model,
                messages=[
                    {"role": "user", "content": text},
                ],
                response_model=schema,
            )

            serialized_result = result.model_dump_json()
            await cache.aset(key, serialized_result)
            return result

    async def _gather():
        sem = asyncio.Semaphore(concurrency)
        async_client = instructor.from_openai(openai.AsyncOpenAI())
        _jobs = [fn(sem, async_client, text) for text in texts]
        return await asyncio.gather(*_jobs)

    return _coroutine.run(_gather())
