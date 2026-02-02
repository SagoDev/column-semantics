"""Output models for column semantics detection results."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional


@dataclass
class RuleMatch:
    """Represents a matched rule with explainability."""

    label: str
    description: str | None
    priority: int | None
    priority_real: int | None
    evidence: List[Dict[str, Any]]
    expected_conditions: List[Dict[str, Any]]
    recommended_treatment: List[str]


# ---------------- Semantic Hypothesis ---------------- #


@dataclass(slots=True)
class SemanticHypothesis:
    """
    A semantic hypothesis inferred for a column.

    Represents a recommendation about how the column
    should be interpreted and treated downstream.
    """

    # Core inference
    label: str
    confidence: float
    rule: RuleMatch


# ---------------- Inference Result ---------------- #


@dataclass(slots=True)
class InferenceResult:
    """
    Result of semantic inference for a single column.

    Holds all semantic hypotheses inferred from the column name
    and exposes helpers to resolve the dominant recommendation.
    """

    column_name: str
    hypotheses: List[SemanticHypothesis]

    # ---------------- resolution helpers ---------------- #

    @property
    def best(self) -> Optional[SemanticHypothesis]:
        """
        Returns the best hypothesis based on rule priority and confidence.

        Resolution order:
        1. Higher rule priority
        2. Higher confidence
        """
        if not self.hypotheses:
            return None

        return max(
            self.hypotheses,
            key=lambda h: (
                h.rule.priority if h.rule.priority is not None else 0,
                h.confidence,
            ),
        )

    @property
    def is_ambiguous(self) -> bool:
        """
        Determines if the result is ambiguous.

        Ambiguity is detected when two top hypotheses have
        close confidence AND the same rule priority.
        """
        if len(self.hypotheses) < 2:
            return False

        sorted_h = sorted(
            self.hypotheses,
            key=lambda h: (
                h.rule.priority if h.rule.priority is not None else 0,
                h.confidence,
            ),
            reverse=True,
        )

        top, second = sorted_h[0], sorted_h[1]

        same_priority = (top.rule.priority or 0) == (second.rule.priority or 0)
        close_confidence = abs(top.confidence - second.confidence) < 0.15

        return same_priority and close_confidence

    # ---------------- semantic guidance ---------------- #

    @property
    def recommendations(self) -> List[str]:
        """
        Aggregate recommended treatments from the best hypothesis.
        """
        best = self.best
        if not best:
            return []

        return best.rule.recommended_treatment

    @property
    def expected_conditions(self) -> List[Dict[str, Any]]:
        """
        Aggregate expected conditions from the best hypothesis.
        """
        best = self.best
        if not best:
            return []

        return best.rule.expected_conditions
