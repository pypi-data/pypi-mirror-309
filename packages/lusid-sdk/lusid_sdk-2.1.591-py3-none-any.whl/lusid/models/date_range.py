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

from datetime import datetime
from typing import Any, Dict, Optional
from pydantic.v1 import BaseModel, Field

class DateRange(BaseModel):
    """
    DateRange
    """
    from_date: datetime = Field(..., alias="fromDate")
    until_date: Optional[datetime] = Field(None, alias="untilDate")
    __properties = ["fromDate", "untilDate"]

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
    def from_json(cls, json_str: str) -> DateRange:
        """Create an instance of DateRange from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # set to None if until_date (nullable) is None
        # and __fields_set__ contains the field
        if self.until_date is None and "until_date" in self.__fields_set__:
            _dict['untilDate'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> DateRange:
        """Create an instance of DateRange from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return DateRange.parse_obj(obj)

        _obj = DateRange.parse_obj({
            "from_date": obj.get("fromDate"),
            "until_date": obj.get("untilDate")
        })
        return _obj
