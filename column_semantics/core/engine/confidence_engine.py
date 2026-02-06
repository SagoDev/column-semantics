"""Confidence Engine for Column Semantics Processing"""

from __future__ import annotations

from typing import Dict, List, Any


class ConfidenceEngine:
    """
    Computes confidence scores for semantic hypotheses.
    """

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "abbreviation": 0.50,
        "currency": 0.45,
        "date": 0.60,
        "role": 0.40,
        "data_type": 0.30,
    }

    COMBINATION_BONUS: Dict[frozenset[str], float] = {
        frozenset({"abbreviation", "currency"}): 0.25,
        frozenset({"role", "data_type"}): 0.20,
        frozenset({"date", "data_type"}): 0.15,
        frozenset({"abbreviation", "role"}): 0.30,
        frozenset({"abbreviation", "date"}): 0.25,
        }

    MAX_CONFIDENCE: float = 0.95

    def score(self, signals: List[Dict[str, Any]]) -> float:
        """
        Compute confidence score based on detected signals.
        """
        if not signals:
            return 0.0

        score = 0.0
        signal_types = set()

        for signal in signals:
            signal_type = signal["type"]
            signal_types.add(signal_type)
            score += self.DEFAULT_WEIGHTS.get(signal_type, 0.1)

        # Apply combination bonuses
        for combo, bonus in self.COMBINATION_BONUS.items():
            if combo.issubset(signal_types):
                score += bonus

        return min(score, self.MAX_CONFIDENCE)
