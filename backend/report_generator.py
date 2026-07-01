from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4


def generate_report(filename, data, code):

    doc = SimpleDocTemplate(filename, pagesize=A4)
    styles = getSampleStyleSheet()

    content = []

    content.append(Paragraph("Compiler Front-End System Report", styles["Title"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Source Code", styles["Heading2"]))
    content.append(Paragraph(str(code), styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Tokens", styles["Heading2"]))
    content.append(Paragraph(str(data.get("tokens", [])), styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Symbol Table", styles["Heading2"]))
    content.append(Paragraph(str(data.get("symbol_table", [])), styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("AST", styles["Heading2"]))
    content.append(Paragraph(str(data.get("ast", {})), styles["BodyText"]))
    content.append(Spacer(1, 12))

    content.append(Paragraph("Semantic Analysis", styles["Heading2"]))
    content.append(Paragraph(str(data.get("semantic", {})), styles["BodyText"]))

    doc.build(content)

    return filename