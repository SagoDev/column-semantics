"""
Inference engine orchestrating semantic hypothesis generation.
"""

from __future__ import annotations

from typing import Any, Dict, List

from column_semantics.core.engine.rules_engine import RulesEngine
from column_semantics.core.models.output_models import (
    InferenceResult,
    SemanticHypothesis,
)


class InferenceEngine:
    """
    Orchestrates semantic inference by delegating rule evaluation
    and handling post-processing of hypotheses.
    """

    def __init__(
        self,
        *,
        rules_engine: RulesEngine,
    ) -> None:
        self._rules_engine = rules_engine

    # -------------------- public API -------------------- #

    def infer(
        self,
        *,
        column_name: str,
        signals: List[Dict[str, Any]],
    ) -> InferenceResult:
        """
        Infer semantic hypotheses for a column using declarative rules.
        """
        raw_hypotheses = self._rules_engine.evaluate(signals=signals)

        hypotheses = self._post_process(raw_hypotheses)

        return InferenceResult(
            column_name=column_name,
            hypotheses=hypotheses,
        )

    # -------------------- post-processing -------------------- #

    @staticmethod
    def _post_process(
        hypotheses: List[SemanticHypothesis],
    ) -> List[SemanticHypothesis]:
        """
        Deduplicate hypotheses by label keeping the strongest one
        based on priority and confidence.
        """
        unique: dict[str, SemanticHypothesis] = {}

        for hypothesis in hypotheses:
            existing = unique.get(hypothesis.label)

            if existing is None:
                unique[hypothesis.label] = hypothesis
                continue

            existing_key = (
                existing.priority or 0,
                existing.confidence,
            )
            new_key = (
                hypothesis.priority or 0,
                hypothesis.confidence,
            )

            if new_key > existing_key:
                unique[hypothesis.label] = hypothesis

        return sorted(
            unique.values(),
            key=lambda h: (
                h.priority or 0,
                h.confidence,
            ),
            reverse=True,
        )
