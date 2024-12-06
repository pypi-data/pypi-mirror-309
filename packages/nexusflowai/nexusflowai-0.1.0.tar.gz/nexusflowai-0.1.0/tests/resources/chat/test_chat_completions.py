from typing import Any, Dict, List, Optional, Union

from enum import Enum
from unittest.mock import MagicMock, AsyncMock

from os import environ

from pydantic import BaseModel

from openai.types.chat.chat_completion_named_tool_choice_param import Function
from openai._types import NOT_GIVEN, NotGiven
from openai._streaming import Stream, AsyncStream
from openai._models import (
    FinalRequestOptions,
)
from openai.types.chat.completion_create_params import (
    CompletionCreateParams as ChatCompletionCreateParams,
)

from nexusflowai import NexusflowAI, AsyncNexusflowAI
from nexusflowai.types import (
    NexusflowAICompletionUsage,
    NexusflowAIChatCompletion,
    NexusflowAIChatCompletionChunk,
    NexusflowAIChatCompletionMessage,
    NexusflowAIChatCompletionMessageToolCall,
)
from nexusflowai.types.chat_completion import Choice
from nexusflowai.utils import get_extra_header

import nexusflowai.resources.chat.completions
from nexusflowai.resources.chat.completions import AsyncCompletions


from tests.utils import BASE_URL, API_KEY, MODEL_ID

import pytest
from pytest import fixture

from unittest.mock import MagicMock


def _mock_completions_pass_through_resp(model: str) -> NexusflowAIChatCompletion:
    return NexusflowAIChatCompletion(
        id="chatcmpl-9toBrs7jCx6UnFUQADzHJ93nhc6jb",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=NexusflowAIChatCompletionMessage(
                    content="The capital of France is Paris.",
                    role="assistant",
                    function_call=None,
                    tool_calls=None,
                    refusal=None,
                ),
                logprobs=None,
            )
        ],
        created=1723087999,
        model=model,
        object="chat.completion",
        system_fingerprint=None,
        usage=NexusflowAICompletionUsage(
            completion_tokens=7, prompt_tokens=24, total_tokens=31
        ),
    )


def _mock_completions_tools_resp(model: str) -> NexusflowAIChatCompletion:
    return NexusflowAIChatCompletion(
        id="chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
        choices=[
            Choice(
                finish_reason="tool_calls",
                index=0,
                message=NexusflowAIChatCompletionMessage(
                    content=None,
                    role="assistant",
                    function_call=None,
                    tool_calls=[
                        NexusflowAIChatCompletionMessageToolCall(
                            id="call_KDpcAwVN0FNZXERhXwVz6FNX",
                            function=Function(
                                arguments='{"location":"Paris, France"}',
                                name="get_current_weather",
                            ),
                            type="function",
                        )
                    ],
                    refusal=None,
                ),
                logprobs=None,
            )
        ],
        created=1723136387,
        model=model,
        object="chat.completion",
        system_fingerprint=None,
        usage=NexusflowAICompletionUsage(
            completion_tokens=17, prompt_tokens=86, total_tokens=103
        ),
    )


def _final_request_opts_pass_through() -> FinalRequestOptions:
    return FinalRequestOptions.construct(
        method="post",
        url="/chat/completions",
        params={},
        headers=get_extra_header(),
        max_retries=NOT_GIVEN,
        timeout=NOT_GIVEN,
        files=None,
        idempotency_key=None,
        post_parser=NOT_GIVEN,
        json_data={
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"},
            ],
            "model": MODEL_ID,
            "max_tokens": 150,
            "temperature": 0.7,
            "tools": [{"type": "function", "function": "some fake function"}],
            "n": 1,
            "stop": ["<bot_end>"],
        },
        extra_json=None,
    )


def _final_request_opts_tools() -> FinalRequestOptions:
    return FinalRequestOptions.construct(
        method="post",
        url="/chat/completions",
        params={},
        headers=get_extra_header(),
        max_retries=NOT_GIVEN,
        timeout=NOT_GIVEN,
        files=None,
        idempotency_key=None,
        post_parser=NOT_GIVEN,
        json_data={
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Weather in Paris, France?"},
            ],
            "model": MODEL_ID,
            "max_tokens": 150,
            "n": 1,  # n added
            "stop": ["<bot_end>"],  # stop sequence added
            "temperature": 0.7,
            "tools": [
                {
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "unit": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                },
                            },
                            "required": ["location"],
                        },
                    },
                }
            ],
        },
        extra_json=None,
    )


