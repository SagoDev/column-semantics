"""
Knowledge loader for semantic inference.
"""

from __future__ import annotations

from pathlib import Path
from typing import Dict, Any, List, Set

import yaml


class KnowledgeBase:
    """
    Loads and stores semantic knowledge used for column inference.
    """

    def __init__(
        self,
        *,
        abbreviations: Dict[str, Any],
        roles: Dict[str, Any],
        data_types: Dict[str, Any],
        dates: Dict[str, Any],
        currencies: Dict[str, Any],
        stopwords: Dict[str, List[str]],
        rules: List[Dict[str, Any]],
    ) -> None:
        self.abbreviations = abbreviations
        self.roles = roles
        self.data_types = data_types
        self.dates = dates
        self.currencies = currencies
        self.stopwords = stopwords
        self.rules = rules

    @property
    def flat_stopwords(self) -> Set[str]:
        """
        Flatten categorized stopwords into a single set.
        """
        words: Set[str] = set()

        for group in self.stopwords.values():
            words.update(group)

        return words

    @classmethod
    def load(cls, base_path: Path | None = None) -> "KnowledgeBase":
        """
        Load knowledge YAML files into a KnowledgeBase instance.
        """
        if base_path is None:
            base_path = Path(__file__).resolve().parent.parent / "knowledge"

        return cls(
            abbreviations=_load_yaml_dict(base_path / "abbreviations.yml"),
            roles=_load_yaml_dict(base_path / "roles.yml"),
            data_types=_load_yaml_dict(base_path / "data_types.yml"),
            dates=_load_yaml_dict(base_path / "dates.yml"),
            currencies=_load_yaml_dict(base_path / "currencies.yml"),
            stopwords=_load_yaml_dict(base_path / "stopwords.yml"),
            rules=_load_yaml_list(base_path / "rules.yml"),
        )


def _load_yaml(path: Path) -> Any:
    if not path.exists():
        raise FileNotFoundError(f"Knowledge file not found: {path.name}")

    with path.open("r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _load_yaml_dict(path: Path) -> Dict[str, Any]:
    data = _load_yaml(path)

    if not isinstance(data, dict):
        raise ValueError(f"Expected dict in {path.name}")

    return data


def _load_yaml_list(path: Path) -> List[Dict[str, Any]]:
    data = _load_yaml(path)

    if not isinstance(data, list):
        raise ValueError(f"Expected list in {path.name}")

    return data
