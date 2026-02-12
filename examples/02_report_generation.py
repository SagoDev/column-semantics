"""Report Generation Example

This example demonstrates how to generate comprehensive reports
from column analysis results using the ReportGenerator.
"""

import column_semantics as cs
from column_semantics.core.reporter_generator import ReportGenerator


def main():
    """Demonstrate report generation capabilities."""

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
    print("Analyzing e-commerce columns...")
    ecommerce_results = cs.analyze_columns(ecommerce_columns, include_summary=True)

    print("Analyzing financial columns...")
    financial_results = cs.analyze_columns(financial_columns, include_summary=True)

    # Initialize report generator
    print("\n=== Initializing Report Generator ===")
    report_generator = ReportGenerator(output_dir="./reports")

    # Generate PDF report for e-commerce analysis
    print("\nGenerating e-commerce analysis PDF...")
    pdf_path = report_generator.generate_pdf_report(
        results=ecommerce_results,
        filename="ecommerce_analysis_report.pdf",
        include_details=True,
        include_summary=True,
        include_charts=False,
    )
    print(f"  ✓ PDF report saved to: {pdf_path}")

    # Generate JSON report for financial analysis
    print("Generating financial analysis JSON...")
    json_path = report_generator.generate_json_report(
        results=financial_results, filename="financial_analysis_report.json"
    )
    print(f"  ✓ JSON report saved to: {json_path}")

    # Generate text report for e-commerce analysis
    print("Generating e-commerce analysis text report...")
    text_path = report_generator.generate_text_report(
        results=ecommerce_results, filename="ecommerce_analysis_report.txt"
    )
    print(f"  ✓ Text report saved to: {text_path}")

    # Generate comprehensive report combining both datasets
    print("\nGenerating comprehensive dataset report...")

    # Combine both datasets for comprehensive analysis
    all_columns = ecommerce_columns + financial_columns
    combined_results = cs.analyze_columns(all_columns, include_summary=True)

    comprehensive_pdf = report_generator.generate_pdf_report(
        results=combined_results,
        filename="comprehensive_analysis_report.pdf",
        include_details=True,
        include_summary=True,
    )
    print(f"  ✓ Comprehensive PDF report saved to: {comprehensive_pdf}")

    # Demonstrate filtering capabilities
    print("\n=== Generating Filtered Reports ===")

    # Generate report with only high-confidence results
    high_confidence_results = ecommerce_results.filter_by_confidence(0.7)
    filtered_pdf = report_generator.generate_pdf_report(
        results=high_confidence_results,
        filename="high_confidence_analysis_report.pdf",
        include_details=True,
        include_summary=True,
    )
    print(f"  ✓ High confidence PDF report saved to: {filtered_pdf}")

    # Generate report with custom filename
    timestamp_pdf = report_generator.generate_pdf_report(
        results=financial_results,
        filename=None,  # Will auto-generate with timestamp
        include_details=True,
        include_summary=True,
    )
    print(f"  ✓ Timestamped PDF report saved to: {timestamp_pdf}")

    print("\n=== Report Generation Complete ===")
    print("All reports have been generated and saved to the './reports' directory.")
    print("\nGenerated reports:")
    print("  1. ecommerce_analysis_report.pdf - Full e-commerce analysis")
    print("  2. financial_analysis_report.json - Financial analysis in JSON format")
    print("  3. ecommerce_analysis_report.txt - E-commerce analysis in text format")
    print("  4. comprehensive_analysis_report.pdf - Combined datasets analysis")
    print("  5. high_confidence_analysis_report.pdf - High confidence results only")
    print("  6. Timestamped PDF report - Auto-generated filename")

    print("\nAnalysis Summary:")
    print(
        f"  E-commerce: {ecommerce_results.count} columns, {ecommerce_results.total_hypotheses} hypotheses"
    )
    print(
        f"  Financial: {financial_results.count} columns, {financial_results.total_hypotheses} hypotheses"
    )
    print(
        f"  Combined: {combined_results.count} columns, {combined_results.total_hypotheses} hypotheses"
    )


if __name__ == "__main__":
    main()
