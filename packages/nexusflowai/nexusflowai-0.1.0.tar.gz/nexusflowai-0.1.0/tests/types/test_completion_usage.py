from io import BytesIO

from base64 import b64encode, b64decode

from nexusflowai.types import NexusflowAIChatCompletion, NexusflowAICompletion

from tests import skip_unless_full

from pytest import approx


class TestCompletionUsageUnit:
    def test_completions_sanity(self) -> None:
        json_with_only_tokens_usage = {
            "id": "nf_completion_a64e80ff-fad2-4408-aa2c-6865600e265b",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "logprobs": None,
                    "text": "get_weather(city_name=None)",
                    "message": {
                        "content": "get_weather(city_name=None)",
                        "role": "assistant",
                        "function_call": None,
                        "tool_calls": [
                            {
                                "id": "call_032486bb-e826-4963-98dc-c3017937dc0c",
                                "function": {
                                    "arguments": '{"city_name": null}',
                                    "name": "get_weather",
                                },
                                "type": "function",
                            }
                        ],
                        "parsed": None,
                    },
                }
            ],
            "created": 1727246053,
            "model": "nexus-tool-use-20240816",
            "object": "text_completion",
            "system_fingerprint": "2.0.5-dev0-sha-d32e33b",
            "usage": {
                "completion_tokens": 7,
                "prompt_tokens": 25,
                "total_tokens": 32,
            },
        }
        c = NexusflowAICompletion.model_validate(json_with_only_tokens_usage)
        expected_total_tokens = 32
        actual_total_tokens = c.usage.total_tokens
        assert expected_total_tokens == actual_total_tokens
        expected_latency = None
        actual_latency = c.usage.latency
        assert expected_latency == actual_latency

        json_with_extra_latency = {
            "id": "nf_completion_a64e80ff-fad2-4408-aa2c-6865600e265b",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "logprobs": None,
                    "text": "get_weather(city_name=None)",
                    "message": {
                        "content": "get_weather(city_name=None)",
                        "role": "assistant",
                        "function_call": None,
                        "tool_calls": [
                            {
                                "id": "call_032486bb-e826-4963-98dc-c3017937dc0c",
                                "function": {
                                    "arguments": '{"city_name": null}',
                                    "name": "get_weather",
                                },
                                "type": "function",
                            }
                        ],
                        "parsed": None,
                    },
                }
            ],
            "created": 1727246053,
            "model": "nexus-tool-use-20240816",
            "object": "text_completion",
            "system_fingerprint": "2.0.5-dev0-sha-d32e33b",
            "usage": {
                "completion_tokens": 7,
                "prompt_tokens": 25,
                "total_tokens": 32,
                "latency": 123.234,
            },
        }
        c = NexusflowAICompletion.model_validate(json_with_extra_latency)
        expected_total_tokens = 32
        actual_total_tokens = c.usage.total_tokens
        assert expected_total_tokens == actual_total_tokens
        expected_latency = 123.234
        actual_latency = c.usage.latency
        assert approx(expected_latency) == actual_latency
        expected_time_to_first_token = None
        actual_time_to_first_token = c.usage.time_to_first_token
        assert expected_time_to_first_token == actual_time_to_first_token

        json_with_extra_latency = {
            "id": "nf_completion_a64e80ff-fad2-4408-aa2c-6865600e265b",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "logprobs": None,
                    "text": "get_weather(city_name=None)",
                    "message": {
                        "content": "get_weather(city_name=None)",
                        "role": "assistant",
                        "function_call": None,
                        "tool_calls": [
                            {
                                "id": "call_032486bb-e826-4963-98dc-c3017937dc0c",
                                "function": {
                                    "arguments": '{"city_name": null}',
                                    "name": "get_weather",
                                },
                                "type": "function",
                            }
                        ],
                        "parsed": None,
                    },
                }
            ],
            "created": 1727246053,
            "model": "nexus-tool-use-20240816",
            "object": "text_completion",
            "system_fingerprint": "2.0.5-dev0-sha-d32e33b",
            "usage": {
                "completion_tokens": 7,
                "prompt_tokens": 25,
                "total_tokens": 32,
                "latency": 123.234,
                "time_to_first_token": 47.8834,
                "output_tokens_per_sec": 57.44444,
            },
        }
        c = NexusflowAICompletion.model_validate(json_with_extra_latency)
        expected_total_tokens = 32
        actual_total_tokens = c.usage.total_tokens
        assert expected_total_tokens == actual_total_tokens
        expected_latency = 123.234
        actual_latency = c.usage.latency
        assert approx(expected_latency) == actual_latency
        expected_time_to_first_token = 47.8834
        actual_time_to_first_token = c.usage.time_to_first_token
        assert approx(expected_time_to_first_token) == actual_time_to_first_token
        expected_output_tokens_per_sec = 57.44444
        actual_output_tokens_per_sec = c.usage.output_tokens_per_sec
        assert approx(expected_output_tokens_per_sec) == actual_output_tokens_per_sec

    def test_chat_completions_sanity(self) -> None:
        json_with_only_tokens_usage = {
            "id": "chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "message": {
                        "content": None,
                        "role": "assistant",
                        "tool_calls": [],
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
        cc = NexusflowAIChatCompletion.model_validate(json_with_only_tokens_usage)
        expected_total_tokens = 103
        actual_total_tokens = cc.usage.total_tokens
        assert expected_total_tokens == actual_total_tokens
        expected_latency = None
        actual_latency = cc.usage.latency
        assert expected_latency == actual_latency

        json_with_extra_latency = {
            "id": "chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "message": {
                        "content": None,
                        "role": "assistant",
                        "tool_calls": [],
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
                "latency": 123.234,
            },
            "hints": None,
        }
        cc = NexusflowAIChatCompletion.model_validate(json_with_extra_latency)
        expected_latency = 123.234
        actual_latency = cc.usage.latency
        assert approx(expected_latency) == actual_latency
        expected_time_to_first_token = None
        actual_time_to_first_token = cc.usage.time_to_first_token
        assert expected_time_to_first_token == actual_time_to_first_token

        json_with_extra_everything = {
            "id": "chatcmpl-9u0mJeNHHBxKkcLFgtsqu8KsFZwJ8",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "message": {
                        "content": None,
                        "role": "assistant",
                        "tool_calls": [],
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
                "latency": 123.234,
                "time_to_first_token": 47.8834,
                "output_tokens_per_sec": 57.44444,
            },
            "hints": None,
        }
        cc = NexusflowAIChatCompletion.model_validate(json_with_extra_everything)
        expected_latency = 123.234
        actual_latency = cc.usage.latency
        assert approx(expected_latency) == actual_latency
        expected_time_to_first_token = 47.8834
        actual_time_to_first_token = cc.usage.time_to_first_token
        assert approx(expected_time_to_first_token) == actual_time_to_first_token
        expected_output_tokens_per_sec = 57.44444
        actual_output_tokens_per_sec = cc.usage.output_tokens_per_sec
        assert approx(expected_output_tokens_per_sec) == actual_output_tokens_per_sec

        json_with_extra_execution_results = {
            "id": "nf_completion_a64e80ff-fad2-4408-aa2c-6865600e265b",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "logprobs": None,
                    "text": "get_text(text=None); get_image(image=None)",
                    "message": {
                        "content": "get_text(text=None); get_image(image=None)",
                        "role": "assistant",
                        "function_call": None,
                        "tool_calls": [
                            {
                                "id": "call_032486bb-e826-4963-98dc-c3017937dc0c",
                                "function": {
                                    "arguments": '{"text": null}',
                                    "name": "get_text",
                                },
                                "type": "function",
                                "execution_result": {
                                    "text": "execution_text",
                                    "type": "text",
                                },
                            },
                            {
                                "id": "call_032486bb-e826-4963-98dc-c3017937dc0d",
                                "function": {
                                    "arguments": '{"image": null}',
                                    "name": "get_image",
                                },
                                "type": "function",
                                "execution_result": {
                                    "image_bytes": "abcd",
                                    "type": "image_bytes",
                                },
                            },
                        ],
                        "parsed": None,
                    },
                }
            ],
            "created": 1727246053,
            "model": "nexus-tool-use-20240816",
            "object": "chat.completion",
            "system_fingerprint": "2.0.5-dev0-sha-d32e33b",
            "usage": {
                "completion_tokens": 7,
                "prompt_tokens": 25,
                "total_tokens": 32,
                "latency": 123.234,
                "time_to_first_token": 47.8834,
                "output_tokens_per_sec": 57.44444,
            },
        }
        c = NexusflowAIChatCompletion.model_validate(json_with_extra_execution_results)
        assert (
            c.choices[0].message.tool_calls[0].execution_result["text"]
            == "execution_text"
        )
        assert (
            c.choices[0].message.tool_calls[1].execution_result["image_bytes"] == "abcd"
        )


