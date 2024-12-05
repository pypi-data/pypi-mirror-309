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
from pydantic.v1 import BaseModel, Field, StrictStr, conlist
from lusid.models.link import Link
from lusid.models.resource_id import ResourceId
from lusid.models.version import Version

class RelationDefinition(BaseModel):
    """
    RelationDefinition
    """
    version: Optional[Version] = None
    relation_definition_id: Optional[ResourceId] = Field(None, alias="relationDefinitionId")
    source_entity_domain: Optional[StrictStr] = Field(None, alias="sourceEntityDomain", description="The entity domain of the source entity object.")
    target_entity_domain: Optional[StrictStr] = Field(None, alias="targetEntityDomain", description="The entity domain of the target entity object.")
    display_name: Optional[StrictStr] = Field(None, alias="displayName", description="The display name of the relation.")
    outward_description: Optional[StrictStr] = Field(None, alias="outwardDescription", description="The description to relate source entity object and target entity object")
    inward_description: Optional[StrictStr] = Field(None, alias="inwardDescription", description="The description to relate target entity object and source entity object")
    life_time: Optional[StrictStr] = Field(None, alias="lifeTime", description="Describes how the relations can change over time, allowed values are \"Perpetual\" and \"TimeVariant\"")
    constraint_style: Optional[StrictStr] = Field(None, alias="constraintStyle", description="Describes the uniqueness and cardinality for relations with a specific source entity object and relations under this definition. Allowed values are \"Property\" and \"Collection\", defaults to \"Collection\" if not specified.")
    links: Optional[conlist(Link)] = None
    __properties = ["version", "relationDefinitionId", "sourceEntityDomain", "targetEntityDomain", "displayName", "outwardDescription", "inwardDescription", "lifeTime", "constraintStyle", "links"]

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
    def from_json(cls, json_str: str) -> RelationDefinition:
        """Create an instance of RelationDefinition from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of version
        if self.version:
            _dict['version'] = self.version.to_dict()
        # override the default output from pydantic by calling `to_dict()` of relation_definition_id
        if self.relation_definition_id:
            _dict['relationDefinitionId'] = self.relation_definition_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in links (list)
        _items = []
        if self.links:
            for _item in self.links:
                if _item:
                    _items.append(_item.to_dict())
            _dict['links'] = _items
        # set to None if source_entity_domain (nullable) is None
        # and __fields_set__ contains the field
        if self.source_entity_domain is None and "source_entity_domain" in self.__fields_set__:
            _dict['sourceEntityDomain'] = None

        # set to None if target_entity_domain (nullable) is None
        # and __fields_set__ contains the field
        if self.target_entity_domain is None and "target_entity_domain" in self.__fields_set__:
            _dict['targetEntityDomain'] = None

        # set to None if display_name (nullable) is None
        # and __fields_set__ contains the field
        if self.display_name is None and "display_name" in self.__fields_set__:
            _dict['displayName'] = None

        # set to None if outward_description (nullable) is None
        # and __fields_set__ contains the field
        if self.outward_description is None and "outward_description" in self.__fields_set__:
            _dict['outwardDescription'] = None

        # set to None if inward_description (nullable) is None
        # and __fields_set__ contains the field
        if self.inward_description is None and "inward_description" in self.__fields_set__:
            _dict['inwardDescription'] = None

        # set to None if life_time (nullable) is None
        # and __fields_set__ contains the field
        if self.life_time is None and "life_time" in self.__fields_set__:
            _dict['lifeTime'] = None

        # set to None if constraint_style (nullable) is None
        # and __fields_set__ contains the field
        if self.constraint_style is None and "constraint_style" in self.__fields_set__:
            _dict['constraintStyle'] = None

        # set to None if links (nullable) is None
        # and __fields_set__ contains the field
        if self.links is None and "links" in self.__fields_set__:
            _dict['links'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> RelationDefinition:
        """Create an instance of RelationDefinition from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return RelationDefinition.parse_obj(obj)

        _obj = RelationDefinition.parse_obj({
            "version": Version.from_dict(obj.get("version")) if obj.get("version") is not None else None,
            "relation_definition_id": ResourceId.from_dict(obj.get("relationDefinitionId")) if obj.get("relationDefinitionId") is not None else None,
            "source_entity_domain": obj.get("sourceEntityDomain"),
            "target_entity_domain": obj.get("targetEntityDomain"),
            "display_name": obj.get("displayName"),
            "outward_description": obj.get("outwardDescription"),
            "inward_description": obj.get("inwardDescription"),
            "life_time": obj.get("lifeTime"),
            "constraint_style": obj.get("constraintStyle"),
            "links": [Link.from_dict(_item) for _item in obj.get("links")] if obj.get("links") is not None else None
        })
        return _obj
