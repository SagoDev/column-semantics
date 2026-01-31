"""Role detector."""

from __future__ import annotations

from typing import List, Dict, Any

from .base import BaseDetector


class RoleDetector(BaseDetector):
    """
    Detects business or analytical roles of a column.
    """

    def detect(self, tokens: List[str]) -> List[Dict[str, Any]]:
        signals: List[Dict[str, Any]] = []

        for token in tokens:
            if token in self.knowledge:
                signals.append(
                    {
                        "type": "role",
                        "token": token,
                        "role": self.knowledge[token],
                    }
                )

        return signals
