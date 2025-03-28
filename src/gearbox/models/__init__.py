from .base_class import Base

from .saved_input import SavedInput
from .criterion_has_tag import CriterionHasTag
from .criterion_has_value import CriterionHasValue
from .criterion import Criterion
from .criterion_staging import CriterionStaging
from .display_rules import DisplayRules
from .el_criteria_has_criterion import ElCriteriaHasCriterion
from .eligibility_criteria_has_note import EligibilityCriteriaHasNote
from .eligibility_criteria import EligibilityCriteria
from .input_type import InputType
from .note import Note
from .ontology_code import OntologyCode
from .raw_criteria import RawCriteria
from .pre_annotated_criterion import PreAnnotatedCriterion
from .pre_annotated_criterion_model import PreAnnotatedCriterionModel
from .source import Source
from .site_has_study import SiteHasStudy
from .site import Site
from .study_algorithm_engine import StudyAlgorithmEngine
from .study_link import StudyLink
from .study_version import StudyVersion
from .study import Study
from .tag import Tag
from .triggered_by import TriggeredBy
from .value import Value
from .unit import Unit
from .study_has_patient import StudyHasPatient
from .study_external_id import StudyExternalId

# from sqlalchemy.ext.declarative import declarative_base
# from app.main import DbSession


# class BaseModel(object):
#     """
#     Extend base class for models with some specific methods / thingies.
#     """

#     query = DbSession.query_property()

#     def as_dict(self):
#         """
#         Return an iterable dictionary of model's fields.
#         """
#         return {c.name: getattr(self, c.name) for c in self.__table__.columns}


# Base = declarative_base(cls=BaseModel)
                     
