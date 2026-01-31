"""Inference engine for column semantics detection."""

from __future__ import annotations

from typing import List, Dict, Any

from column_semantics.core.models.output_models import (
    InferenceResult,
    SemanticHypothesis,
)


class InferenceEngine:
    """
    Combines semantic signals into high-level hypotheses.
    """

    def infer(
        self,
        *,
        column_name: str,
        signals: List[Dict[str, Any]],
    ) -> InferenceResult:
        """Infers semantic hypotheses from signals for a given column."""
        hypotheses: List[SemanticHypothesis] = []

        grouped = self._group_by_type(signals)

        # Monetary column
        if "currency" in grouped and "abbreviation" in grouped:
            hypotheses.append(
                SemanticHypothesis(
                    label="monetary_amount",
                    evidence=grouped["currency"] + grouped["abbreviation"],
                    confidence=0.85,
                )
            )

        # Date column
        if "date" in grouped:
            hypotheses.append(
                SemanticHypothesis(
                    label="date",
                    evidence=grouped["date"],
                    confidence=0.80,
                )
            )

        # Identifier
        if "role" in grouped:
            for role in grouped["role"]:
                if role.get("role") == "identifier":
                    hypotheses.append(
                        SemanticHypothesis(
                            label="identifier",
                            evidence=[role],
                            confidence=0.75,
                        )
                    )

        return InferenceResult(
            column_name=column_name,
            hypotheses=hypotheses,
        )

    def _group_by_type(
        self, signals: List[Dict[str, Any]]
    ) -> Dict[str, List[Dict[str, Any]]]:
        grouped: Dict[str, List[Dict[str, Any]]] = {}

        for signal in signals:
            signal_type = signal["type"]
            grouped.setdefault(signal_type, []).append(signal)

        return grouped
