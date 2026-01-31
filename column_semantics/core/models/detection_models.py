"""Detection models for semantic inference."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class Detection:
    """
    Represents a semantic detection derived from a column token.
    """

    token: str
    meaning: Optional[str] = None
    data_type: Optional[str] = None
    role: Optional[str] = None
    source: str = ""
