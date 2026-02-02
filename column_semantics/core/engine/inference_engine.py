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
        hypotheses = self._rules_engine.evaluate(signals=signals)

        hypotheses = self._post_process(hypotheses)

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
        Sort, deduplicate and prioritize hypotheses.
        """
        # Deduplicate by label keeping highest confidence
        unique: dict[str, SemanticHypothesis] = {}

        for hypothesis in hypotheses:
            existing = unique.get(hypothesis.label)
            if existing is None or hypothesis.confidence > existing.confidence:
                unique[hypothesis.label] = hypothesis

        return sorted(
            unique.values(),
            key=lambda h: h.confidence,
            reverse=True,
        )
