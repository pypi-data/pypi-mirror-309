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
from pydantic.v1 import BaseModel, Field
from lusid.models.resource_id import ResourceId

class OrderGraphBlockExecutionDetail(BaseModel):
    """
    OrderGraphBlockExecutionDetail
    """
    id: ResourceId = Field(...)
    __properties = ["id"]

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
    def from_json(cls, json_str: str) -> OrderGraphBlockExecutionDetail:
        """Create an instance of OrderGraphBlockExecutionDetail from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of id
        if self.id:
            _dict['id'] = self.id.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> OrderGraphBlockExecutionDetail:
        """Create an instance of OrderGraphBlockExecutionDetail from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return OrderGraphBlockExecutionDetail.parse_obj(obj)

        _obj = OrderGraphBlockExecutionDetail.parse_obj({
            "id": ResourceId.from_dict(obj.get("id")) if obj.get("id") is not None else None
        })
        return _obj
