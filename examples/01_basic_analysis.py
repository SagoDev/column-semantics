"""Basic Column Analysis Example

This example demonstrates the fundamental usage of column_semantics
for analyzing column names and understanding their semantic meaning.
"""

import column_semantics as cs


def main():
    """Demonstrate basic column analysis features."""

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

    # Example 4: Access statistics
    print("=== Statistics ===")
    print(f"Total hypotheses tested: {ecommerce_results.total_hypotheses}")
    print(f"Average confidence: {ecommerce_results.average_confidence:.2f}")
    print(
        f"High confidence matches: {len(ecommerce_results.high_confidence_hypotheses)}"
    )
    print(f"Semantic types found: {len(ecommerce_results.semantic_types)}")
    print()

    # Example 5: Show specific semantic types
    print("=== Semantic Type Examples ===")

    # Primary key columns
    id_columns = ecommerce_results.get_columns_with_type("identifier")
    if id_columns:
        print(f"Primary Key Candidates: {', '.join(id_columns)}")

    # Monetary columns
    monetary_columns = ecommerce_results.get_columns_with_type("monetary_amount")
    if monetary_columns:
        print(f"Monetary Columns: {', '.join(monetary_columns)}")

    # Date columns
    date_columns = ecommerce_results.get_columns_with_type("date")
    if date_columns:
        print(f"Date Columns: {', '.join(date_columns)}")

    # Email columns
    email_columns = ecommerce_results.get_columns_with_type("email")
    if email_columns:
        print(f"Email Columns: {', '.join(email_columns)}")


if __name__ == "__main__":
    main()
