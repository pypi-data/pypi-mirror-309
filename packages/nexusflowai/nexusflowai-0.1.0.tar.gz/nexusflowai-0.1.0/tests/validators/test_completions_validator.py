from openai.types.chat.completion_create_params import CompletionCreateParams
from openai._utils import maybe_transform
from openai._types import NOT_GIVEN

from nexusflowai.validators.base_input_validator import (
    MAX_STOP_SEQUENCES,
    BOT_END,
)
from nexusflowai.validators import CompletionsInputValidator
from pytest import raises


class TestCompletionsValidator:
    def test_validate(self) -> None:
        base_request_body = maybe_transform(
            {
                "prompt": "Weather in Paris?",
                "model": "gpt-4",
                "best_of": NOT_GIVEN,
                "echo": NOT_GIVEN,
                "temperature": NOT_GIVEN,
                "frequency_penalty": 0,
                "logit_bias": None,
                "max_tokens": 150,
                "n": NOT_GIVEN,
                "presence_penalty": 0,
                "response_format": NOT_GIVEN,
                "seed": 42,
                "stop": NOT_GIVEN,
                "stream": NOT_GIVEN,
                "suffix": NOT_GIVEN,
                "top_p": 1,
                "user": "user_123456",
                "logprobs": NOT_GIVEN,
            },
            CompletionCreateParams,
        )

        # Test stream true
        base_request_body["stream"] = True
        CompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["stream"] = NOT_GIVEN

        # Test n
        validated_rb = CompletionsInputValidator(
            request_body=base_request_body
        ).validate()

        assert validated_rb["temperature"] == 0.0
        assert validated_rb["n"] == 1
        base_request_body["n"] = 2
        with raises(
            NotImplementedError,
            match="The only supported value for the n parameter is 1",
        ):
            CompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["n"] = NOT_GIVEN

        # Test stop tokens
        validated_rb = CompletionsInputValidator(
            request_body=base_request_body
        ).validate()

        assert validated_rb["stop"] == [BOT_END]

        base_request_body["stop"] = ["foo", "bar"]

        validated_rb = CompletionsInputValidator(
            request_body=base_request_body
        ).validate()

        assert validated_rb["stop"] == ["foo", "bar", BOT_END]

        base_request_body["stop"] = ["foo", "bar", "boo", "far"]

        with raises(
            ValueError,
            match=f"A maximum of {MAX_STOP_SEQUENCES} stop sequences can be used, and one of them should be {BOT_END}",
        ):
            CompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["stop"] = ["foo", "bar", "boo", "far", BOT_END]

        with raises(
            ValueError,
            match=f"A maximum of {MAX_STOP_SEQUENCES} stop sequences can be used",
        ):
            CompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["stop"] = 1

        with raises(TypeError, match="Expected stop to be of type 'str' or 'list'"):
            CompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["stop"] = ["<bot_end>"]
        base_request_body["logprobs"] = 2

        with raises(
            NotImplementedError, match="Logprobs is not supported at this time"
        ):
            CompletionsInputValidator(request_body=base_request_body).validate()
