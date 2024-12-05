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
from pydantic.v1 import BaseModel, Field, StrictFloat, StrictInt
from lusid.models.fee_accrual import FeeAccrual
from lusid.models.fund_amount import FundAmount
from lusid.models.fund_pnl_breakdown import FundPnlBreakdown
from lusid.models.previous_fund_valuation_point_data import PreviousFundValuationPointData

class FundValuationPointData(BaseModel):
    """
    The Valuation Point Data for a Fund on a specified date.  # noqa: E501
    """
    back_out: Dict[str, FundAmount] = Field(..., alias="backOut", description="Bucket of detail for the Valuation Point where data points have been 'backed out'.")
    dealing: Dict[str, FundAmount] = Field(..., description="Bucket of detail for any 'Dealing' that has occured inside the queried period.")
    pn_l: FundPnlBreakdown = Field(..., alias="pnL")
    gav: Union[StrictFloat, StrictInt] = Field(..., description="The Gross Asset Value of the Fund or Share Class at the Valuation Point. This is effectively a summation of all Trial balance entries linked to accounts of types 'Asset' and 'Liabilities'.")
    fees: Dict[str, FeeAccrual] = Field(..., description="Bucket of detail for any 'Fees' that have been charged in the selected period.")
    nav: Union[StrictFloat, StrictInt] = Field(..., description="The Net Asset Value of the Fund or Share Class at the Valuation Point. This represents the GAV with any fees applied in the period.")
    miscellaneous: Optional[Dict[str, FundAmount]] = Field(None, description="Not used directly by the LUSID engines but serves as a holding area for any custom derived data points that may be useful in, for example, fee calculations).")
    previous_valuation_point_data: Optional[PreviousFundValuationPointData] = Field(None, alias="previousValuationPointData")
    __properties = ["backOut", "dealing", "pnL", "gav", "fees", "nav", "miscellaneous", "previousValuationPointData"]

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
    def from_json(cls, json_str: str) -> FundValuationPointData:
        """Create an instance of FundValuationPointData from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in back_out (dict)
        _field_dict = {}
        if self.back_out:
            for _key in self.back_out:
                if self.back_out[_key]:
                    _field_dict[_key] = self.back_out[_key].to_dict()
            _dict['backOut'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in dealing (dict)
        _field_dict = {}
        if self.dealing:
            for _key in self.dealing:
                if self.dealing[_key]:
                    _field_dict[_key] = self.dealing[_key].to_dict()
            _dict['dealing'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of pn_l
        if self.pn_l:
            _dict['pnL'] = self.pn_l.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each value in fees (dict)
        _field_dict = {}
        if self.fees:
            for _key in self.fees:
                if self.fees[_key]:
                    _field_dict[_key] = self.fees[_key].to_dict()
            _dict['fees'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of each value in miscellaneous (dict)
        _field_dict = {}
        if self.miscellaneous:
            for _key in self.miscellaneous:
                if self.miscellaneous[_key]:
                    _field_dict[_key] = self.miscellaneous[_key].to_dict()
            _dict['miscellaneous'] = _field_dict
        # override the default output from pydantic by calling `to_dict()` of previous_valuation_point_data
        if self.previous_valuation_point_data:
            _dict['previousValuationPointData'] = self.previous_valuation_point_data.to_dict()
        # set to None if miscellaneous (nullable) is None
        # and __fields_set__ contains the field
        if self.miscellaneous is None and "miscellaneous" in self.__fields_set__:
            _dict['miscellaneous'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FundValuationPointData:
        """Create an instance of FundValuationPointData from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FundValuationPointData.parse_obj(obj)

        _obj = FundValuationPointData.parse_obj({
            "back_out": dict(
                (_k, FundAmount.from_dict(_v))
                for _k, _v in obj.get("backOut").items()
            )
            if obj.get("backOut") is not None
            else None,
            "dealing": dict(
                (_k, FundAmount.from_dict(_v))
                for _k, _v in obj.get("dealing").items()
            )
            if obj.get("dealing") is not None
            else None,
            "pn_l": FundPnlBreakdown.from_dict(obj.get("pnL")) if obj.get("pnL") is not None else None,
            "gav": obj.get("gav"),
            "fees": dict(
                (_k, FeeAccrual.from_dict(_v))
                for _k, _v in obj.get("fees").items()
            )
            if obj.get("fees") is not None
            else None,
            "nav": obj.get("nav"),
            "miscellaneous": dict(
                (_k, FundAmount.from_dict(_v))
                for _k, _v in obj.get("miscellaneous").items()
            )
            if obj.get("miscellaneous") is not None
            else None,
            "previous_valuation_point_data": PreviousFundValuationPointData.from_dict(obj.get("previousValuationPointData")) if obj.get("previousValuationPointData") is not None else None
        })
        return _obj
