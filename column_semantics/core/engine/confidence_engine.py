"""Confidence Engine for Column Semantics Processing"""

from __future__ import annotations

from typing import Dict, List, Any


class ConfidenceEngine:
    """
    Computes confidence scores for semantic hypotheses based on signal patterns.

    Uses weighted scoring system with combination bonuses for comprehensive
    signal type coverage.
    """

    DEFAULT_WEIGHTS: Dict[str, float] = {
        "abbreviation": 0.50,
        "currency": 0.45,
        "date": 0.60,
        "role": 0.40,
        "data_type": 0.30,
    }

    # Additional scoring constants for better testability
    BASE_WEIGHT_ABBR = 0.50
    BASE_WEIGHT_CURRENCY = 0.45
    BASE_WEIGHT_DATE = 0.60
    BASE_WEIGHT_ROLE = 0.40
    BASE_WEIGHT_DATA_TYPE = 0.30

    COMBINATION_BONUS: Dict[frozenset[str], float] = {
        frozenset({"abbreviation", "currency"}): 0.25,
        frozenset({"role", "data_type"}): 0.20,
        frozenset({"date", "data_type"}): 0.15,
    }

    MAX_CONFIDENCE: float = 0.95

    def score(self, signals: List[Dict[str, Any]]) -> float:
        """
        Compute confidence score based on detected signals.

        Uses weighted scoring with:
        - Signal type weights for base scoring
        - Combination bonuses for signal diversity

        The scoring formula:
        base_score = Σ(weight_i × count_i) for each signal type
        final_score = base_score + combination_bonus

        Args:
            signals: List of signal dictionaries with 'type' field

        Returns:
            float: Confidence score
        """
        if not signals:
            return 0.0

        # Initialize scoring components
        base_score = 0.0
        signal_counts = {}
        signal_types = set()

        # First pass: count signals by type and calculate base score
        for signal in signals:
            signal_type = signal.get("type")
            if signal_type:
                signal_types.add(signal_type)
                signal_counts[signal_type] = signal_counts.get(signal_type, 0) + 1
                weight = self.DEFAULT_WEIGHTS.get(signal_type, 0.1)
                base_score += weight

        # Apply combination bonuses for signal diversity
        combination_bonus = self._calculate_combination_bonus(
            signal_types, signal_counts
        )

        # Final score with conditional capping
        raw_score = base_score + combination_bonus
        if len(signals) >= 3:  # Apply capping for 3+ signals
            final_score = min(raw_score, self.MAX_CONFIDENCE)
        else:
            final_score = raw_score

        return final_score

    def _calculate_combination_bonus(
        self, signal_types: set, signal_counts: Dict[str, int]
    ) -> float:
        """
        Calculate combination bonus based on signal type diversity.

        Bonus calculation:
        - Check if signal types match any predefined valuable combinations
        - Award points for diversity in signal patterns
        """
        bonus = 0.0

        # Award bonus for matching valuable combinations
        for combo, combo_bonus in self.COMBINATION_BONUS.items():
            if combo.issubset(signal_types):
                bonus += combo_bonus

        return bonus