def _mock_completions_hints_resp() -> NexusflowAIChatCompletion:
    return NexusflowAIChatCompletion(
        id="chatcmpl-9toBrs7jCx6UnFUQADzHJ93nhc6jb",
        choices=[
            Choice(
                finish_reason="stop",
                index=0,
                message=NexusflowAIChatCompletionMessage(
                    content="The capital of France is Paris.",
                    role="assistant",
                    function_call=None,
                    tool_calls=None,
                    refusal=None,
                ),
                logprobs=None,
            )
        ],
        created=1723087999,
        model=MODEL_ID,
        object="chat.completion",
        system_fingerprint=None,
        usage=NexusflowAICompletionUsage(
            completion_tokens=7, prompt_tokens=24, total_tokens=31
        ),
        hints=["hint1", "hint2"],
    )


class TestChatCompletions:
    @fixture
    def setup_client(self, monkeypatch) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = NexusflowAI(base_url=BASE_URL)

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

    def test_completions_sanity(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "request", post_mock)
        post_mock.return_value = _mock_completions_pass_through_resp(model=model)

        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"},
            ],
            tools=[{"type": "function", "function": "some fake function"}],
            temperature=0.7,
            max_tokens=150,
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

        opts = _final_request_opts_pass_through()

        stream_type = Stream[NexusflowAIChatCompletionChunk]
        post_mock.assert_called_once_with(
            NexusflowAIChatCompletion,
            opts,
            stream=False,
            stream_cls=stream_type,
        )

    def test_hints(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "request", post_mock)
        post_mock.return_value = _mock_completions_hints_resp()

        maybe_print_hints_mock = MagicMock()
        maybe_print_hints_mock.side_effect = (
            nexusflowai.resources.chat.completions.maybe_print_hints
        )
        monkeypatch.setattr(
            nexusflowai.resources.chat.completions,
            "maybe_print_hints",
            maybe_print_hints_mock,
        )

        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"},
            ],
            tools=[{"type": "function", "function": "some fake function"}],
            temperature=0.7,
            max_tokens=150,
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

        maybe_print_hints_mock.assert_called_once()

    def test_completions_tools(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "request", post_mock)
        post_mock.return_value = _mock_completions_tools_resp(model=model)

        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Weather in Paris, France?"},
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "unit": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                },
                            },
                            "required": ["location"],
                        },
                    },
                }
            ],
            temperature=0.7,
            max_tokens=150,
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

        opts = _final_request_opts_tools()

        stream_type = Stream[NexusflowAIChatCompletionChunk]
        post_mock.assert_called_once_with(
            NexusflowAIChatCompletion,
            opts,
            stream=False,
            stream_cls=stream_type,
        )

    def test_completions_response_format_parsed(
        self, setup_client, monkeypatch
    ) -> None:
        """
        Uses examples from https://platform.openai.com/docs/guides/structured-outputs/examples
        """

        parsed = {
            "steps": [
                {
                    "explanation": "Start with the equation 8x + 7 = -23.",
                    "output": "8x + 7 = -23",
                },
                {
                    "explanation": "Subtract 7 from both sides to isolate the term with the variable.",
                    "output": "8x = -23 - 7",
                },
                {
                    "explanation": "Simplify the right side of the equation.",
                    "output": "8x = -30",
                },
                {
                    "explanation": "Divide both sides by 8 to solve for x.",
                    "output": "x = -30 / 8",
                },
                {"explanation": "Simplify the fraction.", "output": "x = -15 / 4"},
            ],
            "final_answer": "x = -15 / 4",
        }

        class Step(BaseModel):
            explanation: str
            output: str

        class MathReasoning(BaseModel):
            steps: List[Step]
            final_answer: str

        expected_output = MathReasoning(
            steps=[
                Step(
                    explanation="Start with the equation 8x + 7 = -23.",
                    output="8x + 7 = -23",
                ),
                Step(
                    explanation="Subtract 7 from both sides to isolate the term with the variable.",
                    output="8x = -23 - 7",
                ),
                Step(
                    explanation="Simplify the right side of the equation.",
                    output="8x = -30",
                ),
                Step(
                    explanation="Divide both sides by 8 to solve for x.",
                    output="x = -30 / 8",
                ),
                Step(
                    explanation="Simplify the fraction.",
                    output="x = -15 / 4",
                ),
            ],
            final_answer="x = -15 / 4",
        )
        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=MathReasoning,
            parsed=parsed,
            expected_output=expected_output,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "math_reasoning",
                "schema": {
                    "type": "object",
                    "properties": {
                        "steps": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "explanation": {"type": "string"},
                                    "output": {"type": "string"},
                                },
                                "required": ["explanation", "output"],
                                "additionalProperties": False,
                            },
                        },
                        "final_answer": {"type": "string"},
                    },
                    "required": ["steps", "final_answer"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }

        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=response_format,
            parsed=parsed,
            expected_output=parsed,
        )

        parsed = {
            "title": "Application of Quantum Algorithms in Interstellar Navigation: A New Frontier",
            "authors": ["Dr. Stella Voyager", "Dr. Nova Star", "Dr. Lyra Hunter"],
            "abstract": "This paper investigates the utilization of quantum algorithms to improve interstellar navigation systems. By leveraging quantum superposition and entanglement, our proposed navigation system can calculate optimal travel paths through space-time anomalies more efficiently than classical methods. Experimental simulations suggest a significant reduction in travel time and fuel consumption for interstellar missions.",
            "keywords": [
                "Quantum algorithms",
                "interstellar navigation",
                "space-time anomalies",
                "quantum superposition",
                "quantum entanglement",
                "space travel",
            ],
        }

        class ResearchPaperExtraction(BaseModel):
            title: str
            authors: List[str]
            abstract: str
            keywords: List[str]

        expected_output = ResearchPaperExtraction(
            title="Application of Quantum Algorithms in Interstellar Navigation: A New Frontier",
            authors=["Dr. Stella Voyager", "Dr. Nova Star", "Dr. Lyra Hunter"],
            abstract="This paper investigates the utilization of quantum algorithms to improve interstellar navigation systems. By leveraging quantum superposition and entanglement, our proposed navigation system can calculate optimal travel paths through space-time anomalies more efficiently than classical methods. Experimental simulations suggest a significant reduction in travel time and fuel consumption for interstellar missions.",
            keywords=[
                "Quantum algorithms",
                "interstellar navigation",
                "space-time anomalies",
                "quantum superposition",
                "quantum entanglement",
                "space travel",
            ],
        )
        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=ResearchPaperExtraction,
            parsed=parsed,
            expected_output=expected_output,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "research_paper_extraction",
                "schema": {
                    "type": "object",
                    "properties": {
                        "title": {"type": "string"},
                        "authors": {"type": "array", "items": {"type": "string"}},
                        "abstract": {"type": "string"},
                        "keywords": {"type": "array", "items": {"type": "string"}},
                    },
                    "required": ["title", "authors", "abstract", "keywords"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=response_format,
            parsed=parsed,
            expected_output=parsed,
        )

        parsed = {
            "type": "form",
            "label": "User Profile Form",
            "children": [
                {
                    "type": "div",
                    "label": "",
                    "children": [
                        {
                            "type": "field",
                            "label": "First Name",
                            "children": [],
                            "attributes": [
                                {"name": "type", "value": "text"},
                                {"name": "name", "value": "firstName"},
                                {
                                    "name": "placeholder",
                                    "value": "Enter your first name",
                                },
                            ],
                        },
                        {
                            "type": "field",
                            "label": "Last Name",
                            "children": [],
                            "attributes": [
                                {"name": "type", "value": "text"},
                                {"name": "name", "value": "lastName"},
                                {
                                    "name": "placeholder",
                                    "value": "Enter your last name",
                                },
                            ],
                        },
                    ],
                    "attributes": [],
                },
                {
                    "type": "button",
                    "label": "Submit",
                    "children": [],
                    "attributes": [{"name": "type", "value": "submit"}],
                },
            ],
            "attributes": [
                {"name": "method", "value": "post"},
                {"name": "action", "value": "/submit-profile"},
            ],
        }

        class UIType(str, Enum):
            div = "div"
            button = "button"
            header = "header"
            section = "section"
            field = "field"
            form = "form"

        class Attribute(BaseModel):
            name: str
            value: str

        class UI(BaseModel):
            type: UIType
            label: str
            children: List["UI"]
            attributes: List[Attribute]

        UI.model_rebuild()  # This is required to enable recursive types

        expected_output = UI(
            type="form",
            label="User Profile Form",
            children=[
                UI(
                    type="div",
                    label="",
                    children=[
                        UI(
                            type="field",
                            label="First Name",
                            children=[],
                            attributes=[
                                Attribute(
                                    name="type",
                                    value="text",
                                ),
                                Attribute(
                                    name="name",
                                    value="firstName",
                                ),
                                Attribute(
                                    name="placeholder",
                                    value="Enter your first name",
                                ),
                            ],
                        ),
                        UI(
                            type="field",
                            label="Last Name",
                            children=[],
                            attributes=[
                                Attribute(
                                    name="type",
                                    value="text",
                                ),
                                Attribute(
                                    name="name",
                                    value="lastName",
                                ),
                                Attribute(
                                    name="placeholder",
                                    value="Enter your last name",
                                ),
                            ],
                        ),
                    ],
                    attributes=[],
                ),
                UI(
                    type="button",
                    label="Submit",
                    children=[],
                    attributes=[
                        Attribute(
                            name="type",
                            value="submit",
                        ),
                    ],
                ),
            ],
            attributes=[
                Attribute(
                    name="method",
                    value="post",
                ),
                Attribute(
                    name="action",
                    value="/submit-profile",
                ),
            ],
        )
        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=UI,
            parsed=parsed,
            expected_output=expected_output,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "ui",
                "description": "Dynamically generated UI",
                "schema": {
                    "type": "object",
                    "properties": {
                        "type": {
                            "type": "string",
                            "description": "The type of the UI component",
                            "enum": [
                                "div",
                                "button",
                                "header",
                                "section",
                                "field",
                                "form",
                            ],
                        },
                        "label": {
                            "type": "string",
                            "description": "The label of the UI component, used for buttons or form fields",
                        },
                        "children": {
                            "type": "array",
                            "description": "Nested UI components",
                            "items": {"$ref": "#"},
                        },
                        "attributes": {
                            "type": "array",
                            "description": "Arbitrary attributes for the UI component, suitable for any element",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "name": {
                                        "type": "string",
                                        "description": "The name of the attribute, for example onClick or className",
                                    },
                                    "value": {
                                        "type": "string",
                                        "description": "The value of the attribute",
                                    },
                                },
                                "required": ["name", "value"],
                                "additionalProperties": False,
                            },
                        },
                    },
                    "required": ["type", "label", "children", "attributes"],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=response_format,
            parsed=parsed,
            expected_output=parsed,
        )

        parsed = {
            "is_violating": False,
            "category": None,
            "explanation_if_violating": None,
        }

        class Category(str, Enum):
            violence = "violence"
            sexual = "sexual"
            self_harm = "self_harm"

        class ContentCompliance(BaseModel):
            is_violating: bool
            category: Optional[Category]
            explanation_if_violating: Optional[str]

        expected_output = ContentCompliance(
            is_violating=False,
            category=None,
            explanation_if_violating=None,
        )
        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=ContentCompliance,
            parsed=parsed,
            expected_output=expected_output,
        )

        response_format = {
            "type": "json_schema",
            "json_schema": {
                "name": "content_compliance",
                "description": "Determines if content is violating specific moderation rules",
                "schema": {
                    "type": "object",
                    "properties": {
                        "is_violating": {
                            "type": "boolean",
                            "description": "Indicates if the content is violating guidelines",
                        },
                        "category": {
                            "type": ["string", "null"],
                            "description": "Type of violation, if the content is violating guidelines. Null otherwise.",
                            "enum": ["violence", "sexual", "self_harm"],
                        },
                        "explanation_if_violating": {
                            "type": ["string", "null"],
                            "description": "Explanation of why the content is violating",
                        },
                    },
                    "required": [
                        "is_violating",
                        "category",
                        "explanation_if_violating",
                    ],
                    "additionalProperties": False,
                },
                "strict": True,
            },
        }
        self._response_format_parsed_test_helper(
            monkeypatch,
            response_format=response_format,
            parsed=parsed,
            expected_output=parsed,
        )

    def _response_format_parsed_test_helper(
        self,
        monkeypatch,
        response_format: Union[BaseModel, Dict[str, Any]],
        parsed: Dict[str, Any],
        expected_output: Union[BaseModel, Dict[str, Any]],
    ) -> None:
        client = self.client
        model = MODEL_ID

        mock_cc = NexusflowAIChatCompletion(
            id="chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
            choices=[
                Choice(
                    finish_reason="tool_calls",
                    index=0,
                    message=NexusflowAIChatCompletionMessage(
                        content=None,
                        role="assistant",
                        function_call=None,
                        parsed=parsed,
                        refusal=None,
                    ),
                    logprobs=None,
                )
            ],
            created=1723136387,
            model=MODEL_ID,
            object="chat.completion",
            system_fingerprint=None,
            usage=NexusflowAICompletionUsage(
                completion_tokens=17, prompt_tokens=86, total_tokens=103
            ),
        )
        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "request", post_mock)
        post_mock.return_value = mock_cc

        res = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Weather in Paris, France?"},
            ],
            tools=NOT_GIVEN,
            temperature=0.7,
            max_tokens=150,
            response_format=response_format,
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

        actual_output = res.choices[0].message.parsed
        assert expected_output == actual_output

    def test_execution_result_sanity(self) -> None:
        json_with_empty_execution_result = {
            "id": "chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "message": {
                        "content": None,
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_KDpcAwVN0FNZXERhXwVz6FNX",
                                "function": {
                                    "arguments": '{"location":"Paris, France"}',
                                    "name": "get_current_weather",
                                },
                                "type": "function",
                                "execution_result": None,
                            }
                        ],
                        "parsed": None,
                        "function_call": None,
                        "refusal": None,
                    },
                    "logprobs": None,
                }
            ],
            "created": 1723136387,
            "model": "test model",
            "object": "chat.completion",
            "system_fingerprint": None,
            "usage": {
                "completion_tokens": 17,
                "prompt_tokens": 86,
                "total_tokens": 103,
            },
            "hints": None,
        }
        cc = NexusflowAIChatCompletion.model_validate(json_with_empty_execution_result)
        expected_execution_result = None
        actual_execution_result = cc.choices[0].message.tool_calls[0].execution_result
        assert expected_execution_result == actual_execution_result

        json_with_str_execution_result = {
            "id": "chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "message": {
                        "content": None,
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_KDpcAwVN0FNZXERhXwVz6FNX",
                                "function": {
                                    "arguments": '{"location":"Paris, France"}',
                                    "name": "get_current_weather",
                                },
                                "type": "function",
                                "execution_result": {
                                    "type": "text",
                                    "text": "some execution result str",
                                },
                            }
                        ],
                        "parsed": None,
                        "function_call": None,
                        "refusal": None,
                    },
                    "logprobs": None,
                }
            ],
            "created": 1723136387,
            "model": "test model",
            "object": "chat.completion",
            "system_fingerprint": None,
            "usage": {
                "completion_tokens": 17,
                "prompt_tokens": 86,
                "total_tokens": 103,
            },
            "hints": None,
        }
        cc = NexusflowAIChatCompletion.model_validate(json_with_str_execution_result)
        expected_text = "some execution result str"
        actual_text = cc.choices[0].message.tool_calls[0].execution_result["text"]
        assert expected_text == actual_text

        json_with_image_url_execution_result = {
            "id": "chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "message": {
                        "content": None,
                        "role": "assistant",
                        "tool_calls": [
                            {
                                "id": "call_KDpcAwVN0FNZXERhXwVz6FNX",
                                "function": {
                                    "arguments": '{"location":"Paris, France"}',
                                    "name": "get_current_weather",
                                },
                                "type": "function",
                                "execution_result": {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": "blah url",
                                        "detail": "auto",
                                    },
                                },
                            }
                        ],
                        "parsed": None,
                        "function_call": None,
                        "refusal": None,
                    },
                    "logprobs": None,
                }
            ],
            "created": 1723136387,
            "model": "test model",
            "object": "chat.completion",
            "system_fingerprint": None,
            "usage": {
                "completion_tokens": 17,
                "prompt_tokens": 86,
                "total_tokens": 103,
            },
            "hints": None,
        }
        cc = NexusflowAIChatCompletion.model_validate(
            json_with_image_url_execution_result
        )
        expected_url = "blah url"
        actual_url = (
            cc.choices[0].message.tool_calls[0].execution_result["image_url"]["url"]
        )
        assert expected_url == actual_url


