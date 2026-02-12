"""Practical Data Engineering Recommendations

This example demonstrates how to extract practical data engineering
recommendations from column analysis results.
"""

import column_semantics as cs


def main():
    """Demonstrate practical data engineering recommendations."""

    # Sample datasets for analysis
    ecommerce_columns = [
        "user_id",
        "product_id",
        "order_id",
        "quantity",
        "price_usd",
        "created_at",
        "updated_at",
        "is_active",
        "customer_email",
        "shipping_address",
        "payment_method",
        "order_status",
    ]

    financial_columns = [
        "account_number",
        "balance",
        "transaction_date",
        "amount",
        "currency",
        "debit_credit",
        "reference_id",
        "category",
    ]

    # Perform analysis
    print("=== Performing Column Analysis ===")
    ecommerce_results = cs.analyze_columns(ecommerce_columns, include_summary=True)
    financial_results = cs.analyze_columns(financial_columns, include_summary=True)

    # E-commerce recommendations
    print("\n=== E-commerce Dataset Recommendations ===")
    print("Treatment recommendations for high-confidence columns:")
    for column in ecommerce_columns:
        column_result = ecommerce_results[column]
        if column_result.best and column_result.best.confidence > 0.7:
            recommendations = column_result.recommendations
            if recommendations:
                print(f"  {column}:")
                for rec in recommendations:
                    print(f"    - {rec}")
            else:
                print(f"  {column}: No specific recommendations")

    # Expected data quality conditions
    print("\n=== Data Quality Expectations ===")
    print("Expected conditions for high-confidence columns:")
    for column in ecommerce_columns:
        column_result = ecommerce_results[column]
        if column_result.best and column_result.best.confidence > 0.7:
            conditions = column_result.expected_conditions
            if conditions:
                print(f"  {column}:")
                for condition in conditions[:3]:  # Show first 3 conditions
                    print(f"    - {condition}")
                if len(conditions) > 3:
                    print(f"    - ... and {len(conditions) - 3} more")
            else:
                print(f"  {column}: No specific conditions")

    # Financial recommendations
    print("\n=== Financial Dataset Recommendations ===")
    print("Key recommendations for financial data:")
    for column in financial_columns:
        if column in financial_results:
            column_result = financial_results[column]
            if column_result.best and column_result.best.confidence > 0.6:
                recommendations = column_result.recommendations
                if recommendations:
                    print(f"  {column} ({column_result.best.label}):")
                    for rec in recommendations[:2]:  # Show top 2 recommendations
                        print(f"    - {rec}")

    # Practical data engineering tips
    print("\n=== Practical Data Engineering Tips ===")
    print("Based on the analysis, here are actionable recommendations:")

    # Primary key recommendations
    id_columns = ecommerce_results.get_columns_with_type("identifier")
    if id_columns:
        print(f"\n  Primary Key Candidates: {', '.join(id_columns)}")
        print("    -> Consider these for primary keys or foreign key relationships")
        print("    -> Use appropriate data types (BIGINT for large datasets)")
        print("    -> Add indexes for performance optimization")
        print("    -> Implement proper constraints (NOT NULL, UNIQUE)")

    # Monetary column recommendations
    monetary_columns = ecommerce_results.get_columns_with_type("monetary_amount")
    if monetary_columns:
        print(f"\n  Monetary Columns: {', '.join(monetary_columns)}")
        print("    -> Use DECIMAL/NUMERIC type, avoid FLOAT for precision")
        print("    -> Store currency metadata separately if multi-currency")
        print("    -> Consider negative values for refunds/returns")
        print("    -> Add CHECK constraints for positive values where applicable")

    # Date column recommendations
    date_columns = ecommerce_results.get_columns_with_type("date")
    if date_columns:
        print(f"\n  Date Columns: {', '.join(date_columns)}")
        print("    -> Use ISO 8601 format (YYYY-MM-DD) for consistency")
        print("    -> Consider timezone handling for created_at/updated_at")
        print("    -> Use TIMESTAMP WITH TIME ZONE for global applications")
        print("    -> Add appropriate indexes for date-based queries")

    # Email column recommendations
    email_columns = ecommerce_results.get_columns_with_type("email")
    if email_columns:
        print(f"\n  Email Columns: {', '.join(email_columns)}")
        print("    -> Implement email validation constraints")
        print("    -> Consider encryption for privacy compliance (GDPR)")
        print("    -> Use lowercase storage for uniqueness")
        print("    -> Add unique constraints where appropriate")

    # Boolean column recommendations
    bool_columns = ecommerce_results.get_columns_with_type("boolean")
    if bool_columns:
        print(f"\n  Boolean Columns: {', '.join(bool_columns)}")
        print("    -> Use BOOLEAN type where supported")
        print("    -> Consider NOT NULL constraints")
        print("    -> Document business logic for default values")
        print("    -> Add indexes for frequently filtered boolean columns")

    # Text/identifier column recommendations
    text_id_columns = ecommerce_results.get_columns_with_type("text_identifier")
    if text_id_columns:
        print(f"\n  Text Identifier Columns: {', '.join(text_id_columns)}")
        print("    -> Consider VARCHAR length carefully")
        print("    -> Add unique constraints where appropriate")
        print("    -> Use consistent case (upper/lower)")
        print("    -> Consider checksums for very long identifiers")

    # Schema design recommendations
    print("\n=== Schema Design Recommendations ===")
    print("Based on semantic analysis:")

    high_confidence_count = len(ecommerce_results.high_confidence_hypotheses)
    total_columns = ecommerce_results.count
    confidence_ratio = high_confidence_count / total_columns if total_columns > 0 else 0

    if confidence_ratio > 0.8:
        print("  ✓ High confidence in column naming - good semantic clarity")
    elif confidence_ratio > 0.6:
        print("  ⚠ Moderate confidence - consider standardizing some column names")
    else:
        print("  ✗ Low confidence - significant naming inconsistencies detected")

    print(f"  → {total_columns} total columns analyzed")
    print(f"  → {high_confidence_count} high-confidence semantic matches")
    print(
        f"  → {len(ecommerce_results.semantic_types)} distinct semantic types identified"
    )

    # Performance optimization tips
    print("\n=== Performance Optimization Tips ===")

    # Index recommendations based on query patterns
    print("  Indexing strategy:")
    for column in ecommerce_columns:
        if column in ecommerce_results:
            result = ecommerce_results[column]
            if result.best and result.best.confidence > 0.7:
                sem_type = result.best.label
                if sem_type in ["identifier", "date"]:
                    print(f"    → {column}: CREATE INDEX (high selectivity)")
                elif sem_type in ["email", "text_identifier"]:
                    print(f"    → {column}: CREATE UNIQUE INDEX (lookup queries)")
                elif sem_type == "boolean":
                    print(f"    → {column}: CREATE INDEX (filtering queries)")

    # Data governance recommendations
    print("\n=== Data Governance Recommendations ===")

    sensitive_columns = []
    for column in ecommerce_columns:
        if column in ecommerce_results:
            result = ecommerce_results[column]
            if result.best and result.best.confidence > 0.7:
                if any(
                    keyword in column.lower()
                    for keyword in ["email", "address", "customer", "user"]
                ):
                    sensitive_columns.append(column)

    if sensitive_columns:
        print(f"  Sensitive data columns: {', '.join(sensitive_columns)}")
        print("    → Implement access controls")
        print("    → Consider encryption for storage")
        print("    → Add audit logging")
        print("    → Ensure GDPR/CCPA compliance")


if __name__ == "__main__":
    main()
