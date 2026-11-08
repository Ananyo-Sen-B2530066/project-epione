from pathlib import Path

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import landscape, letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    BaseDocTemplate,
    Frame,
    PageBreak,
    PageTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[2]
PDF_PATH = ROOT / "output" / "pdf" / "EDA_Column_Audit.pdf"


ROWS = [
    (1, "encounter_id", "EDA", "Checked for missing values and duplicates. Confirmed unique across all 101,766 encounters; used to align and join all six files.", "encounter_id (preserved as join key)"),
    (1, "num_medications", "EDA", "Checked missingness, unique values, summary statistics, frequency/distribution, and box plot.", "num_medications"),
    (1, "metformin-pioglitazone", "EDA", "Checked category counts and plotted category frequencies. Rare medication status retained because it is not constant.", "metformin-pioglitazone"),
    (1, "diabetesMed", "EDA", "Checked category counts and plotted the Yes/No frequency distribution.", "diabetesMed"),
    (1, "metformin-rosiglitazone", "EDA", "Checked category counts and plotted category frequencies. Rare non-No values retained.", "metformin-rosiglitazone"),
    (1, "diag_1", "EDA", "Diagnosis code kept as text. Checked missingness, code frequencies, and top diagnosis codes; source '?' was treated as missing and labeled Unknown for analysis.", "diag_1; diag_1_missing"),
    (1, "glimepiride", "EDA", "Checked medication-status counts and plotted category frequencies.", "glimepiride"),
    (1, "chlorpropamide", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "chlorpropamide"),
    (1, "nateglinide", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "nateglinide"),
    (1, "tolbutamide", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "tolbutamide"),
    (2, "encounter_id", "EDA", "Checked for missing values and duplicates. Confirmed unique and aligned with the other splits.", "encounter_id (preserved as join key)"),
    (2, "diag_3", "EDA", "Diagnosis code kept as text. Checked missingness, code frequencies, and top diagnosis codes; source '?' was treated as missing and labeled Unknown for analysis.", "diag_3; diag_3_missing"),
    (2, "num_procedures", "EDA", "Checked missingness, unique values, descriptive statistics, frequency/distribution, box plot, and numeric correlation with other measures in this split.", "num_procedures"),
    (2, "weight", "DROP", "Dropped because 98,569 of 101,766 values were missing (96.86%); too sparse for reliable use in this split.", ""),
    (2, "acarbose", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "acarbose"),
    (2, "time_in_hospital", "EDA", "Checked missingness, unique values, descriptive statistics, frequency/distribution, box plot, and correlation with other numeric measures.", "time_in_hospital"),
    (2, "age", "DROP", "Source age band was expanded into numeric lower and upper bounds, then the original interval text was removed.", "age_min; age_max"),
    (2, "discharge_disposition_id", "EDA", "Checked missingness, category counts, unique codes, and category-frequency plot. IDs remain codes; no unsupported labels were inferred.", "discharge_disposition_id"),
    (2, "insulin", "EDA", "Checked medication-status counts and plotted category frequencies.", "insulin"),
    (3, "encounter_id", "EDA", "Checked for missing values and duplicates. Confirmed unique and aligned with the other splits.", "encounter_id (preserved as join key)"),
    (3, "glyburide-metformin", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "glyburide-metformin"),
    (3, "change", "EDA", "Checked category counts and plotted whether medication changes were recorded.", "change"),
    (3, "number_emergency", "EDA", "Checked missingness, unique values, descriptive statistics, frequency/distribution, box plot, and correlation with inpatient visits.", "number_emergency"),
    (3, "payer_code", "EDA", "Checked missingness and payer-code frequencies. Source '?' was treated as missing and labeled Unknown for analysis.", "payer_code; payer_code_missing"),
    (3, "number_inpatient", "EDA", "Checked missingness, unique values, descriptive statistics, frequency/distribution, box plot, and correlation with emergency visits.", "number_inpatient"),
    (3, "repaglinide", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "repaglinide"),
    (3, "rosiglitazone", "EDA", "Checked medication-status counts and plotted category frequencies.", "rosiglitazone"),
    (3, "glyburide", "EDA", "Checked medication-status counts and plotted category frequencies.", "glyburide"),
    (4, "encounter_id", "EDA", "Checked for missing values and duplicates. Confirmed unique and aligned with the other splits.", "encounter_id (preserved as join key)"),
    (4, "patient_nbr", "EDA", "Checked identifier completeness and distinct-patient count. Preserved because many encounters can belong to the same patient.", "patient_nbr"),
    (4, "glimepiride-pioglitazone", "EDA", "Checked medication-status counts and plotted category frequencies. Rare status retained.", "glimepiride-pioglitazone"),
    (4, "pioglitazone", "EDA", "Checked medication-status counts and plotted category frequencies.", "pioglitazone"),
    (4, "admission_type_id", "EDA", "Checked missingness, unique codes, category counts, and category-frequency plot. Kept as an ID code.", "admission_type_id"),
    (4, "glipizide", "EDA", "Checked medication-status counts and plotted category frequencies.", "glipizide"),
    (4, "num_lab_procedures", "EDA", "Checked missingness, unique values, descriptive statistics, frequency/distribution, and box plot.", "num_lab_procedures"),
    (4, "troglitazone", "EDA", "Checked medication-status counts and plotted category frequencies. Rare status retained.", "troglitazone"),
    (4, "race", "EDA", "Checked missingness and category distribution. Source '?' was treated as missing and labeled Unknown for analysis.", "race; race_missing"),
    (5, "encounter_id", "EDA", "Checked for missing values and duplicates. Confirmed unique and aligned with the other splits.", "encounter_id (preserved as join key)"),
    (5, "max_glu_serum", "EDA", "Checked category distribution and source missingness. Missing means no recorded result; labeled Not measured and retained a missingness flag.", "max_glu_serum; max_glu_serum_missing"),
    (5, "gender", "EDA", "Checked category counts and plotted frequencies. Normalized Unknown/Invalid to Unknown.", "gender"),
    (5, "tolazamide", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "tolazamide"),
    (5, "miglitol", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "miglitol"),
    (5, "metformin", "EDA", "Checked medication-status counts and plotted category frequencies.", "metformin"),
    (5, "citoglipton", "DROP", "Dropped because every encounter had the same value (No); a constant feature has no variation for analysis or prediction.", ""),
    (5, "medical_specialty", "EDA", "Checked missingness and specialty frequencies. Source '?' was treated as missing and labeled Unknown for analysis.", "medical_specialty; medical_specialty_missing"),
    (5, "A1Cresult", "EDA", "Checked category distribution and source missingness. Missing means no recorded result; labeled Not measured and retained a missingness flag.", "A1Cresult; A1Cresult_missing"),
    (6, "encounter_id", "EDA", "Checked for missing values and duplicates. Confirmed unique and aligned with the other splits.", "encounter_id (preserved as join key)"),
    (6, "diag_2", "EDA", "Diagnosis code kept as text. Checked missingness, code frequencies, and top diagnosis codes; source '?' was treated as missing and labeled Unknown for analysis.", "diag_2; diag_2_missing"),
    (6, "readmitted", "EDA", "Checked outcome category counts and plotted readmission frequencies; compared diagnosis counts and prior outpatient visits by readmission group.", "readmitted"),
    (6, "number_diagnoses", "EDA", "Checked missingness, unique values, descriptive statistics, frequency/distribution, box plot, numeric correlation, and grouped summaries by readmission outcome.", "number_diagnoses"),
    (6, "admission_source_id", "EDA", "Checked missingness, unique codes, category counts, and category-frequency plot. Kept as an ID code.", "admission_source_id"),
    (6, "glipizide-metformin", "EDA", "Checked medication-status counts and plotted category frequencies. Rare statuses retained.", "glipizide-metformin"),
    (6, "number_outpatient", "EDA", "Checked missingness, unique values, descriptive statistics, frequency/distribution, box plot, correlation, and grouped summaries by readmission outcome.", "number_outpatient"),
    (6, "acetohexamide", "EDA", "Checked medication-status counts and plotted category frequencies. Rare status retained because it is not constant.", "acetohexamide"),
    (6, "examide", "DROP", "Dropped because every encounter had the same value (No); a constant feature has no variation for analysis or prediction.", ""),
]


