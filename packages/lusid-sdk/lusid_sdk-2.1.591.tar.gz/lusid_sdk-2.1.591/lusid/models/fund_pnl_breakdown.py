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
from lusid.models.fund_amount import FundAmount

class FundPnlBreakdown(BaseModel):
    """
    The breakdown of PnL for a Fund on a specified date.  # noqa: E501
    """
    non_class_specific_pnl: Dict[str, FundAmount] = Field(..., alias="nonClassSpecificPnl", description="Bucket of detail for PnL within the queried period that is not specific to any share class.")
    aggregated_class_pnl: Dict[str, FundAmount] = Field(..., alias="aggregatedClassPnl", description="Bucket of detail for the sum of class PnL across all share classes in a fund and within the queried period.")
    total_pnl: Dict[str, FundAmount] = Field(..., alias="totalPnl", description="Bucket of detail for the sum of class PnL and PnL not specific to a class within the queried period.")
    __properties = ["nonClassSpecificPnl", "aggregatedClassPnl", "totalPnl"]

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
    def from_json(cls, json_str: str) -> FundPnlBreakdown:
        """Create an instance of FundPnlBreakdown from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in non_class_specific_pnl (dict)
        _field_dict = {}
        if self.non_class_specific_pnl:
            for _key in self.non_class_specific_pnl:
                if self.non_class_specific_pnl[_key]:
                    _field_dict[_key] = self.non_class_specific_pnl[_key].to_dict()
            _dict['nonClassSpecificPnl'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in aggregated_class_pnl (dict)
        _field_dict = {}
        if self.aggregated_class_pnl:
            for _key in self.aggregated_class_pnl:
                if self.aggregated_class_pnl[_key]:
                    _field_dict[_key] = self.aggregated_class_pnl[_key].to_dict()
            _dict['aggregatedClassPnl'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in total_pnl (dict)
        _field_dict = {}
        if self.total_pnl:
            for _key in self.total_pnl:
                if self.total_pnl[_key]:
                    _field_dict[_key] = self.total_pnl[_key].to_dict()
            _dict['totalPnl'] = _field_dict
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FundPnlBreakdown:
        """Create an instance of FundPnlBreakdown from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FundPnlBreakdown.parse_obj(obj)

        _obj = FundPnlBreakdown.parse_obj({
            "non_class_specific_pnl": dict(
                (_k, FundAmount.from_dict(_v))
                for _k, _v in obj.get("nonClassSpecificPnl").items()
            )
            if obj.get("nonClassSpecificPnl") is not None
            else None,
            "aggregated_class_pnl": dict(
                (_k, FundAmount.from_dict(_v))
                for _k, _v in obj.get("aggregatedClassPnl").items()
            )
            if obj.get("aggregatedClassPnl") is not None
            else None,
            "total_pnl": dict(
                (_k, FundAmount.from_dict(_v))
                for _k, _v in obj.get("totalPnl").items()
            )
            if obj.get("totalPnl") is not None
            else None
        })
        return _obj
