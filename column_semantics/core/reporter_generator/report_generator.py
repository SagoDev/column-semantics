"""Report Generator for converting analysis results to PDF reports."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

from column_semantics.core.analysis.analysis_results import ColumnAnalysisResults
from column_semantics.core.reporter_generator.pdf_generator import PDFReporter


class ReportGenerator:
    """Generates reports from column analysis results."""

    def __init__(self, output_dir: Optional[Path | str] = None):
        """Initialize the report generator.
        
        Args:
            output_dir: Directory where reports will be saved. Defaults to current directory.
        """
        self.output_dir = Path(output_dir) if output_dir else Path.cwd()
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def generate_pdf_report(
        self,
        results: ColumnAnalysisResults,
        filename: Optional[str] = None,
        include_details: bool = True,
        include_summary: bool = True,
        include_charts: bool = False,
    ) -> Path:
        """Generate a PDF report from analysis results.
        
        Args:
            results: ColumnAnalysisResults object to convert to PDF
            filename: Name of the PDF file. If None, auto-generates with timestamp.
            include_details: Whether to include detailed column analysis
            include_summary: Whether to include summary statistics
            include_charts: Whether to include charts (placeholder for future)
            
        Returns:
            Path to the generated PDF file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"column_analysis_report_{timestamp}.pdf"

        output_path = self.output_dir / filename

        pdf_reporter = PDFReporter()
        pdf_reporter.create_report(
            results=results,
            output_path=output_path,
            include_details=include_details,
            include_summary=include_summary,
            include_charts=include_charts,
        )

        return output_path

    def generate_json_report(
        self,
        results: ColumnAnalysisResults,
        filename: Optional[str] = None,
        indent: int = 2,
    ) -> Path:
        """Generate a JSON report from analysis results.
        
        Args:
            results: ColumnAnalysisResults object to convert to JSON
            filename: Name of the JSON file. If None, auto-generates with timestamp.
            indent: Number of spaces for JSON indentation
            
        Returns:
            Path to the generated JSON file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"column_analysis_report_{timestamp}.json"

        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(results.to_json(indent=indent))

        return output_path

    def generate_text_report(
        self,
        results: ColumnAnalysisResults,
        filename: Optional[str] = None,
        include_details: bool = True,
    ) -> Path:
        """Generate a text report from analysis results.
        
        Args:
            results: ColumnAnalysisResults object to convert to text
            filename: Name of the text file. If None, auto-generates with timestamp.
            include_details: Whether to include detailed column analysis
            
        Returns:
            Path to the generated text file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"column_analysis_report_{timestamp}.txt"

        output_path = self.output_dir / filename

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(self._format_text_report(results, include_details))

        return output_path

    def _format_text_report(
        self, results: ColumnAnalysisResults, include_details: bool
    ) -> str:
        """Format analysis results as text."""
        lines = [
            "COLUMN SEMANTICS ANALYSIS REPORT",
            "=" * 50,
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            "",
            "SUMMARY",
            "-" * 20,
            results.get_summary_text(),
            "",
        ]

        if include_details:
            lines.extend([
                "DETAILED ANALYSIS",
                "-" * 20,
                ""
            ])
            
            for col_name in results:
                best = results.get_best_for_column(col_name)
                all_hyps = results.get_all_for_column(col_name)
                
                lines.append(f"Column: {col_name}")
                lines.append("-" * len(f"Column: {col_name}"))
                
                if best:
                    lines.append(f"Best Match: {best.label}")
                    lines.append(f"Confidence: {best.confidence:.3f}")
                    lines.append(f"Rule: {best.rule.description}")
                    if best.rule.recommended_treatment:
                        lines.append(f"Recommendations: {', '.join(best.rule.recommended_treatment)}")
                else:
                    lines.append("No hypotheses found")
                
                if len(all_hyps) > 1:
                    lines.append("\nAll Hypotheses:")
                    for i, hyp in enumerate(all_hyps, 1):
                        lines.append(f"  {i}. {hyp.label} (confidence: {hyp.confidence:.3f})")
                
                lines.append("")

        return "\n".join(lines)