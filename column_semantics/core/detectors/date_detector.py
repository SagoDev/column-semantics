"""Date detector."""

from __future__ import annotations

from typing import List, Dict, Any

from .base import BaseDetector


class DateDetector(BaseDetector):
    """
    Detects date-related semantics.
    """

    def detect(self, tokens: List[str]) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []

        for token in tokens:
            if token in self.knowledge:
                signals.append(
                    {
                        "type": "date",
                        "token": token,
                        "semantic": self.knowledge[token],
                    }
                )

        return signals
