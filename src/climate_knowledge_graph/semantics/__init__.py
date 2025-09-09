"""
This module handles common semantics information
"""

from enum import Enum


class RelationshipEnum(Enum):
    ADDRESSES = "ADDRESSES"
    INCLUDES = "INCLUDES"
    INCREASES = "INCREASES"
    NEGATIVELY_IMPACTS = "NEGATIVELY_IMPACTS"
    POSITIVELY_IMPACTS = "POSITIVELY_IMPACTS"
    REDUCES = "REDUCES"
    TARGETS = "TARGETS"


class RelationshipWithRuleBasedLogicEnum(Enum):
    IS_AVAILABLE_AT_URL = "IS_AVAILABLE_AT_URL"
    IS_A = "IS_A"
    IS_LICENSED_UNDER = "IS_LICENSED_UNDER"
    IS_FROM_ORGANISATION = "IS_FROM_ORGANISATION"


class ResourceTypeEnum(Enum):
    WEBSITE = "WEBSITE"
    CODE_REPOSITORY = "CODE_REPOSITORY"
    ORGANISATION = "ORGANISATION"


RELATIONSHIPS = [i.value for i in RelationshipEnum]
