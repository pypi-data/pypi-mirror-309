from typing import Dict, List, Tuple, Type, Optional

from dataclasses import dataclass

from os import environ
from os.path import join, splitext, split

from glob import glob

import json
from unittest.mock import MagicMock, AsyncMock
import pytest
from pytest import fixture, mark, raises
from _pytest.assertion.util import _compare_eq_any

from pydantic import BaseModel, Field

from openai._types import NOT_GIVEN, NotGiven
from openai._streaming import Stream, AsyncStream
from openai._models import (
    FinalRequestOptions,
)
from openai.types.completion_create_params import CompletionCreateParams
from openai.types.chat.completion_create_params import (
    CompletionCreateParams as ChatCompletionCreateParams,
)

from nexusflowai import NexusflowAI, AsyncNexusflowAI
from nexusflowai.utils import get_extra_header
from nexusflowai.types import (
    NexusflowAICompletionUsage,
    NexusflowAICompletionChoice,
    NexusflowAICompletion,
    NexusflowAIChatCompletionMessage,
    NexusflowAIChatCompletionMessageToolCall,
    NexusflowAIChatCompletion,
)
from nexusflowai.types.chat_completion_message_tool_call import Function
from nexusflowai.validators.create_with_tools import ChatCompletionToolsFlow
from nexusflowai.validators.create_with_tools.postprocess import (
    FunctionCallResponseTranslator,
)
from nexusflowai.resources.completions import AsyncCompletions

from tests.utils import BASE_URL, API_KEY, MODEL_ID


def _mock_completions_data(model: str) -> NexusflowAICompletion:
    chat_fc = dict()
    chat_fc["name"] = "test_func"
    chat_fc["arguments"] = json.dumps({"c": "the cat", "d": 2})

    return NexusflowAICompletion(
        id="cmpl-9tkIbmAYHM9lGSaSG75A2x9BNJERb",
        choices=[
            NexusflowAICompletionChoice(
                finish_reason="length",
                index=0,
                logprobs=None,
                text="bob(a=1, b=frank(c='the cat', d=2), e=3)",
                message=NexusflowAIChatCompletionMessage(
                    content="bob(a=1, b=frank(c='the cat', d=2), e=3)",
                    role="assistant",
                    function_call=None,
                    tool_calls=[
                        NexusflowAIChatCompletionMessageToolCall(
                            id="call_1",
                            type="function",
                            function=Function.model_validate(chat_fc),
                        )
                    ],
                ),
            )
        ],
        created=1723073041,
        model=model,
        object="text_completion",
        system_fingerprint=None,
        usage=NexusflowAICompletionUsage(
            completion_tokens=16, prompt_tokens=2, total_tokens=18
        ),
    )


def _final_request_opts() -> None:
    return FinalRequestOptions.construct(
        method="post",
        url="/completions",
        params={},
        headers=get_extra_header(),
        max_retries=NOT_GIVEN,
        timeout=NOT_GIVEN,
        files=None,
        idempotency_key=None,
        post_parser=NOT_GIVEN,
        json_data={
            "model": MODEL_ID,
            "prompt": "Hello World!",
            # added by validator
            "best_of": 1,
            "echo": False,
            "n": 1,
            "stop": ["<bot_end>"],
            "temperature": 0.0,
        },
        extra_json=None,
    )


def discover_in_dir(
    cls: Type, input_fnames: List[str], parent_dir_path: str
) -> Dict[str, List]:
    dir_names = glob(join(parent_dir_path, "*"))
    dir_paths = [join(parent_dir_path, n) for n in dir_names]

    examples = []
    for dir_path in dir_paths:
        example_dict = {"dir_path": dir_path, "test_case_id": split(dir_path)[-1]}
        fnames = glob(join(dir_path, "*"))
        fnames = [n for n in fnames if any(n.endswith(i) for i in input_fnames)]

        for fname in fnames:
            fname_no_ext, ext = splitext(fname)
            fname_no_ext = split(fname_no_ext)[-1]
            fpath = join(dir_path, fname)
            with open(fpath) as f:
                if ext == ".json":
                    value = json.load(f)
                elif ext == ".txt":
                    value = f.read()
                else:
                    raise NotImplementedError

            example_dict[fname_no_ext] = value

        example = cls(**example_dict)
        examples.append(example)

    return {
        "argvalues": examples,
        "ids": [e.test_case_id for e in examples],
    }