@skip_unless_full
class TestCompletionUsageE2E:
    def test_image_bytes(self):
        # get image
        with open("tests/types/test_image.png", "rb") as f:
            im_bytes = f.read()
            encoded_im = b64encode(im_bytes).decode("utf-8")

        json_with_extra_execution_results = {
            "id": "nf_completion_a64e80ff-fad2-4408-aa2c-6865600e265b",
            "choices": [
                {
                    "finish_reason": "tool_calls",
                    "index": 0,
                    "logprobs": None,
                    "text": "get_image(image=None)",
                    "message": {
                        "content": "get_image(image=None)",
                        "role": "assistant",
                        "function_call": None,
                        "tool_calls": [
                            {
                                "id": "call_032486bb-e826-4963-98dc-c3017937dc0d",
                                "function": {
                                    "arguments": '{"image": null}',
                                    "name": "get_image",
                                },
                                "type": "function",
                                "execution_result": {
                                    "image_bytes": encoded_im,
                                    "type": "image_bytes",
                                },
                            },
                        ],
                        "parsed": None,
                    },
                }
            ],
            "created": 1727246053,
            "model": "nexus-tool-use-20240816",
            "object": "chat.completion",
            "system_fingerprint": "2.0.5-dev0-sha-d32e33b",
            "usage": {
                "completion_tokens": 7,
                "prompt_tokens": 25,
                "total_tokens": 32,
            },
        }
        c = NexusflowAIChatCompletion.model_validate(json_with_extra_execution_results)
        retrieved_encoded_im = (
            c.choices[0].message.tool_calls[0].execution_result["image_bytes"]
        )
        retrieved_decoded_im = b64decode(retrieved_encoded_im)
        assert retrieved_decoded_im == im_bytes
