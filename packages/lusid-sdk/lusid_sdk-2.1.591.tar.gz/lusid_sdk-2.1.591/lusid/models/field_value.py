# coding: utf-8

"""
    LUSID API

    FINBOURNE Technology  # noqa: E501

    Contact: info@finbourne.com
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""


from __future__ import annotations
import pprint
import re  # noqa: F401
import json


from typing import Any, Dict
from pydantic.v1 import BaseModel, Field, StrictStr, constr, validator

class FieldValue(BaseModel):
    """
    FieldValue
    """
    value: constr(strict=True, max_length=512, min_length=1) = Field(...)
    fields: Dict[str, StrictStr] = Field(...)
    __properties = ["value", "fields"]

    @validator('value')
    def value_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    class Config:
        """Pydantic configuration"""
        allow_population_by_field_name = True
        validate_assignment = True

    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.dict(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> FieldValue:
        """Create an instance of FieldValue from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FieldValue:
        """Create an instance of FieldValue from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FieldValue.parse_obj(obj)

        _obj = FieldValue.parse_obj({
            "value": obj.get("value"),
            "fields": obj.get("fields")
        })
        return _obj
