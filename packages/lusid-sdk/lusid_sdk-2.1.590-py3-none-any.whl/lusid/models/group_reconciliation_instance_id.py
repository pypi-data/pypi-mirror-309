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
from pydantic.v1 import BaseModel, Field, constr

class GroupReconciliationInstanceId(BaseModel):
    """
    GroupReconciliationInstanceId
    """
    run_id_type: constr(strict=True, min_length=1) = Field(..., alias="runIdType", description="Type of the reconciliation run, manual or automatic (via the workflow). \"Manual\" | \"WorkflowServiceTaskId\"")
    run_id_value: constr(strict=True, min_length=1) = Field(..., alias="runIdValue", description="Reconciliation run identifier: a manually-provided key or taskId.")
    __properties = ["runIdType", "runIdValue"]

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
    def from_json(cls, json_str: str) -> GroupReconciliationInstanceId:
        """Create an instance of GroupReconciliationInstanceId from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> GroupReconciliationInstanceId:
        """Create an instance of GroupReconciliationInstanceId from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return GroupReconciliationInstanceId.parse_obj(obj)

        _obj = GroupReconciliationInstanceId.parse_obj({
            "run_id_type": obj.get("runIdType"),
            "run_id_value": obj.get("runIdValue")
        })
        return _obj
