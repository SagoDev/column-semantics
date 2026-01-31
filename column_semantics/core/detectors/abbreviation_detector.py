""" "Abbreviation detector."""

from __future__ import annotations

from typing import List, Dict, Any

from .base import BaseDetector


class AbbreviationDetector(BaseDetector):
    """
    Detects known abbreviations in column names.
    """

    def detect(self, tokens: List[str]) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []

        for token in tokens:
            if token in self.knowledge:
                signals.append(
                    {
                        "type": "abbreviation",
                        "token": token,
                        "meaning": self.knowledge[token],
                    }
                )

        return signals
