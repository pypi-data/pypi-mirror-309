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
from pydantic.v1 import BaseModel, Field, constr, validator

class UpdateRelationshipDefinitionRequest(BaseModel):
    """
    UpdateRelationshipDefinitionRequest
    """
    display_name: constr(strict=True, max_length=512, min_length=1) = Field(..., alias="displayName", description="The display name of the relation.")
    outward_description: constr(strict=True, max_length=512, min_length=1) = Field(..., alias="outwardDescription", description="The description to relate source entity object and target entity object.")
    inward_description: constr(strict=True, max_length=512, min_length=1) = Field(..., alias="inwardDescription", description="The description to relate target entity object and source entity object.")
    __properties = ["displayName", "outwardDescription", "inwardDescription"]

    @validator('display_name')
    def display_name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('outward_description')
    def outward_description_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if not re.match(r"^[\s\S]*$", value):
            raise ValueError(r"must validate the regular expression /^[\s\S]*$/")
        return value

    @validator('inward_description')
    def inward_description_validate_regular_expression(cls, value):
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
    def from_json(cls, json_str: str) -> UpdateRelationshipDefinitionRequest:
        """Create an instance of UpdateRelationshipDefinitionRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> UpdateRelationshipDefinitionRequest:
        """Create an instance of UpdateRelationshipDefinitionRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return UpdateRelationshipDefinitionRequest.parse_obj(obj)

        _obj = UpdateRelationshipDefinitionRequest.parse_obj({
            "display_name": obj.get("displayName"),
            "outward_description": obj.get("outwardDescription"),
            "inward_description": obj.get("inwardDescription")
        })
        return _obj