@dataclass
class CreateWithToolsTestCase:
    test_case_id: str
    dir_path: str

    chat_completion_create_params: ChatCompletionCreateParams

    expected_prompt: Optional[str] = None
    expected_exception: Optional[Dict[str, str]] = None

    @classmethod
    def test_cases(cls) -> Dict[str, List]:
        INPUT_FNAMES = [
            "chat_completion_create_params.json",
            "expected_prompt.txt",
            "expected_exception.json",
        ]
        parent_dir_path = join(split(__file__)[0], "create_with_tools")
        return discover_in_dir(cls, INPUT_FNAMES, parent_dir_path)


@dataclass
class FunctionCallResponseTestCase:
    test_case_id: str
    dir_path: str

    tool_params: List
    raw_response: str

    expected_parallel_function_calls: Optional[List[List[str]]] = None
    expected_tool_calls: Optional[List[Dict[str, str]]] = None
    expected_exception: Optional[Dict[str, str]] = None

    @classmethod
    def test_cases(cls) -> Dict[str, List]:
        INPUT_FNAMES = [
            "tool_params.json",
            "raw_response.txt",
            "expected_parallel_function_calls.json",
            "expected_tool_calls.json",
            "expected_exception.json",
        ]
        parent_dir_path = join(split(__file__)[0], "function_call_response")
        return discover_in_dir(cls, INPUT_FNAMES, parent_dir_path)


