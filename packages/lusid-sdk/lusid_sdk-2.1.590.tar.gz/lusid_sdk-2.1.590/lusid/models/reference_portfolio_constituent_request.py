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


from typing import Any, Dict, Optional, Union
from pydantic.v1 import BaseModel, Field, StrictFloat, StrictInt, StrictStr
from lusid.models.perpetual_property import PerpetualProperty

class ReferencePortfolioConstituentRequest(BaseModel):
    """
    ReferencePortfolioConstituentRequest
    """
    instrument_identifiers: Dict[str, StrictStr] = Field(..., alias="instrumentIdentifiers", description="Unique instrument identifiers")
    properties: Optional[Dict[str, PerpetualProperty]] = None
    weight: Union[StrictFloat, StrictInt] = Field(...)
    currency: Optional[StrictStr] = None
    __properties = ["instrumentIdentifiers", "properties", "weight", "currency"]

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
    def from_json(cls, json_str: str) -> ReferencePortfolioConstituentRequest:
        """Create an instance of ReferencePortfolioConstituentRequest from a JSON string"""
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
        # set to None if properties (nullable) is None
        # and __fields_set__ contains the field
        if self.properties is None and "properties" in self.__fields_set__:
            _dict['properties'] = None

        # set to None if currency (nullable) is None
        # and __fields_set__ contains the field
        if self.currency is None and "currency" in self.__fields_set__:
            _dict['currency'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReferencePortfolioConstituentRequest:
        """Create an instance of ReferencePortfolioConstituentRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReferencePortfolioConstituentRequest.parse_obj(obj)

        _obj = ReferencePortfolioConstituentRequest.parse_obj({
            "instrument_identifiers": obj.get("instrumentIdentifiers"),
            "properties": dict(
                (_k, PerpetualProperty.from_dict(_v))
                for _k, _v in obj.get("properties").items()
            )
            if obj.get("properties") is not None
            else None,
            "weight": obj.get("weight"),
            "currency": obj.get("currency")
        })
        return _obj
