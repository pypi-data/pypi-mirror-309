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
from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictStr, conlist, constr, validator
from lusid.models.model_property import ModelProperty

class ClosePeriodDiaryEntryRequest(BaseModel):
    """
    A definition for the period you wish to close  # noqa: E501
    """
    diary_entry_code: Optional[constr(strict=True, max_length=64, min_length=1)] = Field(None, alias="diaryEntryCode", description="Unique code assigned to a period. When left blank a code will be created by the system in the format 'yyyyMMDD'.")
    name: Optional[constr(strict=True, max_length=512, min_length=1)] = Field(None, description="Identifiable Name assigned to the period. Where left blank, the system will generate a name in the format 'yyyyMMDD'.")
    effective_at: Optional[datetime] = Field(None, alias="effectiveAt", description="The effective time of the diary entry.")
    query_as_at: Optional[datetime] = Field(None, alias="queryAsAt", description="The query time of the diary entry. Defaults to latest.")
    status: Optional[StrictStr] = Field(None, description="The status of a Diary Entry of Type 'PeriodBoundary'. Defaults to 'Estimate' when closing a period, and supports 'Estimate' and 'Final' for closing periods and 'Final' for locking periods.")
    properties: Optional[Dict[str, ModelProperty]] = Field(None, description="A set of properties for the diary entry.")
    closing_options: Optional[conlist(StrictStr)] = Field(None, alias="closingOptions", description="The options which will be executed once a period is closed or locked.")
    __properties = ["diaryEntryCode", "name", "effectiveAt", "queryAsAt", "status", "properties", "closingOptions"]

    @validator('diary_entry_code')
    def diary_entry_code_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

        if not re.match(r"^[a-zA-Z0-9\-_]+$", value):
            raise ValueError(r"must validate the regular expression /^[a-zA-Z0-9\-_]+$/")
        return value

    @validator('name')
    def name_validate_regular_expression(cls, value):
        """Validates the regular expression"""
        if value is None:
            return value

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
    def from_json(cls, json_str: str) -> ClosePeriodDiaryEntryRequest:
        """Create an instance of ClosePeriodDiaryEntryRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in properties (dict)
        _field_dict = {}
        if self.properties:
            for _key in self.properties:
                if self.properties[_key]:
                    _field_dict[_key] = self.properties[_key].to_dict()
            _dict['properties'] = _field_dict
        # set to None if diary_entry_code (nullable) is None
        # and __fields_set__ contains the field
        if self.diary_entry_code is None and "diary_entry_code" in self.__fields_set__:
            _dict['diaryEntryCode'] = None

        # set to None if name (nullable) is None
        # and __fields_set__ contains the field
        if self.name is None and "name" in self.__fields_set__:
            _dict['name'] = None

        # set to None if effective_at (nullable) is None
        # and __fields_set__ contains the field
        if self.effective_at is None and "effective_at" in self.__fields_set__:
            _dict['effectiveAt'] = None

        # set to None if query_as_at (nullable) is None
        # and __fields_set__ contains the field
        if self.query_as_at is None and "query_as_at" in self.__fields_set__:
            _dict['queryAsAt'] = None

        # set to None if status (nullable) is None
        # and __fields_set__ contains the field
        if self.status is None and "status" in self.__fields_set__:
            _dict['status'] = None

        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if closing_options (nullable) is None
        # and __fields_set__ contains the field
        if self.closing_options is None and "closing_options" in self.__fields_set__:
            _dict['closingOptions'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ClosePeriodDiaryEntryRequest:
        """Create an instance of ClosePeriodDiaryEntryRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ClosePeriodDiaryEntryRequest.parse_obj(obj)

        _obj = ClosePeriodDiaryEntryRequest.parse_obj({
            "diary_entry_code": obj.get("diaryEntryCode"),
            "name": obj.get("name"),
            "effective_at": obj.get("effectiveAt"),
            "query_as_at": obj.get("queryAsAt"),
            "status": obj.get("status"),
            "properties": dict(
                (_k, ModelProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "closing_options": obj.get("closingOptions")
        })
        return _obj
