"""Enums Classes"""

from enum import Enum


class SemanticType(str, Enum):
    """Semantic types"""

    PRIMARY_ID = "primary_id"
    FOREIGN_ID = "foreign_id"
    DATE = "date"
    AMOUNT = "amount"
    UNKNOWN = "unknown"
