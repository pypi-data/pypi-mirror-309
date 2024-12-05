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


from typing import Any, Dict, List, Optional
from pydantic.v1 import Field, StrictBool, StrictStr, conlist, constr, validator
from lusid.models.lusid_instrument import LusidInstrument
from lusid.models.rounding_convention import RoundingConvention
from lusid.models.schedule import Schedule

class ComplexBond(LusidInstrument):
    """
    LUSID representation of a Complex Bond.  Including Floating, Fixed-to-float, Sinkable, Callable, Puttable, and Mortgage Backed Securities.  # noqa: E501
    """
    identifiers: Optional[Dict[str, StrictStr]] = Field(None, description="External market codes and identifiers for the bond, e.g. ISIN.")
    calculation_type: Optional[constr(strict=True, max_length=50, min_length=0)] = Field(None, alias="calculationType", description="The calculation type applied to the bond coupon amount. This is required for bonds that have a particular type of computing the period coupon, such as simple compounding,  irregular coupons etc.  The default CalculationType is `Standard`, which returns a coupon amount equal to Principal * Coupon Rate / Coupon Frequency. Coupon Frequency is 12M / Payment Frequency.  Payment Frequency can be 1M, 3M, 6M, 12M etc. So Coupon Frequency can be 12, 4, 2, 1 respectively.    Supported string (enumeration) values are: [Standard, DayCountCoupon, NoCalculationFloater, BrazilFixedCoupon, StandardWithCappedAccruedInterest].")
    schedules: Optional[conlist(Schedule)] = Field(None, description="schedules.")
    rounding_conventions: Optional[conlist(RoundingConvention)] = Field(None, alias="roundingConventions", description="Rounding conventions for analytics, if any.")
    asset_backed: Optional[StrictBool] = Field(None, alias="assetBacked", description="If this flag is set to true, then the outstanding notional and principal repayments will be calculated based  on pool factors in the quote store. Usually AssetBacked bonds also require a RollConvention setting of   within the FlowConventions any given rates schedule (to ensure payment dates always happen on the same day  of the month) and US Agency MBSs with Pay Delay features also require their rates schedules to include an  ExDividendConfiguration to drive the lag between interest accrual and payment.")
    asset_pool_identifier: Optional[constr(strict=True, max_length=50, min_length=0)] = Field(None, alias="assetPoolIdentifier", description="Identifier used to retrieve pool factor information about this bond from the quote store. This is typically  the bond's ISIN, but can also be ClientInternal. Please ensure you align the MarketDataKeyRule with the  correct Quote (Quote.ClientInternal.* or Quote.Isin.*)")
    instrument_type: StrictStr = Field(..., alias="instrumentType", description="The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap, SimpleCashFlowLoan, TotalReturnSwap, InflationLeg, FundShareClass, FlexibleLoan, UnsettledCash, Cash, MasteredInstrument, LoanFacility")
    additional_properties: Dict[str, Any] = {}
    __properties = ["instrumentType", "identifiers", "calculationType", "schedules", "roundingConventions", "assetBacked", "assetPoolIdentifier"]

    @validator('instrument_type')
    def instrument_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('QuotedSecurity', 'InterestRateSwap', 'FxForward', 'Future', 'ExoticInstrument', 'FxOption', 'CreditDefaultSwap', 'InterestRateSwaption', 'Bond', 'EquityOption', 'FixedLeg', 'FloatingLeg', 'BespokeCashFlowsLeg', 'Unknown', 'TermDeposit', 'ContractForDifference', 'EquitySwap', 'CashPerpetual', 'CapFloor', 'CashSettled', 'CdsIndex', 'Basket', 'FundingLeg', 'FxSwap', 'ForwardRateAgreement', 'SimpleInstrument', 'Repo', 'Equity', 'ExchangeTradedOption', 'ReferenceInstrument', 'ComplexBond', 'InflationLinkedBond', 'InflationSwap', 'SimpleCashFlowLoan', 'TotalReturnSwap', 'InflationLeg', 'FundShareClass', 'FlexibleLoan', 'UnsettledCash', 'Cash', 'MasteredInstrument', 'LoanFacility'):
            raise ValueError("must be one of enum values ('QuotedSecurity', 'InterestRateSwap', 'FxForward', 'Future', 'ExoticInstrument', 'FxOption', 'CreditDefaultSwap', 'InterestRateSwaption', 'Bond', 'EquityOption', 'FixedLeg', 'FloatingLeg', 'BespokeCashFlowsLeg', 'Unknown', 'TermDeposit', 'ContractForDifference', 'EquitySwap', 'CashPerpetual', 'CapFloor', 'CashSettled', 'CdsIndex', 'Basket', 'FundingLeg', 'FxSwap', 'ForwardRateAgreement', 'SimpleInstrument', 'Repo', 'Equity', 'ExchangeTradedOption', 'ReferenceInstrument', 'ComplexBond', 'InflationLinkedBond', 'InflationSwap', 'SimpleCashFlowLoan', 'TotalReturnSwap', 'InflationLeg', 'FundShareClass', 'FlexibleLoan', 'UnsettledCash', 'Cash', 'MasteredInstrument', 'LoanFacility')")
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
    def from_json(cls, json_str: str) -> ComplexBond:
        """Create an instance of ComplexBond from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in schedules (list)
        _items = []
        if self.schedules:
            for _item in self.schedules:
                if _item:
                    _items.append(_item.to_dict())
            _dict['schedules'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in rounding_conventions (list)
        _items = []
        if self.rounding_conventions:
            for _item in self.rounding_conventions:
                if _item:
                    _items.append(_item.to_dict())
            _dict['roundingConventions'] = _items
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if identifiers (nullable) is None
        # and __fields_set__ contains the field
        if self.identifiers is None and "identifiers" in self.__fields_set__:
            _dict['identifiers'] = None

        # set to None if calculation_type (nullable) is None
        # and __fields_set__ contains the field
        if self.calculation_type is None and "calculation_type" in self.__fields_set__:
            _dict['calculationType'] = None

        # set to None if schedules (nullable) is None
        # and __fields_set__ contains the field
        if self.schedules is None and "schedules" in self.__fields_set__:
            _dict['schedules'] = None

        # set to None if rounding_conventions (nullable) is None
        # and __fields_set__ contains the field
        if self.rounding_conventions is None and "rounding_conventions" in self.__fields_set__:
            _dict['roundingConventions'] = None

        # set to None if asset_backed (nullable) is None
        # and __fields_set__ contains the field
        if self.asset_backed is None and "asset_backed" in self.__fields_set__:
            _dict['assetBacked'] = None

        # set to None if asset_pool_identifier (nullable) is None
        # and __fields_set__ contains the field
        if self.asset_pool_identifier is None and "asset_pool_identifier" in self.__fields_set__:
            _dict['assetPoolIdentifier'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ComplexBond:
        """Create an instance of ComplexBond from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ComplexBond.parse_obj(obj)

        _obj = ComplexBond.parse_obj({
            "instrument_type": obj.get("instrumentType"),
            "identifiers": obj.get("identifiers"),
            "calculation_type": obj.get("calculationType"),
            "schedules": [Schedule.from_dict(_item) for _item in obj.get("schedules")] if obj.get("schedules") is not None else None,
            "rounding_conventions": [RoundingConvention.from_dict(_item) for _item in obj.get("roundingConventions")] if obj.get("roundingConventions") is not None else None,
            "asset_backed": obj.get("assetBacked"),
            "asset_pool_identifier": obj.get("assetPoolIdentifier")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
