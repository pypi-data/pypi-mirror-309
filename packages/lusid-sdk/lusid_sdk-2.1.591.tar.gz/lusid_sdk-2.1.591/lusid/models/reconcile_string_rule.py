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
from pydantic.v1 import Field, StrictStr, conlist, validator
from lusid.models.aggregate_spec import AggregateSpec
from lusid.models.reconciliation_rule import ReconciliationRule

class ReconcileStringRule(ReconciliationRule):
    """
    Comparison of string values  # noqa: E501
    """
    comparison_type: StrictStr = Field(..., alias="comparisonType", description="The available values are: Exact, Contains, CaseInsensitive, ContainsAnyCase, IsOneOf")
    one_of_candidates: Optional[Dict[str, conlist(StrictStr)]] = Field(None, alias="oneOfCandidates", description="For cases of \"IsOneOf\" a set is required to match values against.  Fuzzy matching of strings against one of a set. There can be cases where systems \"A\" and \"B\" might use different terms for the same logical entity. A common case would be  comparison of something like a day count fraction where some convention like the \"actual 365\" convention might be represented as one of [\"A365\", \"Act365\", \"Actual365\"] or similar.  This is to allow this kind of fuzzy matching of values. Note that as this is exhaustive comparison across sets it will be slow and should therefore be used sparingly.")
    applies_to: AggregateSpec = Field(..., alias="appliesTo")
    rule_type: StrictStr = Field(..., alias="ruleType", description="The available values are: ReconcileNumericRule, ReconcileDateTimeRule, ReconcileStringRule, ReconcileExact")
    additional_properties: Dict[str, Any] = {}
    __properties = ["ruleType", "comparisonType", "oneOfCandidates", "appliesTo"]

    @validator('comparison_type')
    def comparison_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('Exact', 'Contains', 'CaseInsensitive', 'ContainsAnyCase', 'IsOneOf'):
            raise ValueError("must be one of enum values ('Exact', 'Contains', 'CaseInsensitive', 'ContainsAnyCase', 'IsOneOf')")
        return value

    @validator('rule_type')
    def rule_type_validate_enum(cls, value):
        """Validates the enum"""
        if value not in ('ReconcileNumericRule', 'ReconcileDateTimeRule', 'ReconcileStringRule', 'ReconcileExact'):
            raise ValueError("must be one of enum values ('ReconcileNumericRule', 'ReconcileDateTimeRule', 'ReconcileStringRule', 'ReconcileExact')")
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
    def from_json(cls, json_str: str) -> ReconcileStringRule:
        """Create an instance of ReconcileStringRule from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                            "additional_properties"
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each value in one_of_candidates (dict of array)
        _field_dict_of_array = {}
        if self.one_of_candidates:
            for _key in self.one_of_candidates:
                if self.one_of_candidates[_key]:
                    _field_dict_of_array[_key] = [
                        _item.to_dict() for _item in self.one_of_candidates[_key]
                    ]
            _dict['oneOfCandidates'] = _field_dict_of_array
        # override the default output from pydantic by calling `to_dict()` of applies_to
        if self.applies_to:
            _dict['appliesTo'] = self.applies_to.to_dict()
        # puts key-value pairs in additional_properties in the top level
        if self.additional_properties is not None:
            for _key, _value in self.additional_properties.items():
                _dict[_key] = _value

        # set to None if one_of_candidates (nullable) is None
        # and __fields_set__ contains the field
        if self.one_of_candidates is None and "one_of_candidates" in self.__fields_set__:
            _dict['oneOfCandidates'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ReconcileStringRule:
        """Create an instance of ReconcileStringRule from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ReconcileStringRule.parse_obj(obj)

        _obj = ReconcileStringRule.parse_obj({
            "rule_type": obj.get("ruleType"),
            "comparison_type": obj.get("comparisonType"),
            "one_of_candidates": obj.get("oneOfCandidates"),
            "applies_to": AggregateSpec.from_dict(obj.get("appliesTo")) if obj.get("appliesTo") is not None else None
        })
        # store additional fields in additional_properties
        for _key in obj.keys():
            if _key not in cls.__properties:
                _obj.additional_properties[_key] = obj.get(_key)

        return _obj
