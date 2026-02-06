"""Column Semantics Module."""

from __future__ import annotations
from typing import Any

from .validators import *
from .utils import *
from .core import *


def analyze_columns(columns: list[str], **kwargs) -> dict[str, Any]:
    """
    Analyze a list of column names and return semantic recommendations.

    This is a convenience function that provides easy access to column analysis.

    Args:
        columns: List of column names to analyze
        **kwargs: Additional options passed to analyze_many method

    Returns:
        Dictionary with analysis results for each column

    Example:
        >>> from column_semantics import analyze_columns
        >>> columns = ["user_id", "created_at", "amount_usd", "is_active"]
        >>> results = analyze_columns(columns, include_summary=True)
        >>> print(results["summary"]["semantic_distribution"])
    """
    from .core.analyzer import ColumnAnalyzer

    analyzer = ColumnAnalyzer()
    return analyzer.analyze_many(columns, **kwargs)
