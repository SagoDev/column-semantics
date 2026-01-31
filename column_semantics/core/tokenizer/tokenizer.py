"""Tokenizer module for column semantics processing."""

import re
from typing import List


class Tokenizer:
    """
    Splits a column name into raw tokens based on naming conventions.
    """

    _SNAKE_SPLIT = re.compile(r"_+")
    _CAMEL_SPLIT = re.compile(r"(?<!^)(?=[A-Z])")

    def tokenize(self, column_name: str) -> List[str]:
        """
        Tokenize a column name into raw components.

        Examples:
            "userCreatedAt" -> ["user", "Created", "At"]
            "TOTAL_AMT_USD" -> ["TOTAL", "AMT", "USD"]
        """
        if not column_name:
            return []

        # First split by snake_case
        parts = self._SNAKE_SPLIT.split(column_name)

        tokens: List[str] = []
        for part in parts:
            # Then split camelCase / PascalCase
            tokens.extend(self._CAMEL_SPLIT.split(part))

        return [t for t in tokens if t]
