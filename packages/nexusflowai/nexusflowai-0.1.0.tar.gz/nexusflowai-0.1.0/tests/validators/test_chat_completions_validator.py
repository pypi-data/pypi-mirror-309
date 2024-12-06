from typing import Any, List, Optional

from enum import Enum

from pydantic import BaseModel, EmailStr

from openai.types.chat.completion_create_params import CompletionCreateParams
from openai._utils import maybe_transform
from openai._types import NOT_GIVEN

from nexusflowai.validators.base_input_validator import (
    MAX_STOP_SEQUENCES,
    BOT_END,
)
from nexusflowai.validators import ChatCompletionsInputValidator
from nexusflowai.validators.json_schema_to_dataclasses import (
    try_convert_to_dataclasses_str,
)
from nexusflowai._exceptions import DeprecationError

from pytest import raises


class TestChatCompletionValidator:
    def test_validate(self) -> None:
        base_request_body = maybe_transform(
            {
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": "What's the weather like in New York?"},
                ],
                "model": "gpt-4",
                "frequency_penalty": 0,
                "function_call": NOT_GIVEN,
                "functions": NOT_GIVEN,
                "logit_bias": None,
                "max_tokens": 150,
                "n": NOT_GIVEN,
                "presence_penalty": 0,
                "response_format": NOT_GIVEN,
                "seed": 42,
                "stop": NOT_GIVEN,
                "stream": NOT_GIVEN,
                "temperature": 0.7,
                "tool_choice": NOT_GIVEN,
                "tools": NOT_GIVEN,
                "top_p": 1,
                "user": "user_123456",
            },
            CompletionCreateParams,
        )

        # no tools or response format
        validated_rb = ChatCompletionsInputValidator(
            request_body=base_request_body
        ).validate()

        base_request_body["tools"] = [
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
        ]

        base_request_body["function_call"] = "auto"

        # Test deprecated error for function_call or functions
        with raises(
            DeprecationError,
            match="The function_call parameter is deprecated",
        ):
            ChatCompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["function_call"] = NOT_GIVEN
        base_request_body["tool_choice"] = "auto"

        # Test tool_choice not implemented error
        with raises(
            NotImplementedError,
            match="The tool_choice parameter is currently not supported.  It may be supported in the future, but this is not a commitment to support it in the future.",
        ):
            ChatCompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["tool_choice"] = NOT_GIVEN

        # Test n
        validated_rb = ChatCompletionsInputValidator(
            request_body=base_request_body
        ).validate()

        assert validated_rb["n"] == 1
        base_request_body["n"] = 2
        with raises(
            NotImplementedError,
            match="The only supported value for the n parameter is 1",
        ):
            ChatCompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["n"] = NOT_GIVEN
        base_request_body["stream"] = True

        # Test stream true assertion error
        with raises(
            AssertionError,
            match="Streaming is not supported with tools!",
        ):
            ChatCompletionsInputValidator(request_body=base_request_body).validate()

        # Test stream true without tools
        tools = base_request_body["tools"]
        base_request_body["tools"] = NOT_GIVEN
        ChatCompletionsInputValidator(request_body=base_request_body).validate()
        base_request_body["tools"] = tools

        base_request_body["stream"] = NOT_GIVEN

        # Test stop tokens
        validated_rb = ChatCompletionsInputValidator(
            request_body=base_request_body
        ).validate()

        assert validated_rb["stop"] == [BOT_END]

        base_request_body["stop"] = ["foo", "bar"]

        validated_rb = ChatCompletionsInputValidator(
            request_body=base_request_body
        ).validate()

        assert validated_rb["stop"] == ["foo", "bar", BOT_END]

        base_request_body["stop"] = ["foo", "bar", "boo", "far"]

        with raises(
            ValueError,
            match=f"A maximum of {MAX_STOP_SEQUENCES} stop sequences can be used, and one of them should be {BOT_END}",
        ):
            ChatCompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["stop"] = ["foo", "bar", "boo", "far", BOT_END]

        with raises(
            ValueError,
            match=f"A maximum of {MAX_STOP_SEQUENCES} stop sequences can be used",
        ):
            ChatCompletionsInputValidator(request_body=base_request_body).validate()

        base_request_body["stop"] = 1

        with raises(TypeError, match="Expected stop to be of type 'str' or 'list'"):
            ChatCompletionsInputValidator(request_body=base_request_body).validate()

    def _response_format_test_helper(
        self,
        response_format: Any,
        expected_response_format: Any = None,
        expected_dataclasses_str: str = None,
    ) -> None:
        request_dict = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What's the weather like in New York?"},
            ],
            "model": "gpt-4",
            "frequency_penalty": 0,
            "function_call": NOT_GIVEN,
            "functions": NOT_GIVEN,
            "logit_bias": None,
            "max_tokens": 150,
            "n": NOT_GIVEN,
            "presence_penalty": 0,
            "response_format": response_format,
            "seed": 42,
            "stop": NOT_GIVEN,
            "stream": NOT_GIVEN,
            "temperature": 0.7,
            "tool_choice": NOT_GIVEN,
            "tools": [],
            "top_p": 1,
            "user": "user_123456",
        }

        request_body = maybe_transform(request_dict, CompletionCreateParams)
        validator = ChatCompletionsInputValidator(request_body=request_body)
        validated_rb = validator.validate()

        actual_response_format = validated_rb["response_format"]
        if expected_response_format is not None:
            assert expected_response_format == actual_response_format

        if expected_dataclasses_str is not None:
            actual_dataclasses_str = try_convert_to_dataclasses_str(
                actual_response_format
            )[1]
            assert (
                expected_dataclasses_str == actual_dataclasses_str
            ), actual_response_format

    def test_validate_response_format_sanity(self) -> None:
        self._response_format_test_helper(NOT_GIVEN, NOT_GIVEN)

        class Person(BaseModel):
            name: str
            age: int
            email: Optional[EmailStr] = None

        expected_response_format = {
            "type": "json_schema",
            "json_schema": {
                "properties": {
                    "name": {"title": "Name", "type": "string"},
                    "age": {"title": "Age", "type": "integer"},
                    "email": {
                        "anyOf": [
                            {"format": "email", "type": "string"},
                            {"type": "null"},
                        ],
                        "default": None,
                        "title": "Email",
                    },
                },
                "required": ["name", "age"],
                "title": "Person",
                "type": "object",
            },
        }

        self._response_format_test_helper(Person, expected_response_format)

        input_json_schema_dict = {
            "title": "Person",
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "age": {"type": "integer"},
                "email": {"type": "string", "format": "email"},
            },
            "required": ["name", "age"],
        }
        expected_response_format = {
            "type": "json_schema",
            "json_schema": input_json_schema_dict,
        }
        self._response_format_test_helper(
            input_json_schema_dict, expected_response_format
        )

        with raises(AssertionError):
            invalid_json_schema = 2
            self._response_format_test_helper(invalid_json_schema, None)

    def test_validate_response_format_openai_examples(self) -> None:
        """
        From https://platform.openai.com/docs/guides/structured-outputs/introduction
        """

        expected_dataclasses_str = """@dataclass
class Step:
    explanation: str
    output: str


@dataclass
class MathReasoning:
    steps: List[Step]
    final_answer: str
"""

        class Step(BaseModel):
            explanation: str
            output: str

        class MathReasoning(BaseModel):
            steps: List[Step]
            final_answer: str

        self._response_format_test_helper(
            MathReasoning, expected_dataclasses_str=expected_dataclasses_str
        )

        input_json_schema = {
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
        self._response_format_test_helper(
            input_json_schema, expected_dataclasses_str=expected_dataclasses_str
        )

        expected_dataclasses_str = """@dataclass
class ResearchPaperExtraction:
    title: str
    authors: List[str]
    abstract: str
    keywords: List[str]
"""

        class ResearchPaperExtraction(BaseModel):
            title: str
            authors: List[str]
            abstract: str
            keywords: List[str]

        self._response_format_test_helper(
            ResearchPaperExtraction, expected_dataclasses_str=expected_dataclasses_str
        )

        input_json_schema = {
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
        self._response_format_test_helper(
            input_json_schema, expected_dataclasses_str=expected_dataclasses_str
        )

        expected_dataclasses_str = """@dataclass
class Attribute:
    name: str
    value: str


class UIType(Enum):
    div = 'div'
    button = 'button'
    header = 'header'
    section = 'section'
    field = 'field'
    form = 'form'


@dataclass
class UI:
    type: UIType
    label: str
    children: List[UI]
    attributes: List[Attribute]


@dataclass
class Response:
    ui: UI
"""

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

        class Response(BaseModel):
            ui: UI

        self._response_format_test_helper(
            Response, expected_dataclasses_str=expected_dataclasses_str
        )

        expected_dataclasses_str = """class Type(Enum):
    \"\"\"
    The type of the UI component
    \"\"\"

    div = 'div'
    button = 'button'
    header = 'header'
    section = 'section'
    field = 'field'
    form = 'form'


@dataclass
class Attribute:
    name: str
    \"\"\"
    The name of the attribute, for example onClick or className
    \"\"\"
    value: str
    \"\"\"
    The value of the attribute
    \"\"\"


@dataclass
class Ui:
    type: Type
    \"\"\"
    The type of the UI component
    \"\"\"
    label: str
    \"\"\"
    The label of the UI component, used for buttons or form fields
    \"\"\"
    children: List[Ui]
    \"\"\"
    Nested UI components
    \"\"\"
    attributes: List[Attribute]
    \"\"\"
    Arbitrary attributes for the UI component, suitable for any element
    \"\"\"
"""
        input_json_schema = {
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
        self._response_format_test_helper(
            input_json_schema, expected_dataclasses_str=expected_dataclasses_str
        )

        expected_dataclasses_str = """class Category(Enum):
    violence = 'violence'
    sexual = 'sexual'
    self_harm = 'self_harm'


@dataclass
class ContentCompliance:
    is_violating: bool
    category: Optional[Category]
    explanation_if_violating: Optional[str]
"""

        class Category(str, Enum):
            violence = "violence"
            sexual = "sexual"
            self_harm = "self_harm"

        class ContentCompliance(BaseModel):
            is_violating: bool
            category: Optional[Category]
            explanation_if_violating: Optional[str]

        self._response_format_test_helper(
            ContentCompliance, expected_dataclasses_str=expected_dataclasses_str
        )

        expected_dataclasses_str = """class Category(Enum):
    \"\"\"
    Type of violation, if the content is violating guidelines. Null otherwise.
    \"\"\"

    violence = 'violence'
    sexual = 'sexual'
    self_harm = 'self_harm'


@dataclass
class ContentCompliance:
    is_violating: bool
    \"\"\"
    Indicates if the content is violating guidelines
    \"\"\"
    category: Category
    \"\"\"
    Type of violation, if the content is violating guidelines. Null otherwise.
    \"\"\"
    explanation_if_violating: Optional[str]
    \"\"\"
    Explanation of why the content is violating
    \"\"\"
"""
        input_json_schema = {
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
        self._response_format_test_helper(
            input_json_schema, expected_dataclasses_str=expected_dataclasses_str
        )

    def test_response_format_stream_not_allowed(self) -> None:
        class Person(BaseModel):
            name: str
            age: int
            email: Optional[EmailStr] = None

        response_format = Person

        request_dict = {
            "messages": [
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "What's the weather like in New York?"},
            ],
            "model": "gpt-4",
            "frequency_penalty": 0,
            "function_call": NOT_GIVEN,
            "functions": NOT_GIVEN,
            "logit_bias": None,
            "max_tokens": 150,
            "n": NOT_GIVEN,
            "presence_penalty": 0,
            "response_format": response_format,
            "seed": 42,
            "stop": NOT_GIVEN,
            "stream": True,
            "temperature": 0.7,
            "tool_choice": NOT_GIVEN,
            "tools": [],
            "top_p": 1,
            "user": "user_123456",
        }

        request_body = maybe_transform(request_dict, CompletionCreateParams)
        with raises(
            AssertionError,
            match="Streaming is not supported with response format!",
        ):
            ChatCompletionsInputValidator(request_body=request_body).validate()
