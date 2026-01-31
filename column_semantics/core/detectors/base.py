"""Base detector class."""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class BaseDetector(ABC):
    """
    Base class for all semantic detectors.
    """

    def __init__(self, knowledge: Dict[str, Any]) -> None:
        self.knowledge = knowledge

    @abstractmethod
    def detect(self, tokens: List[str]) -> List[Dict[str, Any]]:
        """
        Detect semantic signals from normalized tokens.
        """
        raise NotImplementedError
