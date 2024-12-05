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
from typing import Any, Dict, List, Optional
from pydantic.v1 import BaseModel, Field, StrictBool, StrictStr, conlist, constr
from lusid.models.aggregate_spec import AggregateSpec
from lusid.models.market_data_overrides import MarketDataOverrides
from lusid.models.order_by_spec import OrderBySpec
from lusid.models.order_flow_configuration import OrderFlowConfiguration
from lusid.models.portfolio_entity_id import PortfolioEntityId
from lusid.models.property_filter import PropertyFilter
from lusid.models.resource_id import ResourceId
from lusid.models.valuation_schedule import ValuationSchedule

class ValuationRequest(BaseModel):
    """
    Specification object for the parameters of a valuation  # noqa: E501
    """
    recipe_id: ResourceId = Field(..., alias="recipeId")
    as_at: Optional[datetime] = Field(None, alias="asAt", description="The asAt date to use")
    metrics: conlist(AggregateSpec) = Field(..., description="The set of specifications to calculate or retrieve during the valuation and present in the results. For example:  AggregateSpec('Valuation/PV','Sum') for returning the PV (present value) of holdings  AggregateSpec('Holding/default/Units','Sum') for returning the units of holidays  AggregateSpec('Instrument/default/LusidInstrumentId','Value') for returning the Lusid Instrument identifier")
    group_by: Optional[conlist(StrictStr)] = Field(None, alias="groupBy", description="The set of items by which to perform grouping. This primarily matters when one or more of the metric operators is a mapping  that reduces set size, e.g. sum or proportion. The group-by statement determines the set of keys by which to break the results out.")
    filters: Optional[conlist(PropertyFilter)] = Field(None, description="A set of filters to use to reduce the data found in a request. Equivalent to the 'where ...' part of a Sql select statement.  For example, filter a set of values within a given range or matching a particular value.")
    sort: Optional[conlist(OrderBySpec)] = Field(None, description="A (possibly empty/null) set of specifications for how to order the results.")
    report_currency: Optional[constr(strict=True, max_length=3, min_length=0)] = Field(None, alias="reportCurrency", description="Three letter ISO currency string indicating what currency to report in for ReportCurrency denominated queries.  If not present, then the currency of the relevant portfolio will be used in its place.")
    equip_with_subtotals: Optional[StrictBool] = Field(None, alias="equipWithSubtotals", description="Flag directing the Valuation call to populate the results with subtotals of aggregates.")
    return_result_as_expanded_types: Optional[StrictBool] = Field(None, alias="returnResultAsExpandedTypes", description="Financially meaningful results can be presented as either simple flat types or more complex expanded types.  For example, the present value (PV) of a holding could be represented either as a simple decimal (with currency implied)  or as a decimal-currency pair. This flag allows either representation to be returned. In the PV example,  the returned value would be the decimal-currency pair if this flag is true, or the decimal only if this flag is false.")
    include_order_flow: Optional[OrderFlowConfiguration] = Field(None, alias="includeOrderFlow")
    portfolio_entity_ids: conlist(PortfolioEntityId) = Field(..., alias="portfolioEntityIds", description="The set of portfolio or portfolio group identifier(s) that is to be valued.")
    valuation_schedule: ValuationSchedule = Field(..., alias="valuationSchedule")
    market_data_overrides: Optional[MarketDataOverrides] = Field(None, alias="marketDataOverrides")
    corporate_action_source_id: Optional[ResourceId] = Field(None, alias="corporateActionSourceId")
    __properties = ["recipeId", "asAt", "metrics", "groupBy", "filters", "sort", "reportCurrency", "equipWithSubtotals", "returnResultAsExpandedTypes", "includeOrderFlow", "portfolioEntityIds", "valuationSchedule", "marketDataOverrides", "corporateActionSourceId"]

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
    def from_json(cls, json_str: str) -> ValuationRequest:
        """Create an instance of ValuationRequest from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self):
        """Returns the dictionary representation of the model using alias"""
        _dict = self.dict(by_alias=True,
                          exclude={
                          },
                          exclude_none=True)
        # override the default output from pydantic by calling `to_dict()` of recipe_id
        if self.recipe_id:
            _dict['recipeId'] = self.recipe_id.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in metrics (list)
        _items = []
        if self.metrics:
            for _item in self.metrics:
                if _item:
                    _items.append(_item.to_dict())
            _dict['metrics'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in filters (list)
        _items = []
        if self.filters:
            for _item in self.filters:
                if _item:
                    _items.append(_item.to_dict())
            _dict['filters'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in sort (list)
        _items = []
        if self.sort:
            for _item in self.sort:
                if _item:
                    _items.append(_item.to_dict())
            _dict['sort'] = _items
        # override the default output from pydantic by calling `to_dict()` of include_order_flow
        if self.include_order_flow:
            _dict['includeOrderFlow'] = self.include_order_flow.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in portfolio_entity_ids (list)
        _items = []
        if self.portfolio_entity_ids:
            for _item in self.portfolio_entity_ids:
                if _item:
                    _items.append(_item.to_dict())
            _dict['portfolioEntityIds'] = _items
        # override the default output from pydantic by calling `to_dict()` of valuation_schedule
        if self.valuation_schedule:
            _dict['valuationSchedule'] = self.valuation_schedule.to_dict()
        # override the default output from pydantic by calling `to_dict()` of market_data_overrides
        if self.market_data_overrides:
            _dict['marketDataOverrides'] = self.market_data_overrides.to_dict()
        # override the default output from pydantic by calling `to_dict()` of corporate_action_source_id
        if self.corporate_action_source_id:
            _dict['corporateActionSourceId'] = self.corporate_action_source_id.to_dict()
        # set to None if as_at (nullable) is None
        # and __fields_set__ contains the field
        if self.as_at is None and "as_at" in self.__fields_set__:
            _dict['asAt'] = None

        # set to None if group_by (nullable) is None
        # and __fields_set__ contains the field
        if self.group_by is None and "group_by" in self.__fields_set__:
            _dict['groupBy'] = None

        # set to None if filters (nullable) is None
        # and __fields_set__ contains the field
        if self.filters is None and "filters" in self.__fields_set__:
            _dict['filters'] = None

        # set to None if sort (nullable) is None
        # and __fields_set__ contains the field
        if self.sort is None and "sort" in self.__fields_set__:
            _dict['sort'] = None

        # set to None if report_currency (nullable) is None
        # and __fields_set__ contains the field
        if self.report_currency is None and "report_currency" in self.__fields_set__:
            _dict['reportCurrency'] = None

        return _dict

    @classmethod
    def from_dict(cls, obj: dict) -> ValuationRequest:
        """Create an instance of ValuationRequest from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return ValuationRequest.parse_obj(obj)

        _obj = ValuationRequest.parse_obj({
            "recipe_id": ResourceId.from_dict(obj.get("recipeId")) if obj.get("recipeId") is not None else None,
            "as_at": obj.get("asAt"),
            "metrics": [AggregateSpec.from_dict(_item) for _item in obj.get("metrics")] if obj.get("metrics") is not None else None,
            "group_by": obj.get("groupBy"),
            "filters": [PropertyFilter.from_dict(_item) for _item in obj.get("filters")] if obj.get("filters") is not None else None,
            "sort": [OrderBySpec.from_dict(_item) for _item in obj.get("sort")] if obj.get("sort") is not None else None,
            "report_currency": obj.get("reportCurrency"),
            "equip_with_subtotals": obj.get("equipWithSubtotals"),
            "return_result_as_expanded_types": obj.get("returnResultAsExpandedTypes"),
            "include_order_flow": OrderFlowConfiguration.from_dict(obj.get("includeOrderFlow")) if obj.get("includeOrderFlow") is not None else None,
            "portfolio_entity_ids": [PortfolioEntityId.from_dict(_item) for _item in obj.get("portfolioEntityIds")] if obj.get("portfolioEntityIds") is not None else None,
            "valuation_schedule": ValuationSchedule.from_dict(obj.get("valuationSchedule")) if obj.get("valuationSchedule") is not None else None,
            "market_data_overrides": MarketDataOverrides.from_dict(obj.get("marketDataOverrides")) if obj.get("marketDataOverrides") is not None else None,
            "corporate_action_source_id": ResourceId.from_dict(obj.get("corporateActionSourceId")) if obj.get("corporateActionSourceId") is not None else None
        })
        return _obj