def footer(canvas, doc):
    canvas.saveState()
    width, _ = landscape(letter)
    canvas.setStrokeColor(colors.HexColor("#D6DEE8"))
    canvas.line(0.42 * inch, 0.40 * inch, width - 0.42 * inch, 0.40 * inch)
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(colors.HexColor("#526174"))
    canvas.drawString(0.45 * inch, 0.23 * inch, "Diabetes encounter dataset | Column-level EDA and cleaning record")
    canvas.drawRightString(width - 0.45 * inch, 0.23 * inch, f"Page {doc.page}")
    canvas.restoreState()


def build_pdf():
    PDF_PATH.parent.mkdir(parents=True, exist_ok=True)
    page = landscape(letter)
    doc = BaseDocTemplate(
        str(PDF_PATH),
        pagesize=page,
        rightMargin=0.42 * inch,
        leftMargin=0.42 * inch,
        topMargin=0.52 * inch,
        bottomMargin=0.55 * inch,
        title="Diabetes Dataset EDA and Cleaning by Column",
        author="OpenAI Codex",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="main")
    doc.addPageTemplates([PageTemplate(id="all", frames=[frame], onPage=footer)])

    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="ReportTitle", parent=styles["Title"], fontName="Helvetica-Bold", fontSize=18, leading=22, alignment=TA_LEFT, textColor=colors.HexColor("#17324D"), spaceAfter=5))
    styles.add(ParagraphStyle(name="SubTitle", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#526174"), spaceAfter=7))
    styles.add(ParagraphStyle(name="Cell", parent=styles["BodyText"], fontName="Helvetica", fontSize=7.4, leading=9, alignment=TA_LEFT, textColor=colors.HexColor("#1E293B")))
    styles.add(ParagraphStyle(name="CellSmall", parent=styles["Cell"], fontSize=7, leading=8.4))
    styles.add(ParagraphStyle(name="Header", parent=styles["Cell"], fontName="Helvetica-Bold", fontSize=8, leading=9, textColor=colors.white))
    styles.add(ParagraphStyle(name="Section", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=11, leading=13, textColor=colors.HexColor("#17324D"), spaceBefore=7, spaceAfter=4))

    story = [
        Paragraph("EDA and Data Cleaning by Column", styles["ReportTitle"]),
        Paragraph("Six encounter-level CSV splits | 101,766 records per split | Final joined dataset: 101,766 rows and 56 columns", styles["SubTitle"]),
        Paragraph("How to read this report", styles["Section"]),
        Paragraph("Each source feature is listed once per split. EDA means the feature was inspected and, where appropriate, summarized or plotted. DROP means the source feature was removed from the cleaned output. The last column lists the resulting field names; blank cells indicate a dropped field.", styles["Cell"]),
        Spacer(1, 6),
        Paragraph("Cleaning decisions", styles["Section"]),
        Paragraph("The literal '?' was read as missing. Diagnosis codes and other category codes were kept as text/codes. Missing diagnosis, payer, and race entries were labeled Unknown for analysis while a *_missing indicator preserves the missingness. Missing glucose/A1C test results were labeled Not measured with indicators. Age intervals were split into lower and upper bounds. Weight was dropped at 96.86% missingness. Constant citoglipton and examide were dropped. No rows were removed; no duplicate rows or encounter_id keys were found.", styles["Cell"]),
        Spacer(1, 6),
        Paragraph("Near-constant medication features were retained because their rare non-No values still vary and may carry predictive information. The diagnosis code meanings are not expanded in the cleaned file; no code descriptions are implied by this report.", styles["Cell"]),
        Spacer(1, 8),
    ]

    header = [Paragraph("Feature / column name", styles["Header"]), Paragraph("EDA or DROP", styles["Header"]), Paragraph("Description", styles["Header"]), Paragraph("Inference / output", styles["Header"])]
    for split in range(1, 7):
        split_rows = [record for record in ROWS if record[0] == split]
        if split > 1:
            story.append(PageBreak())
        story.append(Paragraph(f"Dataset {split} columns", styles["Section"]))
        data = [header]
        for _, column, action, description, output in split_rows:
            data.append([
                Paragraph(f"<b>{column}</b>", styles["CellSmall"]),
                Paragraph(action, styles["CellSmall"]),
                Paragraph(description, styles["CellSmall"]),
                Paragraph(output.replace("; ", "<br/>"), styles["CellSmall"]),
            ])
        table = Table(data, colWidths=[1.5 * inch, 0.75 * inch, 5.2 * inch, 2.15 * inch], repeatRows=1, hAlign="LEFT", splitByRow=0)
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#17324D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("LEFTPADDING", (0, 0), (-1, -1), 5),
            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
            ("TOPPADDING", (0, 0), (-1, -1), 4),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.HexColor("#9FB2C7")),
            ("LINEBELOW", (0, 1), (-1, -1), 0.25, colors.HexColor("#D6DEE8")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FB")]),
        ]))
        for row_index, record in enumerate(split_rows, start=1):
            if record[2] == "DROP":
                table.setStyle(TableStyle([("TEXTCOLOR", (1, row_index), (1, row_index), colors.HexColor("#A33A32")), ("FONTNAME", (1, row_index), (1, row_index), "Helvetica-Bold")]))
        story.append(table)
    story += [Spacer(1, 8), Paragraph("Output files", styles["Section"]), Paragraph("Cleaned split files and EDA notebooks are in the project. The joined output is EDA_Dataset/EDA_Full_Dataset.csv. The join uses encounter_id with one-to-one validation.", styles["Cell"])]
    doc.build(story)


if __name__ == "__main__":
    build_pdf()
    print(PDF_PATH)
