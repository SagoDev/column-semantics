"""Validate column names function"""


def validate_column_names(names: list[str]) -> list[str]:
    """Validate column names."""
    if not names:
        raise ValueError("Column name list cannot be empty")

    for name in names:
        if not name or not name.strip():
            raise ValueError("Column name cannot be empty or blank")

        if not any(c.isalnum() for c in name):
            raise ValueError(
                f"Invalid column name '{name}': no alphanumeric characters"
            )

    return names
