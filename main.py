"""
Column Semantics - Usage Example

This example demonstrates how to use the column_semantics library
to analyze and understand the semantic meaning of column names.
"""

import column_semantics as cs


def main():
    """Main example demonstrating column analysis features."""

    # Example 1: E-commerce dataset columns
    print("=== E-commerce Dataset Analysis ===")
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

    ecommerce_results = cs.analyze_columns(ecommerce_columns, include_summary=True)

    print("Column analysis results:")
    for column in ecommerce_results:
        best_match = ecommerce_results.get_best_for_column(column)
        if best_match:
            confidence = best_match.confidence * 100
            print(f"  {column}: {best_match.label} ({confidence:.1f}% confidence)")
    print()

    # Example 2: Financial dataset columns
    print("=== Financial Dataset Analysis ===")
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

    financial_results = cs.analyze_columns(financial_columns)

    print("Financial columns identified:")
    for column in financial_results:
        best_match = financial_results.get_best_for_column(column)
        if best_match and best_match.confidence > 0.7:
            print(f"  [HIGH] {column} -> {best_match.label}")
    print()

    # Example 3: Get summary text
    print("=== Analysis Summary ===")
    print(ecommerce_results.get_summary_text())
    print()

    # Example 4: Show recommendations for high-confidence columns
    print("=== Recommendations ===")
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
    print()

    # Example 5: Show expected conditions
    print("=== Expected Conditions ===")
    print("Data quality expectations for high-confidence columns:")
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
    print()

    # Example 6: Recommendations for financial dataset
    print("=== Financial Dataset Recommendations ===")
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
    print()

    # Example 7: Access statistics
    print("=== Statistics ===")
    print(f"Total hypotheses tested: {ecommerce_results.total_hypotheses}")
    print(f"Average confidence: {ecommerce_results.average_confidence:.2f}")
    print(
        f"High confidence matches: {len(ecommerce_results.high_confidence_hypotheses)}"
    )
    print(f"Semantic types found: {len(ecommerce_results.semantic_types)}")

    # Example 8: Practical recommendations usage
    print("=== Practical Data Engineering Tips ===")
    print("Based on the analysis, here are actionable recommendations:")

    # Primary key columns
    id_columns = ecommerce_results.get_columns_with_type("identifier")
    if id_columns:
        print(f"  Primary Key Candidates: {', '.join(id_columns)}")
        print("    -> Consider these for primary keys or foreign key relationships")

    # Monetary columns
    monetary_columns = ecommerce_results.get_columns_with_type("monetary_amount")
    if monetary_columns:
        print(f"  Monetary Columns: {', '.join(monetary_columns)}")
        print("    -> Use DECIMAL type, avoid FLOAT for precision")
        print("    -> Store currency metadata separately if multi-currency")

    # Date columns
    date_columns = ecommerce_results.get_columns_with_type("date")
    if date_columns:
        print(f"  Date Columns: {', '.join(date_columns)}")
        print("    -> Use ISO 8601 format (YYYY-MM-DD)")
        print("    -> Consider timezone handling for created_at/updated_at")

    # Email columns
    email_columns = ecommerce_results.get_columns_with_type("email")
    if email_columns:
        print(f"  Email Columns: {', '.join(email_columns)}")
        print("    -> Implement email validation")
        print("    -> Consider encryption for privacy compliance")


if __name__ == "__main__":
    main()
