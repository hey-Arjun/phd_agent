from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from textwrap import wrap
import os
from datetime import datetime


def draw_wrapped_text(c, text, x, y, max_chars=90, line_height=15):

    lines = wrap(str(text), max_chars)

    for line in lines:
        c.drawString(x, y, line)
        y -= line_height

    return y


def generate_pdf(all_results):

    os.makedirs("data", exist_ok=True)

    # Create timestamp filename
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
    output_path = f"data/PhD_Report_{timestamp}.pdf"

    c = canvas.Canvas(output_path, pagesize=letter)

    y = 750

    c.setFont("Helvetica-Bold", 20)
    c.drawString(50, y, "Research Report")

    y -= 30

    c.setFont("Helvetica", 11)
    c.drawString(50, y, f"Generated on: {datetime.now().strftime('%d %B %Y %H:%M')}")

    y -= 40

    for phd_data in all_results:

        if y < 120:
            c.showPage()
            y = 750

        c.setFont("Helvetica-Bold", 16)

        y = draw_wrapped_text(
            c,
            f"University: {phd_data.get('university','Not found')}",
            50,
            y
        )

        c.setFont("Helvetica", 12)

        fields = [
            ("Country", phd_data.get("country")),
            ("PhD Program", phd_data.get("phd_program")),
            ("Funding", phd_data.get("funding")),
            ("Tuition Fees", phd_data.get("tuition_fees")),
            ("Requirements", phd_data.get("requirements")),
            ("Application Deadline", phd_data.get("application_deadline")),
            ("Application Link", phd_data.get("application_link")),
            ("Source URL", phd_data.get("source_url")),
        ]

        for title, value in fields:

            text = f"{title}: {value}"

            y = draw_wrapped_text(c, text, 60, y)

            y -= 5

        y -= 20

    c.save()

    return output_path