class TestCompletions:
    @fixture
    def setup_client(self) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = NexusflowAI(base_url=BASE_URL)

    def test_completions(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "request", post_mock)
        post_mock.return_value = _mock_completions_data(model=model)

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

        res = client.completions.create(model=model, prompt="Hello World!")
        assert res.__class__ == NexusflowAICompletion
        assert len(res.choices) == 1

        opts = _final_request_opts()

        stream_type = Stream[NexusflowAICompletion]
        post_mock.assert_called_once_with(
            NexusflowAICompletion,
            opts,
            stream=False,
            stream_cls=stream_type,
        )

    def test_create_with_tools_tools_e2e(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "request", post_mock)
        post_mock.return_value = NexusflowAICompletion(
            id="cmpl-9tkIbmAYHM9lGSaSG75A2x9BNJERb",
            choices=[
                NexusflowAICompletionChoice(
                    finish_reason="length",
                    index=0,
                    logprobs=None,
                    text="get_weather(city_name='Berkeley, CA')",
                )
            ],
            created=1723073041,
            model=model,
            object="text_completion",
            system_fingerprint=None,
            usage=NexusflowAICompletionUsage(
                completion_tokens=16, prompt_tokens=2, total_tokens=18
            ),
        )

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

        res = client.completions.create_with_tools(
            model="nexus-tool-use-20240816",
            messages=[
                {
                    "role": "user",
                    "content": "i am in berkeley.",
                },
            ],
            tools=[
                {
                    "type": "function",
                    "function": {
                        "name": "get_weather",
                        "description": "",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "city_name": {
                                    "type": "string",
                                    "description": "",
                                },
                            },
                            "required": ["city_name"],
                            "additionalProperties": False,
                        },
                    },
                }
            ],
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

    def test_create_with_tools_response_format_e2e(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(NexusflowAI, "request", post_mock)
        post_mock.return_value = NexusflowAICompletion(
            id="cmpl-9tkIbmAYHM9lGSaSG75A2x9BNJERb",
            choices=[
                NexusflowAICompletionChoice(
                    finish_reason="length",
                    index=0,
                    logprobs=None,
                    text="extract_item(value=GasDistributionNetwork(networkID='GDN-4521', pipelineValues={'pipeline_1': [275, 500000], 'pipeline_2': [17, 12000]}, maintenanceSchedules=['January', 'April', 'July', 'October']))",
                )
            ],
            created=1723073041,
            model=model,
            object="text_completion",
            system_fingerprint=None,
            usage=NexusflowAICompletionUsage(
                completion_tokens=16, prompt_tokens=2, total_tokens=18
            ),
        )

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

        class GasDistributionNetwork(BaseModel):
            networkID: str = Field(
                ...,
                description="The identifier for the gas distribution network.",
                title="Network ID",
            )
            pipelineValues: Dict[str, Tuple[int, int]] = Field(
                description="The mapping with key pipeline_1, pipeline_2, etc ... to tuple of (total length in kilometers, maximum amount of gas that can be distributed in cubic meters).",
                title="Pipeline Values",
            )
            maintenanceSchedules: List[str] = Field(
                ...,
                description="The schedule detailing when maintenance activities are to be performed.",
                title="Maintenance Schedule",
            )

        res = client.completions.create_with_tools(
            model="nexus-tool-use-20240816",
            messages=[
                {
                    "role": "user",
                    "content": """I am currently working on a project that involves mapping out a gas distribution network for a new residential area. The network is quite extensive and includes several pipelines that distribute natural gas to various sectors of the community. I need to create a JSON object that captures the essential details of this network. The information I have includes a unique identifier for the network, which is 'GDN-4521'. The total length of the pipeline_1 is 275 kilometers with a capacity 500,000 cubic meters. Pipeline 2 is 17 kilometers long and has a capacity of 12,000 cubic meters. Additionally, there is a detailed maintenance schedule, which includes quarterly inspections in January, April, July, and October.""",
                },
            ],
            response_format=GasDistributionNetwork,
        )
        assert res.__class__ == NexusflowAIChatCompletion
        assert len(res.choices) == 1

        assert isinstance(res.choices[0].message.parsed, GasDistributionNetwork)

    @mark.parametrize("cwt_tc", **CreateWithToolsTestCase.test_cases())
    def test_create_with_tools(self, cwt_tc: CreateWithToolsTestCase) -> None:
        flow = ChatCompletionToolsFlow()

        if cwt_tc.expected_prompt is not None:
            res = flow.preprocess(cwt_tc.chat_completion_create_params)
            actual_prompt = res["prompt"]
            with open(join(cwt_tc.dir_path, "actual_prompt.txt"), "w") as f:
                f.write(actual_prompt)
            diff_prompt = _compare_eq_any(
                cwt_tc.expected_prompt, actual_prompt, verbose=1
            )
            with open(join(cwt_tc.dir_path, "diff_prompt.txt"), "w") as f:
                f.write("\n".join(diff_prompt))
            assert cwt_tc.expected_prompt == actual_prompt

        if cwt_tc.expected_exception is not None:
            expected_exception = eval(cwt_tc.expected_exception["expected_exception"])
            match = cwt_tc.expected_exception["match"]

            exception = None
            try:
                with raises(expected_exception, match=match) as exc_info:
                    flow.preprocess(cwt_tc.chat_completion_create_params)
            except Exception as e:
                exception = e

            actual_exception = exc_info.value.args[0]
            with open(join(cwt_tc.dir_path, "actual_exception.txt"), "w") as f:
                f.write(actual_exception)
            diff_prompt = _compare_eq_any(match, actual_exception, verbose=1)
            with open(join(cwt_tc.dir_path, "diff_exception.txt"), "w") as f:
                f.write("\n".join(diff_prompt))

            if exception is not None:
                raise exception

    @mark.parametrize("fcr_tc", **FunctionCallResponseTestCase.test_cases())
    def test_function_call_response(self, fcr_tc: FunctionCallResponseTestCase) -> None:
        fct = FunctionCallResponseTranslator()
        if fcr_tc.expected_parallel_function_calls:
            fun_name_to_args = fct.maybe_parse_fun_args(fcr_tc.tool_params)
            # We don't test the actual function call obj outputs
            # Since the parallel function call outputs are a superset of them
            (
                _,
                actual_parallel_function_call_objs,
            ) = fct.parse_function_calls(fcr_tc.raw_response, fun_name_to_args)

            actual_parallel_function_calls = [
                [repr(o) for o in os] for os in actual_parallel_function_call_objs
            ]

            with open(
                join(fcr_tc.dir_path, "actual_parallel_function_calls.json"), "w"
            ) as f:
                json.dump(actual_parallel_function_calls, f, indent=4)
            diff_parallel_function_calls = _compare_eq_any(
                fcr_tc.expected_parallel_function_calls,
                actual_parallel_function_calls,
                verbose=1,
            )
            with open(
                join(fcr_tc.dir_path, "diff_parallel_function_calls.txt"), "w"
            ) as f:
                f.write("\n".join(diff_parallel_function_calls))

            assert (
                fcr_tc.expected_parallel_function_calls
                == actual_parallel_function_calls
            )

        if fcr_tc.expected_tool_calls:
            response = fct.raw_response_to_tool_calls(
                fcr_tc.tool_params, fcr_tc.raw_response
            )
            actual_tool_calls = (
                response
                if response is None
                else [tc.function.model_dump() for tc in response]
            )

            with open(join(fcr_tc.dir_path, "actual_tool_calls.json"), "w") as f:
                json.dump(actual_tool_calls, f, indent=4)
            diff_tool_calls = _compare_eq_any(
                fcr_tc.expected_tool_calls, actual_tool_calls, verbose=1
            )
            with open(join(fcr_tc.dir_path, "diff_tool_calls.txt"), "w") as f:
                f.write("\n".join(diff_tool_calls))

            assert fcr_tc.expected_tool_calls == actual_tool_calls

        if fcr_tc.expected_exception:
            expected_exception = eval(fcr_tc.expected_exception["expected_exception"])
            match = fcr_tc.expected_exception["match"]

            exception = None
            try:
                with raises(expected_exception, match=match) as exc_info:
                    response = fct.raw_response_to_tool_calls(
                        fcr_tc.tool_params, fcr_tc.raw_response
                    )
            except Exception as e:
                exception = e

            actual_exception = exc_info.value.args[0]
            with open(join(fcr_tc.dir_path, "actual_exception.txt"), "w") as f:
                f.write(actual_exception)
            diff_prompt = _compare_eq_any(match, actual_exception, verbose=1)
            with open(join(fcr_tc.dir_path, "diff_exception.txt"), "w") as f:
                f.write("\n".join(diff_prompt))

            if exception is not None:
                raise exception


class TestAsyncCompletions:
    @fixture
    def setup_client(self) -> None:
        environ["NEXUSFLOWAI_API_KEY"] = API_KEY
        self.client = AsyncNexusflowAI(base_url=BASE_URL)

    @pytest.mark.asyncio
    async def test_completions(self, setup_client, monkeypatch):
        client = self.client
        model = MODEL_ID

        post_mock = MagicMock()
        monkeypatch.setattr(AsyncNexusflowAI, "request", post_mock)

        async def async_mock_response():
            return _mock_completions_data(model=model)

        post_mock.return_value = async_mock_response()

        not_given_eq_patch = MagicMock()
        not_given_eq_patch.return_value = True
        monkeypatch.setattr(NotGiven, "__eq__", not_given_eq_patch, raising=False)

        res = await client.completions.create(model=model, prompt="Hello World!")
        assert res.__class__ == NexusflowAICompletion
        assert len(res.choices) == 1

        opts = _final_request_opts()

        stream_type = AsyncStream[NexusflowAICompletion]
        post_mock.assert_called_once_with(
            NexusflowAICompletion,
            opts,
            stream=False,
            stream_cls=stream_type,
        )

    def test_batch_run_prompts(self, setup_client, monkeypatch):
        """
        Test if
        1. The completions create call is called the correct number of times.
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

        # check if the completions create call is called the correct number of times.
        mock_prompts_str = ["dummy prompt 1", "dummy prompt 2"]
        mock_params: CompletionCreateParams = dict(
            {"stream": False, "max_tokens": 10, "temperature": 1.0}
        )

        response = client.completions.batch_run_prompts(
            batch_prompts_str=mock_prompts_str, params=mock_params
        )

        assert len(mock_prompts_str) == len(response)

        # check if the length of batched prompts created is correct
        expected_params_dicts = [
            {
                "stream": False,
                "max_tokens": 10,
                "temperature": 1.0,
                "prompt": "dummy prompt 1",
            },
            {
                "stream": False,
                "max_tokens": 10,
                "temperature": 1.0,
                "prompt": "dummy prompt 2",
            },
        ]

        assert len(mock_prompts_str) == len(mock_create.call_args_list)

        # check if the batched prompts contain the correctly parsed prompts
        actual_params_dicts = [d for _, d in mock_create.call_args_list]
        assert all(d in expected_params_dicts for d in actual_params_dicts)
        assert all(d in actual_params_dicts for d in expected_params_dicts)

        # check if error is raised if stream is set to True
        mock_params: CompletionCreateParams = {"stream": True}

        with pytest.raises(
            ValueError, match="Batch create does not support streaming requests!"
        ):
            response = client.completions.batch_run_prompts(
                batch_prompts_str=mock_prompts_str, params=mock_params
            )
