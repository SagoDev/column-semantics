"""Evidence Model"""

from pydantic import BaseModel
from column_semantics.utils.enums import SemanticType


class Evidence(BaseModel):
    """Model representing a single semantic evidence."""

    semantic_type: SemanticType
    rule_name: str
    weight: float
    reason: str