class TestAsyncCompletions:
    @fixture
    def setup_client(self, monkeypatch) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = AsyncNexusflowAI(base_url=BASE_URL)

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

    @pytest.mark.asyncio
    async def test_completions_pass_through(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(AsyncNexusflowAI, "request", post_mock)

        async def async_mock_response():
            return _mock_completions_pass_through_resp(model=model)

        post_mock.return_value = async_mock_response()

        res = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What is the capital of France?"},
            ],
            tools=[{"type": "function", "function": "some fake function"}],
            temperature=0.7,
            max_tokens=150,
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

        opts = _final_request_opts_pass_through()

        stream_type = AsyncStream[NexusflowAIChatCompletionChunk]
        post_mock.assert_called_once_with(
            NexusflowAIChatCompletion,
            opts,
            stream=False,
            stream_cls=stream_type,
        )

    @pytest.mark.asyncio
    async def test_completions_tools(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(AsyncNexusflowAI, "request", post_mock)

        async def async_mock_response():
            return _mock_completions_tools_resp(model=model)

        post_mock.return_value = async_mock_response()

        res = await client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Weather in Paris, France?"},
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_current_weather",
                        "description": "Get the current weather in a given location",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "location": {
                                    "type": "string",
                                    "description": "The city and state, e.g. San Francisco, CA",
                                },
                                "unit": {
                                    "type": "string",
                                    "enum": ["celsius", "fahrenheit"],
                                },
                            },
                            "required": ["location"],
                        },
                    },
                }
            ],
            temperature=0.7,
            max_tokens=150,
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

        opts = _final_request_opts_tools()

        stream_type = AsyncStream[NexusflowAIChatCompletionChunk]
        post_mock.assert_called_once_with(
            NexusflowAIChatCompletion,
            opts,
            stream=False,
            stream_cls=stream_type,
        )

    def test_batch_run_messages(self, setup_client, monkeypatch):
        """
        Test if
        1. The chat completions create call is called the correct number of times.
        2. Prompts are created and batched correctly.
        3. The batched prompts  contain the correctly parsed prompts.
        4. An error is raised if stream is set to True
        """
        client = self.client

        mock_completion1 = MagicMock()
        mock_completion2 = MagicMock()

        mock_completion = [mock_completion1, mock_completion2]

        mock_create = AsyncMock()
        mock_create.side_effect = mock_completion

        monkeypatch.setattr(AsyncCompletions, "create", mock_create)

        # check if the chat completions create call is called the correct number of times.
        mock_batch_messages = [
            [
                {
                    "role": "dummy user 1",
                    "content": "dummy content 1",
                },
            ],
            [
                {
                    "role": "dummy user 2",
                    "content": "dummy content 2",
                },
            ],
        ]

        mock_params: ChatCompletionCreateParams = dict(
            {"stream": False, "max_tokens": 10, "temperature": 1.0}
        )

        response = client.chat.completions.batch_run_messages(
            batch_messages=mock_batch_messages, params=mock_params
        )

        assert len(mock_batch_messages) == len(response)

        # check if the length of batched messages created is correct
        expected_messages_list = [
            {
                "stream": False,
                "max_tokens": 10,
                "temperature": 1.0,
                "messages": [
                    {
                        "role": "dummy user 1",
                        "content": "dummy content 1",
                    },
                ],
            },
            {
                "stream": False,
                "max_tokens": 10,
                "temperature": 1.0,
                "messages": [
                    {
                        "role": "dummy user 2",
                        "content": "dummy content 2",
                    },
                ],
            },
        ]

        # check if the batched messages contain the correctly parsed prompts
        actual_messages_list = [d for _, d in mock_create.call_args_list]
        assert all(d in expected_messages_list for d in actual_messages_list)
        assert all(d in actual_messages_list for d in expected_messages_list)

        # check if error is raised if stream is set to True
        mock_params: ChatCompletionCreateParams = {"stream": True}

        with pytest.raises(
            ValueError, match="Batch create does not support streaming requests!"
        ):
            response = client.chat.completions.batch_run_messages(
                batch_messages=mock_batch_messages, params=mock_params
            )
