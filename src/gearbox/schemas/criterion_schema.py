# from tkinter.tix import DisplayStyle
from pydantic import BaseModel
from datetime import datetime
from typing import Sequence, List, Any, Optional
from pydantic.utils import GetterDict
from .criterion_has_tag import CriterionTag
from .criterion_has_value import CriterionValue
from .input_type import InputType
from .el_criterion_has_criterion_schema import ElCriterionHasCriterionSchema

import logging
logger = logging.getLogger('gb-logger')

"""
class CriterionValueGetter(GetterDict):
    # map and reformat 'value' fields
    def get(self, key: str, default: Any = None) -> Any:
        if key in ('id','code','description','type','value_string','unit','operator','create_date','active','el_criteria_has_criterions'):
            logger.info(f"KEY: {key} VALUE: {getattr(self._obj.study, key)}")
            # note 'value' is the table name here
            return getattr(self._obj.value, key)
        else:
            return super(CriterionValueGetter, self).get(key, default)

class CriterionValue(BaseModel):
    id: int
    code: Optional[str]
    description: Optional[str]
    type: Optional[str]
    value_string: Optional[str]
    unit: Optional[str]
    operator: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]

    class Config:
        orm_mode = True
        getter_dict = CriterionValueGetter
"""

class CriterionSchema(BaseModel):
    id: int
    code: Optional[str]
    display_name: Optional[str]
    description: Optional[str]
    create_date: Optional[datetime]
    active: Optional[bool]
    ontology_code_id: Optional[int]
    input_type_id: Optional[int]
    tags: Optional[List[CriterionTag]]
    el_criteria_has_criterions: List[ElCriterionHasCriterionSchema]
    input_type: InputType
    values: Optional[List[CriterionValue]]

    class Config:
        orm_mode = True

class CriterionCreateSchema(BaseModel):
    pass

class CriterionSearchResultsSchema(BaseModel):
    pass


