"""Data type detector."""

from __future__ import annotations

from typing import List, Dict, Any

from .base import BaseDetector


class DataTypeDetector(BaseDetector):
    """
    Detects likely data types from column naming conventions.
    """

    def detect(self, tokens: List[str]) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []

        for token in tokens:
            if token in self.knowledge:
                signals.append(
                    {
                        "type": "data_type",
                        "token": token,
                        "data_type": self.knowledge[token],
                    }
                )

        return signals
