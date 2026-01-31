"""Inference engine for column semantics detection."""

from __future__ import annotations

from collections import defaultdict
from typing import List, Dict, Any, DefaultDict

from column_semantics.core.engine.confidence_engine import ConfidenceEngine
from column_semantics.core.models.output_models import (
    InferenceResult,
    SemanticHypothesis,
)


class InferenceEngine:
    """
    Combines semantic signals into high-level hypotheses.
    """

    def __init__(self) -> None:
        self.confidence_engine = ConfidenceEngine()

    def infer(
        self,
        *,
        column_name: str,
        signals: List[Dict[str, Any]],
    ) -> InferenceResult:
        """Infers semantic hypotheses from signals for a given column."""
        hypotheses: List[SemanticHypothesis] = []

        grouped = self._group_by_type(signals)

        self._infer_monetary(hypotheses, grouped)
        self._infer_date(hypotheses, grouped)
        self._infer_identifier(hypotheses, grouped)

        hypotheses.sort(key=lambda h: h.confidence, reverse=True)

        return InferenceResult(
            column_name=column_name,
            hypotheses=hypotheses,
        )

    # ---------------- inference rules ---------------- #

    def _infer_monetary(
        self,
        hypotheses: List[SemanticHypothesis],
        grouped: Dict[str, List[Dict[str, Any]]],
    ) -> None:
        if not grouped.get("currency") or not grouped.get("abbreviation"):
            return

        evidence = grouped["currency"] + grouped["abbreviation"]
        hypotheses.append(self._build_hypothesis("monetary_amount", evidence))

    def _infer_date(
        self,
        hypotheses: List[SemanticHypothesis],
        grouped: Dict[str, List[Dict[str, Any]]],
    ) -> None:
        if not grouped.get("date"):
            return

        hypotheses.append(self._build_hypothesis("date", grouped["date"]))

    def _infer_identifier(
        self,
        hypotheses: List[SemanticHypothesis],
        grouped: Dict[str, List[Dict[str, Any]]],
    ) -> None:
        for role in grouped.get("role", []):
            if role.get("role") == "identifier":
                hypotheses.append(self._build_hypothesis("identifier", [role]))

    # ---------------- helpers ---------------- #

    def _build_hypothesis(
        self,
        label: str,
        evidence: List[Dict[str, Any]],
    ) -> SemanticHypothesis:
        return SemanticHypothesis(
            label=label,
            evidence=evidence,
            confidence=self.confidence_engine.score(evidence),
        )

    def _group_by_type(
        self, signals: List[Dict[str, Any]]
    ) -> DefaultDict[str, List[Dict[str, Any]]]:
        grouped: DefaultDict[str, List[Dict[str, Any]]] = defaultdict(list)

        for signal in signals:
            grouped[signal["type"]].append(signal)

        return grouped
