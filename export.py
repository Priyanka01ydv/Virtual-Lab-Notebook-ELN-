from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors

def export_to_pdf(filename, entries):
    doc = SimpleDocTemplate(filename, pagesize=(8.5*inch, 11*inch))
    styles = getSampleStyleSheet()
    
    dreamy_title = ParagraphStyle(
        'DreamyTitle',
        parent=styles['Heading1'],
        alignment=TA_CENTER,
        fontSize=18,
        textColor=colors.HexColor("#6A5ACD"), # dreamy lavender
        spaceAfter=20
    )
    dreamy_body = ParagraphStyle(
        'DreamyBody',
        parent=styles['Normal'],
        fontSize=12,
        textColor=colors.HexColor("#333333"),
        spaceAfter=12
    )
    dreamy_category = ParagraphStyle(
        'DreamyCategory',
        parent=styles['Heading2'],
        fontSize=14,
        textColor=colors.HexColor("#FF69B4"), # soft pink
        spaceAfter=10
    )

    story = []
    story.append(Paragraph("Virtual Lab Notebook 📓", dreamy_title))
    story.append(Spacer(1, 12))

    for entry in entries:
        title, date, category, content = entry
        story.append(Paragraph(f"{title} ({date})", dreamy_category))
        story.append(Paragraph(f"<b>Category:</b> {category}", dreamy_body))
        story.append(Paragraph(content.replace("\n", "<br/>"), dreamy_body))
        story.append(Spacer(1, 20))

    doc.build(story)
