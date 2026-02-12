"""PDF Report Generator using ReportLab."""

from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Any, Dict

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.platypus.frames import Frame
from reportlab.platypus.doctemplate import PageTemplate, BaseDocTemplate

from column_semantics.core.analysis.analysis_results import ColumnAnalysisResults


class PDFReporter:
    """Generates PDF reports using ReportLab."""

    def __init__(self, page_size=A4):
        """Initialize PDF reporter.
        
        Args:
            page_size: Page size for the PDF. Defaults to A4.
        """
        self.page_size = page_size
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()

    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Center
            textColor=colors.darkblue,
        ))

        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            spaceAfter=12,
            spaceBefore=20,
            textColor=colors.darkblue,
        ))

        # Subsection style
        self.styles.add(ParagraphStyle(
            name='Subsection',
            parent=self.styles['Heading3'],
            fontSize=12,
            spaceAfter=8,
            spaceBefore=15,
            textColor=colors.darkgreen,
        ))

    def create_report(
        self,
        results: ColumnAnalysisResults,
        output_path: Path,
        include_details: bool = True,
        include_summary: bool = True,
        include_charts: bool = False,
    ):
        """Create a PDF report from analysis results.
        
        Args:
            results: ColumnAnalysisResults object
            output_path: Path where to save the PDF
            include_details: Whether to include detailed column analysis
            include_summary: Whether to include summary statistics
            include_charts: Whether to include charts (placeholder)
        """
        doc = SimpleDocTemplate(
            str(output_path),
            pagesize=self.page_size,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )

        story = []

        # Title page
        self._add_title_page(story, results)
        
        # Executive summary
        if include_summary:
            story.append(PageBreak())
            self._add_executive_summary(story, results)

        # Detailed analysis
        if include_details:
            story.append(PageBreak())
            self._add_detailed_analysis(story, results)

        # Charts section (placeholder)
        if include_charts:
            story.append(PageBreak())
            self._add_charts_section(story, results)

        doc.build(story)

    def _add_title_page(self, story: list, results: ColumnAnalysisResults):
        """Add title page to the report."""
        story.append(Paragraph("Column Semantics Analysis Report", self.styles['CustomTitle']))
        story.append(Spacer(1, 0.5 * inch))
        
        # Report metadata
        metadata_data = [
            ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
            ['Total Columns:', str(results.count)],
            ['Total Hypotheses:', str(results.total_hypotheses)],
            ['Semantic Types Found:', str(len(results.semantic_types))],
            ['Average Confidence:', f'{results.average_confidence:.3f}'],
        ]
        
        metadata_table = Table(metadata_data, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (0, -1), colors.lightgrey),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        story.append(metadata_table)
        story.append(Spacer(1, 1 * inch))

    def _add_executive_summary(self, story: list, results: ColumnAnalysisResults):
        """Add executive summary section."""
        story.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        # Key statistics
        stats_text = f"""
        This report presents the semantic analysis of {results.count} column names. 
        The analysis generated {results.total_hypotheses} hypotheses across 
        {len(results.semantic_types)} distinct semantic types with an average 
        confidence of {results.average_confidence:.3f}.
        """
        
        story.append(Paragraph(stats_text, self.styles['Normal']))
        story.append(Spacer(1, 0.3 * inch))

        # Semantic distribution table
        if results.semantic_distribution:
            story.append(Paragraph("Semantic Type Distribution", self.styles['Subsection']))
            
            dist_data = [['Semantic Type', 'Count', 'Percentage']]
            for sem_type, count in sorted(results.semantic_distribution.items(), key=lambda x: x[1], reverse=True):
                percentage = (count / results.total_hypotheses) * 100
                dist_data.append([sem_type, str(count), f'{percentage:.1f}%'])
            
            dist_table = Table(dist_data, colWidths=[3*inch, 1*inch, 1*inch])
            dist_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(dist_table)
            story.append(Spacer(1, 0.3 * inch))

        # High confidence findings
        high_conf = results.high_confidence_hypotheses
        if high_conf:
            story.append(Paragraph("High Confidence Findings (≥0.7)", self.styles['Subsection']))
            
            high_conf_text = f"""
            Found {len(high_conf)} high-confidence hypotheses. These represent the most 
            reliable semantic inferences from the analysis and are recommended for 
            immediate implementation in data governance workflows.
            """
            
            story.append(Paragraph(high_conf_text, self.styles['Normal']))
            story.append(Spacer(1, 0.3 * inch))

    def _add_detailed_analysis(self, story: list, results: ColumnAnalysisResults):
        """Add detailed column analysis section."""
        story.append(Paragraph("Detailed Column Analysis", self.styles['SectionHeader']))
        
        for col_name in results:
            story.append(Paragraph(f"Column: {col_name}", self.styles['Subsection']))
            
            best = results.get_best_for_column(col_name)
            all_hyps = results.get_all_for_column(col_name)
            
            if best:
                # Best hypothesis details
                best_data = [
                    ['Best Match:', best.label],
                    ['Confidence:', f'{best.confidence:.3f}'],
                    ['Rule Description:', best.rule.description],
                    ['Rule Priority:', str(best.rule.priority)],
                ]
                
                if best.rule.recommended_treatment:
                    best_data.append(['Recommendations:', ', '.join(best.rule.recommended_treatment)])
                
                best_table = Table(best_data, colWidths=[1.5*inch, 4.5*inch])
                best_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (0, -1), colors.lightblue),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
                    ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
                    ('FONTSIZE', (0, 0), (-1, -1), 9),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(best_table)
                story.append(Spacer(1, 0.2 * inch))
            
            # All hypotheses table
            if len(all_hyps) > 1:
                story.append(Paragraph("All Hypotheses:", self.styles['Normal']))
                
                hyp_data = [['Rank', 'Semantic Type', 'Confidence', 'Rule']]
                for i, hyp in enumerate(sorted(all_hyps, key=lambda h: h.confidence, reverse=True), 1):
                    hyp_data.append([
                        str(i),
                        hyp.label,
                        f'{hyp.confidence:.3f}',
                        hyp.rule.label
                    ])
                
                hyp_table = Table(hyp_data, colWidths=[0.5*inch, 2*inch, 1*inch, 2.5*inch])
                hyp_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, -1), 8),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
                ]))
                
                story.append(hyp_table)
            
            story.append(Spacer(1, 0.3 * inch))

    def _add_charts_section(self, story: list, results: ColumnAnalysisResults):
        """Add charts section (placeholder for future implementation)."""
        story.append(Paragraph("Visual Analysis", self.styles['SectionHeader']))
        
        charts_text = """
        Visual charts and graphs will be included in future versions of this report.
        This section will contain:
        - Bar charts showing semantic type distribution
        - Confidence level histograms
        - Column similarity heatmaps
        - Temporal analysis trends
        """
        
        story.append(Paragraph(charts_text, self.styles['Normal']))