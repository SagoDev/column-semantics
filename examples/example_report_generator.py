"""Example usage of the report generator."""

from column_semantics import analyze_columns
from column_semantics.core.reporter_generator import ReportGenerator


def main():
    """Example demonstrating report generation."""

    # Sample columns to analyze
    columns = [
        "user_id",
        "created_at",
        "amount_usd",
        "is_active",
        "email_address",
        "phone_number",
        "first_name",
        "last_name",
        "order_date",
        "total_price",
        "customer_id",
        "product_name",
    ]

    # Analyze columns
    print("Analyzing columns...")
    results = analyze_columns(columns, include_summary=True)

    # Create report generator
    generator = ReportGenerator(output_dir="./reports")

    # Generate PDF report
    print("Generating PDF report...")
    pdf_path = generator.generate_pdf_report(
        results=results,
        filename="sample_analysis.pdf",
        include_details=True,
        include_summary=True,
        include_charts=False,
    )
    print(f"PDF report saved to: {pdf_path}")

    # Generate JSON report
    print("Generating JSON report...")
    json_path = generator.generate_json_report(
        results=results, filename="sample_analysis.json"
    )
    print(f"JSON report saved to: {json_path}")

    # Generate text report
    print("Generating text report...")
    text_path = generator.generate_text_report(
        results=results, filename="sample_analysis.txt"
    )
    print(f"Text report saved to: {text_path}")

    # Print summary to console
    print("\n" + "=" * 50)
    print("ANALYSIS SUMMARY")
    print("=" * 50)
    print(results.get_summary_text())


if __name__ == "__main__":
    main()
