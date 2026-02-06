"""Results classes for column analysis with easy access methods."""

from __future__ import annotations

from typing import Any, Dict, List
from column_semantics.core.models import InferenceResult, SemanticHypothesis


class ColumnAnalysisResults:
    """
    Container for column analysis results with convenient access methods.

    This class wraps the raw dictionary results and provides easy-to-use methods
    for accessing analysis data without manual dictionary navigation.

    Example:
        >>> from column_semantics import analyze_columns
        >>> results = analyze_columns(columns, include_summary=True)
        >>> print(f"Analyzed {results.count} columns")
        >>> print(f"Top hypothesis: {results.top_hypothesis}")
        >>> for col in results:
        ...     print(f"{col}: {results[col].best_hypothesis}")
    """

    def __init__(self, raw_results: Dict[str, Any]):
        self._raw_results = raw_results
        self._columns = raw_results.get("columns", {})
        self._summary = raw_results.get("summary", {})

    @property
    def count(self) -> int:
        """Number of columns analyzed."""
        return self._raw_results.get("total_columns", len(self._columns))

    @property
    def summary(self) -> Dict[str, Any]:
        """Summary statistics (if available)."""
        return self._summary

    @property
    def has_summary(self) -> bool:
        """Whether summary statistics are available."""
        return bool(self._summary)

    @property
    def all_hypotheses(self) -> List[SemanticHypothesis]:
        """All hypotheses from all columns."""
        hypotheses = []
        for result in self._columns.values():
            hypotheses.extend(result.hypotheses)
        return hypotheses

    @property
    def total_hypotheses(self) -> int:
        """Total number of hypotheses generated."""
        if self.has_summary:
            return self._summary.get("total_hypotheses", 0)
        return len(self.all_hypotheses)

    @property
    def semantic_types(self) -> List[str]:
        """All semantic types found."""
        if self.has_summary:
            return self._summary.get("semantic_types_found", [])
        return list(set(h.label for h in self.all_hypotheses))

    @property
    def semantic_distribution(self) -> Dict[str, int]:
        """Count of each semantic type found."""
        if self.has_summary:
            return self._summary.get("semantic_distribution", {})

        distribution = {}
        for hypothesis in self.all_hypotheses:
            distribution[hypothesis.label] = distribution.get(hypothesis.label, 0) + 1
        return distribution

    @property
    def average_confidence(self) -> float:
        """Average confidence of all hypotheses."""
        if self.has_summary:
            return self._summary.get("average_confidence", 0.0)

        if not self.all_hypotheses:
            return 0.0
        return sum(h.confidence for h in self.all_hypotheses) / len(self.all_hypotheses)

    @property
    def top_hypothesis(self) -> SemanticHypothesis | None:
        """Hypothesis with highest confidence."""
        if not self.all_hypotheses:
            return None
        return max(self.all_hypotheses, key=lambda h: h.confidence)

    @property
    def high_confidence_hypotheses(self) -> List[SemanticHypothesis]:
        """Hypotheses with confidence >= 0.7."""
        return [h for h in self.all_hypotheses if h.confidence >= 0.7]

    def get_best_for_column(self, column_name: str) -> SemanticHypothesis | None:
        """Get the best hypothesis for a specific column."""
        result = self._columns.get(column_name)
        if not result or not result.hypotheses:
            return None
        return max(result.hypotheses, key=lambda h: h.confidence)

    def get_all_for_column(self, column_name: str) -> List[SemanticHypothesis]:
        """Get all hypotheses for a specific column."""
        result = self._columns.get(column_name)
        if not result:
            return []
        return result.hypotheses

    def get_columns_with_type(self, semantic_type: str) -> List[str]:
        """Get all column names that have a given semantic type."""
        matching_columns = []
        for col_name, result in self._columns.items():
            if any(h.label == semantic_type for h in result.hypotheses):
                matching_columns.append(col_name)
        return matching_columns

    def filter_by_confidence(self, min_confidence: float) -> ColumnAnalysisResults:
        """Create new results filtered by minimum confidence."""
        filtered_results = {"total_columns": self.count, "columns": {}}

        for col_name, result in self._columns.items():
            filtered_hypotheses = [
                h for h in result.hypotheses if h.confidence >= min_confidence
            ]
            if filtered_hypotheses:
                filtered_results["columns"][col_name] = InferenceResult(
                    column_name=result.column_name, hypotheses=filtered_hypotheses
                )

        if self.has_summary:
            total_filtered = sum(
                len(result.hypotheses)
                for result in filtered_results["columns"].values()
            )
            filtered_results["summary"] = {"total_hypotheses": total_filtered}

        return ColumnAnalysisResults(filtered_results)

    def get_summary_text(self) -> str:
        """Get a human-readable summary text."""
        lines = [
            "📊 Analysis Summary",
            f"Columns analyzed: {self.count}",
            f"Total hypotheses: {self.total_hypotheses}",
            f"Semantic types found: {len(self.semantic_types)}",
            f"Average confidence: {self.average_confidence:.2f}",
        ]

        if self.semantic_distribution:
            lines.append("\nSemantic distribution:")
            for semantic_type, count in self.semantic_distribution.items():
                percentage = (count / self.total_hypotheses) * 100
                lines.append(f"  {semantic_type}: {count} ({percentage:.1f}%)")

        return "\n".join(lines)

    # Dictionary-like access
    def __getitem__(self, column_name: str) -> InferenceResult:
        """Access column analysis by name like a dictionary."""
        return self._columns[column_name]

    def __contains__(self, column_name: str) -> bool:
        """Check if column exists in results."""
        return column_name in self._columns

    def __iter__(self):
        """Iterate over column names."""
        return iter(self._columns.keys())

    def items(self):
        """Get column name and result pairs."""
        return self._columns.items()

    def keys(self):
        """Get all column names."""
        return self._columns.keys()

    def values(self):
        """Get all column results."""
        return self._columns.values()

    def __str__(self) -> str:
        """String representation showing basic info."""
        return f"ColumnAnalysisResults({self.count} columns, {self.total_hypotheses} hypotheses)"

    def __repr__(self) -> str:
        """Detailed representation."""
        return f"ColumnAnalysisResults(count={self.count}, total_hypotheses={self.total_hypotheses}, semantic_types={self.semantic_types})"
