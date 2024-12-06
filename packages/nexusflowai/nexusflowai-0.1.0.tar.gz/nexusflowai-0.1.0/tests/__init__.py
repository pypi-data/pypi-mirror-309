import nexusflowai

import json

from os import getenv

from pytest import mark

from tests.utils import BASE_URL, API_KEY, MODEL_ID


def skip_unless_full(fn):
    full: bool = json.loads(getenv("FULL", "false"))
    return fn if full else mark.skip("Skipping test in slim execution")(fn)
