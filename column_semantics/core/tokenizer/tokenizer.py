"""Tokenizer module for column semantics processing."""

import re
from typing import List


class Tokenizer:
    """
    Splits a column name into raw tokens based on naming conventions.
    """

    _SNAKE_SPLIT = re.compile(r"_+")
    _CAMEL_SPLIT = re.compile(r"(?<!^)(?=[A-Z][a-z]|[A-Z][0-9]|[0-9][A-Z]|[A-Z][A-Z][a-z]|[A-Z]{2,})")
    _NUMBER_SPLIT = re.compile(r"(?<=[a-zA-Z])(?=[0-9])|(?<=[0-9])(?=[a-zA-Z])")

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
            camel_parts = self._CAMEL_SPLIT.split(part)
            
            # Further split letters and numbers
            for camel_part in camel_parts:
                number_parts = self._NUMBER_SPLIT.split(camel_part)
                tokens.extend(number_parts)

        return [t for t in tokens if t and not t.isspace()]