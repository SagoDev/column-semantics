"""Analyzer for column semantics detection."""

from __future__ import annotations

from typing import Any, Dict, List

from column_semantics.core.tokenizer import Tokenizer
from column_semantics.core.normalizer import Normalizer
from column_semantics.core.engine import InferenceEngine
from column_semantics.core.engine.rules_engine import RulesEngine
from column_semantics.core.models import InferenceResult
from column_semantics.core.detectors import (
    AbbreviationDetector,
    DateDetector,
    CurrencyDetector,
    RoleDetector,
    DataTypeDetector,
)
from column_semantics.core.loader import KnowledgeBase


class ColumnAnalyzer:
    """
    High-level orchestrator for column semantic analysis.

    This analyzer operates purely on column names and returns
    semantic recommendations for how the column should be treated.
    """

    def __init__(
        self,
        *,
        knowledge_base: KnowledgeBase | None = None,
    ) -> None:
        self.knowledge = knowledge_base or KnowledgeBase.load()

        self.tokenizer = Tokenizer()
        self.normalizer = Normalizer(
            stopwords=self.knowledge.flat_stopwords,
        )

        self.detectors = [
            AbbreviationDetector(self.knowledge.abbreviations),
            DateDetector(self.knowledge.dates),
            CurrencyDetector(self.knowledge.currencies),
            RoleDetector(self.knowledge.roles),
            DataTypeDetector(self.knowledge.data_types),
        ]

        rules_engine = RulesEngine(
            rules=self.knowledge.rules,
        )

        self.inference_engine = InferenceEngine(
            rules_engine=rules_engine,
        )

    # -------------------- public API -------------------- #

    def analyze(self, column_name: str) -> InferenceResult:
        """
        Analyze a single column name and infer its semantic meaning.
        """
        tokens = self.tokenizer.tokenize(column_name)
        normalized_tokens = self.normalizer.normalize(tokens)

        signals: List[Dict[str, Any]] = []

        for detector in self.detectors:
            signals.extend(detector.detect(normalized_tokens))

        return self.inference_engine.infer(
            column_name=column_name,
            signals=signals,
        )

    def analyze_many(
        self,
        columns: List[str],
    ) -> List[InferenceResult]:
        """
        Analyze multiple column names and return semantic recommendations.
        """
        return [self.analyze(column) for column in columns]
