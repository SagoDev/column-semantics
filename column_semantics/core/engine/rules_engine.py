"""
Rules engine for semantic inference based on declarative YAML rules.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml

from column_semantics.core.engine.confidence_engine import ConfidenceEngine
from column_semantics.core.models.output_models import SemanticHypothesis


class RulesEngine:
    """
    Evaluates semantic rules against detected signals.
    """

    def __init__(
        self,
        *,
        rules_path: Path,
        confidence_engine: ConfidenceEngine | None = None,
    ) -> None:
        self.rules = self._load_rules(rules_path)
        self.confidence_engine = confidence_engine or ConfidenceEngine()

    # ---------------- public API ---------------- #

    def evaluate(
        self,
        *,
        signals: List[Dict[str, Any]],
    ) -> List[SemanticHypothesis]:
        """
        Evaluate all rules against the provided signals.
        """
        hypotheses: List[SemanticHypothesis] = []

        for rule in self.rules:
            if self._rule_matches(rule, signals):
                evidence = self._collect_evidence(rule, signals)
                hypotheses.append(
                    SemanticHypothesis(
                        label=rule["label"],
                        evidence=evidence,
                        confidence=self.confidence_engine.score(evidence),
                    )
                )

        return hypotheses

    # ---------------- rule evaluation ---------------- #

    def _rule_matches(
        self,
        rule: Dict[str, Any],
        signals: List[Dict[str, Any]],
    ) -> bool:
        conditions = rule.get("when", {})

        if "all" in conditions:
            return all(self._condition_matches(c, signals) for c in conditions["all"])

        if "any" in conditions:
            return any(self._condition_matches(c, signals) for c in conditions["any"])

        return False

    def _condition_matches(
        self,
        condition: Dict[str, Any],
        signals: List[Dict[str, Any]],
    ) -> bool:
        signal_type = condition.get("signal")

        for signal in signals:
            if signal.get("type") != signal_type:
                continue

            if "equals" in condition and signal.get("value") == condition["equals"]:
                return True

            if "in" in condition and signal.get("value") in condition["in"]:
                return True

            if len(condition.keys()) == 1:  # only 'signal'
                return True

        return False

    # ---------------- evidence collection ---------------- #

    def _collect_evidence(
        self,
        rule: Dict[str, Any],
        signals: List[Dict[str, Any]],
    ) -> List[Dict[str, Any]]:
        """
        Collect all signals used as evidence for a matched rule.
        """
        used_signals: List[Dict[str, Any]] = []

        conditions = rule.get("when", {})
        condition_blocks = conditions.get("all") or conditions.get("any") or []

        for condition in condition_blocks:
            for signal in signals:
                if signal.get("type") == condition.get("signal"):
                    used_signals.append(signal)

        return used_signals

    # ---------------- loading ---------------- #

    def _load_rules(self, path: Path) -> List[Dict[str, Any]]:
        if not path.exists():
            raise FileNotFoundError(f"Rules file not found: {path}")

        with path.open("r", encoding="utf-8") as f:
            rules = yaml.safe_load(f)

        if not isinstance(rules, list):
            raise ValueError("Rules YAML must be a list of rules")

        return rules
