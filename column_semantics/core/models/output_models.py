"""Output models for column semantics detection results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any


@dataclass
class SemanticHypothesis:
    """A hypothesis about the semantic type of a column."""

    label: str
    evidence: List[Dict[str, Any]]
    confidence: float


@dataclass
class InferenceResult:
    """The result of semantic type inference for a column."""

    column_name: str
    hypotheses: List[SemanticHypothesis]
