"""ID Column Rules"""

from typing import Dict, List


_IDENTIFIER_TOKENS = {"id", "uuid", "guid", "key"}
_WEAK_IDENTIFIER_TOKENS = {"identifier", "ident", "pk"}


def id_rule(
    column_name: str,
    *,
    position: int | None = None,
) -> Dict[str, object]:
    """
    Identifier evidence rule.
    Contributes semantic signals related to identifiers.
    """

    name = column_name.strip().lower()
    normalized = name.replace("-", "_")
    tokens: List[str] = [t for t in normalized.split("_") if t]

    evidence: Dict[str, object] = {
        "meanings": [],
        "data_type": None,
        "role": None,
        "notes": [],
        "confidence_weight": 0.0,
    }

    # --- strong signals ---

    # exact identifier name
    if name in _IDENTIFIER_TOKENS:
        evidence["role"] = "identifier"
        evidence["meanings"].append("Unique identifier")
        evidence["data_type"] = "integer"
        evidence["confidence_weight"] = 0.7
        evidence["notes"].append("Column name is a pure identifier")
        return _apply_position_boost(evidence, position)

    # strict suffix (_id, _uuid, _key)
    if tokens and tokens[-1] in _IDENTIFIER_TOKENS:
        evidence["role"] = "foreign_key_candidate"
        evidence["meanings"].append("Identifier reference")
        evidence["confidence_weight"] = 0.45
        evidence["notes"].append("Column ends with identifier token")
        return _apply_position_boost(evidence, position)

    # --- weak signals ---

    # identifier token anywhere (but not last)
    if any(tok in _IDENTIFIER_TOKENS for tok in tokens):
        evidence["role"] = "identifier_candidate"
        evidence["confidence_weight"] = 0.25
        evidence["notes"].append("Identifier token found in column name")

    # semantic weak identifiers (pk, identifier, etc.)
    elif any(tok in _WEAK_IDENTIFIER_TOKENS for tok in tokens):
        evidence["role"] = "identifier_candidate"
        evidence["confidence_weight"] = 0.15
        evidence["notes"].append("Weak identifier-related token detected")

    return _apply_position_boost(evidence, position)


def _apply_position_boost(
    evidence: Dict[str, object],
    position: int | None,
) -> Dict[str, object]:
    """
    Applies a small confidence boost if the column is first in the schema.
    """

    if position == 0 and evidence["confidence_weight"] > 0:
        evidence["confidence_weight"] += 0.1
        evidence["notes"].append("First column in schema")

    return evidence
