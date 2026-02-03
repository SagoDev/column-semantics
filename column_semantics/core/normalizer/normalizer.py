"""Normalizer module for column semantics processing."""

from typing import Iterable, List, Set


class Normalizer:
    """
    Normalizes raw tokens into a canonical form suitable for semantic inference.
    """

    def __init__(self, *, stopwords: Set[str]) -> None:
        self._stopwords = stopwords

    def normalize(self, tokens: Iterable[str]) -> List[str]:
        """
        Normalize tokens by:
        - lowercasing
        - trimming whitespace
        - removing technical stopwords
        """
        normalized: List[str] = []

        for token in tokens:
            if token is None:
                continue
                
            clean = token.strip().lower()

            if not clean:
                continue

            if clean in self._stopwords:
                continue

            normalized.append(clean)

        return normalized