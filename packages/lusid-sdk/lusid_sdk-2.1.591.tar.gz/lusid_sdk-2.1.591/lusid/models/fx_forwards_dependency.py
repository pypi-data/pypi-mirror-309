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
from typing import Any, Dict
from pydantic.v1 import Field, StrictStr, constr, validator
from lusid.models.economic_dependency import EconomicDependency

class FxForwardsDependency(EconomicDependency):
    """
    Indicates a dependency on an FxForwardCurve.  Identical to Fx dependencies in the meaning of domestic and foreign currencies, but describes a *set* of fx rates.  These rates are quoted rates for fx forwards, which can be used to interpolate the forward rate at a specific time in the future.  In the case of pips, the absolute rates can be expressed as rate = spotFx + pips / pipsPerUnit  # noqa: E501
    """
    domestic_currency: StrictStr = Field(..., alias="domesticCurrency", description="DomesticCurrency is the first currency in a currency pair quote e.g. eur-gbp, eur is the domestic currency.")
    foreign_currency: StrictStr = Field(..., alias="foreignCurrency", description="ForeignCurrency is the second currency in a currency pair quote e.g. eur-gbp, gbp is the foreign currency.")
    curve_type: constr(strict=True, max_length=50, min_length=0) = Field(..., alias="curveType", description="Used to describe the format in which the curve is expressed  e.g. FxFwdCurve (general term to describe any representation), TenorFxFwdCurve, PipsFxFwdCurve.")
    var_date: datetime = Field(..., alias="date", description="The effectiveDate of the entity that this is a dependency for.  Unless there is an obvious date this should be, like for a historic reset, then this is the valuation date.")
    dependency_type: StrictStr = Field(..., alias="dependencyType", description="The available values are: OpaqueDependency, CashDependency, DiscountingDependency, EquityCurveDependency, EquityVolDependency, FxDependency, FxForwardsDependency, FxVolDependency, IndexProjectionDependency, IrVolDependency, QuoteDependency, Vendor, CalendarDependency, InflationFixingDependency")
    additional_properties: Dict[str, Any] = {}
    __properties = ["dependencyType", "domesticCurrency", "foreignCurrency", "curveType", "date"]

    @validator('dependency_type')
    def dependency_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('OpaqueDependency', 'CashDependency', 'DiscountingDependency', 'EquityCurveDependency', 'EquityVolDependency', 'FxDependency', 'FxForwardsDependency', 'FxVolDependency', 'IndexProjectionDependency', 'IrVolDependency', 'QuoteDependency', 'Vendor', 'CalendarDependency', 'InflationFixingDependency'):
            raise ValueError("must be one of enum values ('OpaqueDependency', 'CashDependency', 'DiscountingDependency', 'EquityCurveDependency', 'EquityVolDependency', 'FxDependency', 'FxForwardsDependency', 'FxVolDependency', 'IndexProjectionDependency', 'IrVolDependency', 'QuoteDependency', 'Vendor', 'CalendarDependency', 'InflationFixingDependency')")
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
    def from_json(cls, json_str: str) -> FxForwardsDependency:
        """Create an instance of FxForwardsDependency from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> FxForwardsDependency:
        """Create an instance of FxForwardsDependency from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return FxForwardsDependency.parse_obj(obj)

        _obj = FxForwardsDependency.parse_obj({
            "dependency_type": obj.get("dependencyType"),
            "domestic_currency": obj.get("domesticCurrency"),
            "foreign_currency": obj.get("foreignCurrency"),
            "curve_type": obj.get("curveType"),
            "var_date": obj.get("date")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
