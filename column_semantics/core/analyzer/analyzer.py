"""Analyzer for column semantics detection."""

from __future__ import annotations

from pathlib import Path
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
        *,
        include_summary: bool = False,
        confidence_threshold: float = 0.0,
    ) -> dict[str, Any]:
        """
        Analyze multiple column names with additional options for batch processing.

        Args:
            columns: List of column names to analyze
            include_summary: If True, include summary statistics
            confidence_threshold: Minimum confidence threshold for hypotheses

        Returns:
            Dictionary with analysis results and optional summary
        """
        results = [self.analyze(column) for column in columns]

        response = {
            "columns": {col: result for col, result in zip(columns, results)},
            "total_columns": len(columns),
            "processed_at": str(Path(__file__).stat().st_mtime),
        }

        if include_summary:
            all_hypotheses = []
            for result in results:
                filtered_hypotheses = [
                    h for h in result.hypotheses if h.confidence >= confidence_threshold
                ]
                all_hypotheses.extend(filtered_hypotheses)

            # Count by semantic type
            semantic_counts = {}
            for hypothesis in all_hypotheses:
                semantic_counts[hypothesis.label] = (
                    semantic_counts.get(hypothesis.label, 0) + 1
                )

            response["summary"] = {
                "total_hypotheses": len(all_hypotheses),
                "semantic_types_found": list(semantic_counts.keys()),
                "semantic_distribution": semantic_counts,
                "average_confidence": (
                    sum(h.confidence for h in all_hypotheses) / len(all_hypotheses)
                    if all_hypotheses
                    else 0.0
                ),
            }

        return response
