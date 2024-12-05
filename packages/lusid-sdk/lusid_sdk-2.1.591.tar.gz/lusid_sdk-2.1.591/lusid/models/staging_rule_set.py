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
from pydantic.v1 import BaseModel, Field, StrictStr, conlist, constr
from lusid.models.link import Link
from lusid.models.staging_rule import StagingRule
from lusid.models.version import Version

class StagingRuleSet(BaseModel):
    """
    StagingRuleSet
    """
    entity_type: constr(strict=True, min_length=1) = Field(..., alias="entityType", description="The entity type the staging rule set applies to.")
    staging_rule_set_id: constr(strict=True, min_length=1) = Field(..., alias="stagingRuleSetId", description="System generated unique id for the staging rule set.")
    display_name: constr(strict=True, min_length=1) = Field(..., alias="displayName", description="The name of the staging rule set.")
    description: Optional[StrictStr] = Field(None, description="A description for the staging rule set.")
    rules: conlist(StagingRule) = Field(..., description="The list of staging rules that apply to a specific entity type.")
    href: Optional[StrictStr] = Field(None, description="The specific Uniform Resource Identifier (URI) for this resource at the requested effective and asAt datetime.")
    version: Optional[Version] = None
    links: Optional[conlist(Link)] = None
    __properties = ["entityType", "stagingRuleSetId", "displayName", "description", "rules", "href", "version", "links"]

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
    def from_json(cls, json_str: str) -> StagingRuleSet:
        """Create an instance of StagingRuleSet from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of each item in rules (list)
        _items = []
        if self.rules:
            for _item in self.rules:
                if _item:
                    _items.append(_item.to_dict())
            _dict['rules'] = _items
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if description (nullable) is None
        # and __fields_set__ contains the field
        if self.description is None and "description" in self.__fields_set__:
            _dict['description'] = None

        # set to None if href (nullable) is None
        # and __fields_set__ contains the field
        if self.href is None and "href" in self.__fields_set__:
            _dict['href'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> StagingRuleSet:
        """Create an instance of StagingRuleSet from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return StagingRuleSet.parse_obj(obj)

        _obj = StagingRuleSet.parse_obj({
            "entity_type": obj.get("entityType"),
            "staging_rule_set_id": obj.get("stagingRuleSetId"),
            "display_name": obj.get("displayName"),
            "description": obj.get("description"),
            "rules": [StagingRule.from_dict(_item) for _item in obj.get("rules")] if obj.get("rules") is not None else None,
            "href": obj.get("href"),
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
