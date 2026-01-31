"""Output models for column semantics detection results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class SemanticHypothesis:
    """A single hypothesis for the semantic type of a column."""

    label: str
    evidence: List[Dict[str, Any]]
    confidence: float


@dataclass
class InferenceResult:
    """Result of semantic inference for a single column."""

    column_name: str
    hypotheses: List[SemanticHypothesis]

    @property
    def best(self) -> Optional[SemanticHypothesis]:
        """Returns the hypothesis with the highest confidence, or None if there are no hypotheses."""
        if not self.hypotheses:
            return None
        return max(self.hypotheses, key=lambda h: h.confidence)

    @property
    def is_ambiguous(self) -> bool:
        """Determines if the inference result is ambiguous."""
        if len(self.hypotheses) < 2:
            return False
        sorted_h = sorted(self.hypotheses, key=lambda h: h.confidence, reverse=True)
        return (sorted_h[0].confidence - sorted_h[1].confidence) < 0.15
