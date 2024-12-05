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
from typing import Any, Dict, Optional, Union
from pydantic.v1 import Field, StrictFloat, StrictInt, StrictStr, constr, validator
from lusid.models.futures_contract_details import FuturesContractDetails
from lusid.models.lusid_instrument import LusidInstrument

class Future(LusidInstrument):
    """
    LUSID representation of a Future.  Including, but not limited to, Equity Futures, Bond Futures, Index Futures, Currency Futures, and Interest Rate Futures.  # noqa: E501
    """
    start_date: datetime = Field(..., alias="startDate", description="The start date of the instrument. This is normally synonymous with the trade-date.")
    maturity_date: datetime = Field(..., alias="maturityDate", description="The final maturity date of the instrument. This means the last date on which the instruments makes a payment of any amount.  For the avoidance of doubt, that is not necessarily prior to its last sensitivity date for the purposes of risk; e.g. instruments such as  Constant Maturity Swaps (CMS) often have sensitivities to rates that may well be observed or set prior to the maturity date, but refer to a termination date beyond it.")
    identifiers: Dict[str, StrictStr] = Field(..., description="External market codes and identifiers for the bond, e.g. ISIN.")
    contract_details: FuturesContractDetails = Field(..., alias="contractDetails")
    contracts: Optional[Union[StrictFloat, StrictInt]] = Field(None, description="The number of contracts held.")
    ref_spot_price: Optional[Union[StrictFloat, StrictInt]] = Field(None, alias="refSpotPrice", description="The reference spot price for the future at which the contract was entered into.")
    underlying: Optional[LusidInstrument] = None
    calculation_type: Optional[constr(strict=True, max_length=32, min_length=0)] = Field(None, alias="calculationType", description="Calculation type for some Future instruments which have non-standard methodology.  Optional, if not set defaults as follows:  - If ExchangeCode is \"ASX\" and ContractCode is \"IR\" or \"BB\" set to ASX_BankBills  - If ExchangeCode is \"ASX\" and ContractCode is \"YT\" set to ASX_3Year  - If ExchangeCode is \"ASX\" and ContractCode is \"VT\" set to ASX_5Year  - If ExchangeCode is \"ASX\" and ContractCode is \"XT\" set to ASX_10Year  - If ExchangeCode is \"ASX\" and ContractCode is \"LT\" set to ASX_20Year  - otherwise set to Standard    Specific calculation types for bond and interest rate futures are:  - [Standard] The default calculation type, which does not fit into any of the categories below.  - [ASX_BankBills] Used for AUD and NZD futures “IR” and “BB” on ASX. 90D Bank Bills.  - [ASX_3Year] Used for “YT” on ASX. 3YR semi-annual bond (6 coupons) @ 6%.  - [ASX_5Year] Used for “VT” on ASX. 5yr semi-annual bond (10 coupons) @ 2%.  - [ASX_10Year] Used for “XT” on ASX. 10yr semi-annual bond (20 coupons) @ 6%.  - [ASX_20Year] Used for “LT” on ASX. 20yr semi-annual bond (40 coupons) @ 4%.  - [B3_DI1] Used for “DI1” on B3. Average of 1D interbank deposit rates.    - For futures with this calculation type, quote values are expected to be specified as a percentage.      For example, a quoted rate of 13.205% should be specified as a quote of 13.205 with a face value of 100.    Supported string (enumeration) values are: [Standard, ASX_BankBills, ASX_3Year, ASX_5Year, ASX_10Year, ASX_20Year, B3_DI1].")
    instrument_type: StrictStr = Field(..., alias="instrumentType", description="The available values are: QuotedSecurity, InterestRateSwap, FxForward, Future, ExoticInstrument, FxOption, CreditDefaultSwap, InterestRateSwaption, Bond, EquityOption, FixedLeg, FloatingLeg, BespokeCashFlowsLeg, Unknown, TermDeposit, ContractForDifference, EquitySwap, CashPerpetual, CapFloor, CashSettled, CdsIndex, Basket, FundingLeg, FxSwap, ForwardRateAgreement, SimpleInstrument, Repo, Equity, ExchangeTradedOption, ReferenceInstrument, ComplexBond, InflationLinkedBond, InflationSwap, SimpleCashFlowLoan, TotalReturnSwap, InflationLeg, FundShareClass, FlexibleLoan, UnsettledCash, Cash, MasteredInstrument, LoanFacility")
    additional_properties: Dict[str, Any] = {}
    __properties = ["instrumentType", "startDate", "maturityDate", "identifiers", "contractDetails", "contracts", "refSpotPrice", "underlying", "calculationType"]

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
    def from_json(cls, json_str: str) -> Future:
        """Create an instance of Future from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of contract_details
        if self.contract_details:
            _dict['contractDetails'] = self.contract_details.to_dict()
        # override the default output from pydantic by calling `to_dict()` of underlying
        if self.underlying:
            _dict['underlying'] = self.underlying.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if calculation_type (nullable) is None
        # and __fields_set__ contains the field
        if self.calculation_type is None and "calculation_type" in self.__fields_set__:
            _dict['calculationType'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> Future:
        """Create an instance of Future from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return Future.parse_obj(obj)

        _obj = Future.parse_obj({
            "instrument_type": obj.get("instrumentType"),
            "start_date": obj.get("startDate"),
            "maturity_date": obj.get("maturityDate"),
            "identifiers": obj.get("identifiers"),
            "contract_details": FuturesContractDetails.from_dict(obj.get("contractDetails")) if obj.get("contractDetails") is not None else None,
            "contracts": obj.get("contracts"),
            "ref_spot_price": obj.get("refSpotPrice"),
            "underlying": LusidInstrument.from_dict(obj.get("underlying")) if obj.get("underlying") is not None else None,
            "calculation_type": obj.get("calculationType")
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
