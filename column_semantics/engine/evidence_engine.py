"""Evidence Engine"""

from collections import defaultdict
from typing import Iterable

from column_semantics.models.evidence_models import Evidence
from column_semantics.utils.enums import SemanticType


class EvidenceEngine:
    """
    Aggregates semantic evidences and produces
    a scored, explainable semantic inference.
    """

    def __init__(self) -> None:
        self._evidences: list[Evidence] = []

    def add(self, evidence: Evidence) -> None:
        """Add a single evidence."""
        self._evidences.append(evidence)

    def add_many(self, evidences: Iterable[Evidence]) -> None:
        """Add multiple evidences."""
        self._evidences.extend(evidences)

    def aggregate(self) -> dict:
        """
        Aggregate evidences by semantic type.
        """
        grouped: dict[SemanticType, list[Evidence]] = defaultdict(list)

        for ev in self._evidences:
            grouped[ev.semantic_type].append(ev)

        result: dict[str, dict] = {}

        for semantic_type, evidences in grouped.items():
            total_weight = sum(e.weight for e in evidences)

            result[semantic_type.value] = {
                "score": round(total_weight, 3),
                "evidences": evidences,
            }

        return result
