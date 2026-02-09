"""Rules engine for semantic inference based on declarative rules."""

from __future__ import annotations

from typing import Any, Dict, List

from column_semantics.core.engine.confidence_engine import ConfidenceEngine
from column_semantics.core.models.output_models import SemanticHypothesis, RuleMatch


class RulesEngine:
    """
    Evaluates semantic rules against detected signals.
    """

    def __init__(
        self,
        *,
        rules: List[Dict[str, Any]],
        confidence_engine: ConfidenceEngine | None = None,
    ) -> None:
        if not rules:
            raise ValueError("RulesEngine initialized with empty rules")

        self._rules = rules
        self._confidence_engine = confidence_engine or ConfidenceEngine()

    # ---------------- public API ---------------- #

    def evaluate(
        self,
        *,
        signals: List[Dict[str, Any]],
    ) -> List[SemanticHypothesis]:
        """
        Evaluate rules against provided signals to infer semantic hypotheses.
        """

        hypotheses: List[SemanticHypothesis] = []

        for rule in self._rules:
            if not self._rule_matches(rule, signals):
                continue

            evidence = self._collect_evidence(rule, signals)

            min_signals = rule.get("min_signals")
            if min_signals is not None and len(evidence) < min_signals:
                continue

            rule_match = RuleMatch(
                label=rule["label"],
                description=rule.get("description"),
                priority=rule.get("priority"),
                priority_real=rule.get("priority_real"),
                evidence=evidence,
                expected_conditions=rule.get("expected_conditions", []),
                recommended_treatment=rule.get("recommended_treatment", []),
            )

            hypotheses.append(
                SemanticHypothesis(
                    label=rule["label"],
                    confidence=self._confidence_engine.score(evidence),
                    rule=rule_match,
                )
            )

        return sorted(
            hypotheses,
            key=lambda h: (
                h.rule.priority or 0,
                h.confidence,
            ),
            reverse=True,
        )

    # ---------------- rule evaluation ---------------- #

    def _rule_matches(
        self,
        rule: Dict[str, Any],
        signals: List[Dict[str, Any]],
    ) -> bool:
        when_block = rule.get("when", {})
        not_block = rule.get("not")

        if not self._match_conditions(when_block, signals):
            return False

        if not_block and self._match_conditions(not_block, signals):
            return False

        return True

    def _match_conditions(
        self,
        conditions: Dict[str, Any],
        signals: List[Dict[str, Any]],
    ) -> bool:
        if "all" in conditions:
            return all(
                self._condition_matches(condition, signals)
                for condition in conditions["all"]
            )

        if "any" in conditions:
            return any(
                self._condition_matches(condition, signals)
                for condition in conditions["any"]
            )

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

            if "equals" in condition:
                if signal.get("value") == condition["equals"]:
                    return True
                continue

            if "in" in condition:
                # Check multiple possible fields for the value, prioritized by signal type
                signal_value = None
                if signal_type == "role":
                    field_priority = ["role", "token", "meaning", "value"]
                elif signal_type == "currency":
                    field_priority = ["currency", "token", "meaning", "value"]
                elif signal_type == "abbreviation":
                    field_priority = ["token", "meaning", "role", "value"]
                else:
                    field_priority = ["token", "role", "currency", "meaning", "value"]

                for field in field_priority:
                    if field in signal:
                        signal_value = signal[field]
                        break

                if signal_value and signal_value in condition["in"]:
                    return True
                continue

            if len(condition) == 1:  # only 'signal'
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
        evidence: List[Dict[str, Any]] = []

        when_block = rule.get("when", {})
        condition_blocks = when_block.get("all") or when_block.get("any") or []

        for condition in condition_blocks:
            for signal in signals:
                if signal.get("type") == condition.get("signal"):
                    evidence.append(signal)

        return evidence
