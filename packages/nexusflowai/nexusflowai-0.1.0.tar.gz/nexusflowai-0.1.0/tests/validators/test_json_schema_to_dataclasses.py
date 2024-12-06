from typing import Optional

from pydantic import BaseModel, EmailStr, Field

from nexusflowai.validators.json_schema_to_dataclasses import (
    json_schema_to_dataclasses,
    try_convert_to_dataclasses_str,
)


class TestJsonSchemaToDataclassesUnit:
    def test_sanity(self) -> None:
        json_schema = """
{
  "title": "Person",
  "type": "object",
  "properties": {
    "name": {
      "type": "string"
    },
    "age": {
      "type": "integer"
    },
    "email": {
      "type": "string",
      "format": "email"
    }
  },
  "required": ["name", "age"]
}
"""

        expected_output = """@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
"""
        actual_output = json_schema_to_dataclasses(json_schema)
        assert expected_output == actual_output

    def test_try_convert(self) -> None:
        expected_output = """@dataclass
class Person:
    name: str
    age: int
    email: Optional[str] = None
"""

        class Person(BaseModel):
            name: str
            age: int
            email: Optional[EmailStr] = None

        actual_output = try_convert_to_dataclasses_str(Person)[1]
        assert expected_output == actual_output

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
        actual_output = try_convert_to_dataclasses_str(input_json_schema_dict)[1]
        assert expected_output == actual_output

    def test_sanity_failure_cases(self) -> None:
        expected_output = None

        invalid_json_schema = 2
        actual_output = try_convert_to_dataclasses_str(invalid_json_schema)[1]
        assert expected_output == actual_output

    def test_with_descriptions(self) -> None:
        class GasDistributionNetwork(BaseModel):
            networkIDStr: str = Field(
                description="Prefix of the identifier for the gas distribution network. Does not contain the networkIDInt.",
                title="Network ID Str",
            )
            networkIDInt: int = Field(
                description="Int suffix of the identifier for the gas distribution network.",
                title="Network ID Int",
            )
            pipelineLength: float = Field(
                description="The total length of the pipeline in kilometers.",
                title="Pipeline Length",
            )
            capacity: float = Field(
                description="The maximum amount of gas that can be distributed in cubic meters per day.",
                title="Capacity",
            )
            maintenanceSchedule: str = Field(
                description="The schedule detailing when maintenance activities are to be performed.",
                title="Maintenance Schedule",
            )

        expected_output = """@dataclass
class GasDistributionNetwork:
    networkIDStr: str
    \"\"\"
    Prefix of the identifier for the gas distribution network. Does not contain the networkIDInt.
    \"\"\"
    networkIDInt: int
    \"\"\"
    Int suffix of the identifier for the gas distribution network.
    \"\"\"
    pipelineLength: float
    \"\"\"
    The total length of the pipeline in kilometers.
    \"\"\"
    capacity: float
    \"\"\"
    The maximum amount of gas that can be distributed in cubic meters per day.
    \"\"\"
    maintenanceSchedule: str
    \"\"\"
    The schedule detailing when maintenance activities are to be performed.
    \"\"\"
"""
        _, actual_output = try_convert_to_dataclasses_str(GasDistributionNetwork)
        assert expected_output == actual_output
