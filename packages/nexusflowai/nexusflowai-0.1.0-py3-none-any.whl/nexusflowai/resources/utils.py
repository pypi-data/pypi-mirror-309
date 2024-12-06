from __future__ import annotations

from typing import Any, Callable, Dict, List, Union

from logging import ERROR, getLogger

from asyncio import run
from tqdm.asyncio import tqdm

from pydantic import BaseModel

from openai._types import NOT_GIVEN, NotGiven
from openai.types import CompletionCreateParams
from openai.types.chat.completion_create_params import (
    CompletionCreateParams as ChatCompletionCreateParams,
)

from nexusflowai.types import (
    NexusflowAICompletion,
    NexusflowAIChatCompletion,
    NexusflowAIChatCompletionChunk,
)


def maybe_print_hints(
    res: NexusflowAIChatCompletion | NexusflowAIChatCompletionChunk,
) -> None:
    hints = res.hints or []
    if hints:
        print("\n".join(hints))


def maybe_parse_into_pydantic(
    response_format: Union[BaseModel, Dict[str, Any], NotGiven],
    parsed: Dict[str, Any] | None,
) -> None:
    if response_format is NOT_GIVEN or parsed is None:
        return parsed

    is_pydantic = isinstance(response_format, type) and issubclass(
        response_format, BaseModel
    )
    if not is_pydantic:
        return parsed

    return response_format.model_validate(parsed)


def batch_call(
    caller: Callable,
    batch: List[CompletionCreateParams, ChatCompletionCreateParams],
) -> List[Union[NexusflowAICompletion, NexusflowAIChatCompletion | Exception]]:
    assert not any(
        params.get("stream", False) for params in batch
    ), "Batch create does not support streaming requests!"

    async def create_with_except(**params):
        try:
            return await caller(**params)
        except Exception as e:  # pylint: disable=broad-exception-caught
            # We can handle basic exceptions
            if len(e.args) == 1:
                print(f"{type(e).__name__}: {e.args[0]}")
            else:
                raise e
            return e

    async def gather_responses():
        return await tqdm.gather(*(create_with_except(**params) for params in batch))

    # Set the log level higher to avoid so many prints
    logger_names = ["openai._base_client", "httpx"]
    loggers = list(map(getLogger, logger_names))
    original_log_levels = [l.level for l in loggers]
    for l in loggers:
        l.setLevel(ERROR)

    res = run(gather_responses())

    for l, original_log_level in zip(loggers, original_log_levels):
        l.setLevel(original_log_level)

    return res
