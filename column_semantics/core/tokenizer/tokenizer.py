"""Tokenizer module for column semantics processing."""

import re
from typing import List

# Define common word patterns for better tokenization
_COMMON_WORDS = {
    "user",
    "created",
    "at",
    "is",
    "has",
    "flag",
    "active",
    "date",
    "time",
    "id",
}


class Tokenizer:
    """
    Splits a column name into raw tokens based on naming conventions.
    """

    _SNAKE_SPLIT = re.compile(r"_+")
    _CAMEL_SPLIT = re.compile(r"(?<=[a-z])(?=[A-Z])|(?=[A-Z][a-z]|[A-Z][0-9]|[0-9][A-Z])")
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

            # Filter out empty strings from split results
            camel_parts = [cp for cp in camel_parts if cp]

            # Further split letters and numbers
            for camel_part in camel_parts:
                number_parts = self._NUMBER_SPLIT.split(camel_part)
                # Filter out empty strings from number split
                number_parts = [np for np in number_parts if np]
                tokens.extend(number_parts)

        # Post-process to merge likely single-letter tokens that should be part of words
        merged_tokens = []
        i = 0
        while i < len(tokens):
            # Look ahead for patterns like 'u', 's', 'e', 'r' followed by capital or number
            if (
                i + 2 < len(tokens)
                and len(tokens[i]) == 1
                and tokens[i].islower()
                and (
                    tokens[i + 1].isupper()
                    or any(c.isdigit() for c in tokens[i + 1])
                    or tokens[i + 1].istitle()
                )
            ):
                # Merge consecutive single letters with following capital letter
                merged_token = tokens[i] + tokens[i + 1]
                merged_tokens.append(merged_token)
                i += 2
            else:
                merged_tokens.append(tokens[i])
                i += 1

        return [t for t in merged_tokens if t and not t.isspace()]
