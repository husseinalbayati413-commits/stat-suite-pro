"""
PDF Report Generator
Uses ReportLab to produce a professional analysis report.
"""
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak



def _styles():
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(
        name="MainTitle",
        parent=styles["Title"],
        fontSize=22,
        textColor=colors.HexColor("#1f2937"),
        alignment=1,
        spaceAfter=12,
    ))
    styles.add(ParagraphStyle(
        name="Section",
        parent=styles["Heading1"],
        fontSize=15,
        textColor=colors.HexColor("#4f46e5"),
        spaceBefore=12,
        spaceAfter=8,
    ))
    styles.add(ParagraphStyle(
        name="Sub",
        parent=styles["Heading2"],
        fontSize=12,
        textColor=colors.HexColor("#334155"),
        spaceBefore=8,
        spaceAfter=4,
    ))
    styles.add(ParagraphStyle(
        name="Body2",
        parent=styles["BodyText"],
        fontSize=10,
        leading=14,
    ))
    return styles



def build_pdf_report(project_name: str, filename: str, df_summary: dict, results_log: list, figures: list = None) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        title=f"Stat Suite Pro Report - {project_name}",
    )
    styles = _styles()
    story = []

    story.append(Spacer(1, 2.5 * cm))
    story.append(Paragraph("Stat Suite Pro", styles["MainTitle"]))
    story.append(Paragraph("Professional Statistical Analysis Report", styles["MainTitle"]))
    story.append(Spacer(1, 1.3 * cm))

    cover_data = [
        ["Project Name", project_name],
        ["Dataset", filename or "—"],
        ["Generated", datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        ["Rows x Cols", f"{df_summary.get('rows', '—')} x {df_summary.get('cols', '—')}"],
        ["Total Results", str(len(results_log))],
    ]
    cover_table = Table(cover_data, colWidths=[5 * cm, 9 * cm])
    cover_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#4f46e5")),
        ("TEXTCOLOR", (0, 0), (0, -1), colors.white),
        ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),
        ("FONTSIZE", (0, 0), (-1, -1), 11),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ("TOPPADDING", (0, 0), (-1, -1), 10),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
    ]))
    story.append(cover_table)
    story.append(PageBreak())

    story.append(Paragraph("1. Dataset Overview", styles["Section"]))
    info_text = (
        f"<b>Rows:</b> {df_summary.get('rows','—')} &nbsp;&nbsp;"
        f"<b>Columns:</b> {df_summary.get('cols','—')} <br/>"
        f"<b>Numeric:</b> {df_summary.get('numeric_cols','—')} &nbsp;&nbsp;"
        f"<b>Categorical:</b> {df_summary.get('categorical_cols','—')} <br/>"
        f"<b>Missing values:</b> {df_summary.get('missing','—')}"
    )
    story.append(Paragraph(info_text, styles["Body2"]))
    story.append(Spacer(1, 0.4 * cm))

    desc = df_summary.get("describe")
    if desc is not None and not desc.empty:
        story.append(Paragraph("Descriptive Statistics", styles["Sub"]))
        table_data = [["Statistic"] + list(desc.columns)]
        for idx in desc.index:
            row = [str(idx)] + [f"{v:.3f}" if isinstance(v, (int, float)) else str(v) for v in desc.loc[idx]]
            table_data.append(row)
        desc_table = Table(table_data, repeatRows=1)
        desc_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#4f46e5")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTSIZE", (0, 0), (-1, -1), 8),
            ("GRID", (0, 0), (-1, -1), 0.3, colors.grey),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f8fafc")]),
        ]))
        story.append(desc_table)

    story.append(PageBreak())
    story.append(Paragraph("2. Analysis Results", styles["Section"]))
    if not results_log:
        story.append(Paragraph("No analyses have been recorded yet.", styles["Body2"]))
    else:
        for i, result in enumerate(results_log, 1):
            story.append(Paragraph(f"{i}. [{result['category']}] {result['title']}", styles["Sub"]))
            story.append(Paragraph(f"<i>{result['timestamp']}</i>", styles["Body2"]))
            rows = [[str(k), str(v)] for k, v in result["content"].items()]
            result_table = Table(rows or [["Info", "No content"]], colWidths=[6 * cm, 9 * cm])
            result_table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#eef2ff")),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#cbd5e1")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ]))
            story.append(result_table)
            story.append(Spacer(1, 0.25 * cm))

    if figures:
        story.append(PageBreak())
        story.append(Paragraph("3. Visualizations", styles["Section"]))
        for fig_obj in figures:
            try:
                img_buf = BytesIO()
                fig_obj["fig"].savefig(img_buf, format="PNG", bbox_inches="tight", dpi=120)
                img_buf.seek(0)
                story.append(Paragraph(fig_obj["name"], styles["Sub"]))
                story.append(Image(img_buf, width=15 * cm, height=9 * cm))
                story.append(Spacer(1, 0.3 * cm))
            except Exception:
                continue

    story.append(PageBreak())
    story.append(Spacer(1, 8 * cm))
    story.append(Paragraph(
        "Generated by Stat Suite Pro using Pandas, SciPy, statsmodels, scikit-learn, Plotly and Streamlit.",
        styles["Body2"],
    ))

    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
