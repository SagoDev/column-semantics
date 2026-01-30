"""Response Models"""

from typing import List, Optional
from pydantic import BaseModel, Field


class ColumnResponse(BaseModel):
    """
    Semantic inference result for a single column name.
    """

    column_name: str = Field(
        ...,
        description="Original column name as received in the input",
        examples=["total_amt_usd"],
    )

    meanings: List[str] = Field(
        default_factory=list,
        description="Possible semantic meanings inferred from the column name",
        examples=[["Total monetary amount in USD"]],
    )

    data_type: Optional[str] = Field(
        default=None,
        description="Expected data type inferred from naming conventions",
        examples=["decimal", "integer", "boolean", "timestamp"],
    )

    role: Optional[str] = Field(
        default=None,
        description="Typical role of the column in a data model",
        examples=["metric", "identifier", "flag", "timestamp", "foreign_key"],
    )

    notes: List[str] = Field(
        default_factory=list,
        description="Engineering notes or best practices related to this column",
        examples=[["Avoid float precision issues for financial values"]],
    )

    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence score of the semantic inference",
        examples=[0.91],
    )


class ListColumnsResponse(BaseModel):
    """
    Semantic inference result for multiple column names.
    """

    results: List[ColumnResponse] = Field(
        ...,
        description="Semantic inference results for each column name",
    )
