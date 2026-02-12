"""Column Analysis Results Module."""

from column_semantics.core.analyzer.analyzer import ColumnAnalyzer
from column_semantics.core.analysis.analysis_results import ColumnAnalysisResults


def analyze_columns(columns: list[str], **kwargs) -> ColumnAnalysisResults:
    """
    Analyze columns and return user-friendly results object.

    This function provides the easiest access to column analysis results
    with convenient methods and properties.

    Args:
        columns: List of column names to analyze
        **kwargs: Additional options passed to analysis

    Returns:
        ColumnAnalysisResults object with convenient access methods

    Example:
        >>> from column_semantics import analyze_columns
        >>> columns = ["user_id", "created_at", "amount_usd", "is_active"]
        >>> results = analyze_columns(columns, include_summary=True)
        >>>
        >>> # Easy access to statistics
        >>> print(f"Analyzed {results.count} columns")
        >>> print(f"Top hypothesis: {results.top_hypothesis.label}")
        >>>
        >>> # Easy iteration
        >>> for col in results:
        ...     best = results.get_best_for_column(col)
        ...     if best:
        ...         print(f"{col}: {best.label}")
        >>>
        >>> # Summary text
        >>> print(results.get_summary_text())
    """

    analyzer = ColumnAnalyzer()
    raw_results = analyzer.analyze_many(columns, **kwargs)
    return ColumnAnalysisResults(raw_results)
