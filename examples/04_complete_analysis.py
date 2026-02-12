"""Complete Analysis Example

This example combines all features of the column_semantics library:
basic analysis, report generation, and practical recommendations.
"""

import column_semantics as cs
from column_semantics.core.reporter_generator import ReportGenerator


def analyze_dataset(columns, dataset_name):
    """Analyze a dataset and return results with summary."""
    print(f"\n=== {dataset_name} Dataset Analysis ===")
    results = cs.analyze_columns(columns, include_summary=True)

    print(f"Dataset: {dataset_name}")
    print(f"Columns analyzed: {results.count}")
    print(f"Total hypotheses: {results.total_hypotheses}")
    print(f"Average confidence: {results.average_confidence:.2f}")
    print(f"Semantic types found: {len(results.semantic_types)}")

    # Show high confidence matches
    print("\nHigh confidence matches (≥0.7):")
    for column in results:
        best_match = results.get_best_for_column(column)
        if best_match and best_match.confidence > 0.7:
            print(f"  {column}: {best_match.label} ({best_match.confidence:.3f})")

    return results


def generate_reports(results_list, dataset_names):
    """Generate comprehensive reports for all datasets."""
    print("\n=== Generating Reports ===")

    # Initialize report generator
    report_generator = ReportGenerator(output_dir="./reports")

    # Generate individual reports
    for _, (results, name) in enumerate(zip(results_list, dataset_names)):
        print(f"\nGenerating reports for {name} dataset...")

        # PDF report
        pdf_path = report_generator.generate_pdf_report(
            results=results,
            filename=f"{name.lower().replace(' ', '_')}_analysis.pdf",
            include_details=True,
            include_summary=True,
        )
        print(f"  ✓ PDF: {pdf_path}")

        # JSON report
        json_path = report_generator.generate_json_report(
            results=results, filename=f"{name.lower().replace(' ', '_')}_analysis.json"
        )
        print(f"  ✓ JSON: {json_path}")

    # Generate combined report
    print("\nGenerating combined comprehensive report...")
    all_columns = []
    for results in results_list:
        all_columns.extend(results.keys())

    combined_results = cs.analyze_columns(list(set(all_columns)), include_summary=True)

    combined_pdf = report_generator.generate_pdf_report(
        results=combined_results,
        filename="combined_comprehensive_analysis.pdf",
        include_details=True,
        include_summary=True,
    )
    print(f"  ✓ Combined PDF: {combined_pdf}")


def provide_recommendations(results_list, dataset_names):
    """Provide practical recommendations for all datasets."""
    print("\n=== Practical Recommendations ===")

    for results, name in zip(results_list, dataset_names):
        print(f"\n--- {name} Dataset ---")

        # Key column types and recommendations
        id_columns = results.get_columns_with_type("identifier")
        monetary_columns = results.get_columns_with_type("monetary_amount")
        date_columns = results.get_columns_with_type("date")
        email_columns = results.get_columns_with_type("email")

        if id_columns:
            print(f"  Primary Key Candidates: {', '.join(id_columns)}")

        if monetary_columns:
            print(f"  Monetary Columns: {', '.join(monetary_columns)}")
            print("    → Use DECIMAL type for precision")

        if date_columns:
            print(f"  Date Columns: {', '.join(date_columns)}")
            print("    → Use ISO 8601 format")

        if email_columns:
            print(f"  Email Columns: {', '.join(email_columns)}")
            print("    → Implement validation and encryption")


def main():
    """Complete analysis example combining all features."""

    print("Column Semantics - Complete Analysis Example")
    print("=" * 50)

    # Define datasets
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

    user_management_columns = [
        "user_id",
        "username",
        "email_address",
        "first_name",
        "last_name",
        "date_of_birth",
        "registration_date",
        "last_login",
        "is_verified",
        "phone_number",
        "address",
        "city",
        "country",
        "postal_code",
    ]

    inventory_columns = [
        "product_id",
        "product_name",
        "sku",
        "category",
        "brand",
        "price",
        "stock_quantity",
        "reorder_level",
        "supplier_id",
        "created_date",
        "updated_date",
        "is_active",
    ]

    # Analyze all datasets
    datasets = [
        (ecommerce_columns, "E-commerce"),
        (financial_columns, "Financial"),
        (user_management_columns, "User Management"),
        (inventory_columns, "Inventory"),
    ]

    results_list = []
    dataset_names = []

    for columns, name in datasets:
        results = analyze_dataset(columns, name)
        results_list.append(results)
        dataset_names.append(name)

    # Generate reports
    generate_reports(results_list, dataset_names)

    # Provide recommendations
    provide_recommendations(results_list, dataset_names)

    # Summary statistics
    print("\n=== Summary Statistics ===")
    total_columns = sum(results.count for results in results_list)
    total_hypotheses = sum(results.total_hypotheses for results in results_list)
    avg_confidence = sum(results.average_confidence for results in results_list) / len(
        results_list
    )
    all_semantic_types = set()
    for results in results_list:
        all_semantic_types.update(results.semantic_types)

    print(f"Total datasets analyzed: {len(datasets)}")
    print(f"Total columns analyzed: {total_columns}")
    print(f"Total hypotheses generated: {total_hypotheses}")
    print(f"Average confidence across all datasets: {avg_confidence:.3f}")
    print(f"Unique semantic types identified: {len(all_semantic_types)}")
    print(f"Semantic types: {', '.join(sorted(all_semantic_types))}")

    print("\n" + "=" * 50)
    print("Complete analysis finished successfully!")
    print("Check the './reports' directory for generated reports.")


if __name__ == "__main__":
    main()
