"""
This module handles common semantics information
"""

from enum import Enum


class RelationshipEnum(Enum):
    ADDRESSES = "ADDRESSES"
    INCLUDES = "INCLUDES"
    INCREASES = "INCREASES"
    IS_AVAILABLE_AT_URL = "IS_AVAILABLE_AT_URL"
    NEGATIVELY_IMPACTS = "NEGATIVELY_IMPACTS"
    POSITIVELY_IMPACTS = "POSITIVELY_IMPACTS"
    REDUCES = "REDUCES"
    TARGETS = "TARGETS"


RELATIONSHIPS = [i.value for i in RelationshipEnum]
