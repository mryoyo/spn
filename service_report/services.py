import io
from reportlab.pdfgen import canvas

# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont

# pdfmetrics.registerFont(TTFont('Vera', 'Vera.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBd', 'VeraBd.ttf'))
# pdfmetrics.registerFont(TTFont('VeraIt', 'VeraIt.ttf'))
# pdfmetrics.registerFont(TTFont('VeraBI', 'VeraBI.ttf'))

# canvas.setFont('Vera', 32)
# canvas.drawString(10, 150, "Some text encoded in UTF-8")
# canvas.drawString(10, 100, "In the Vera TT Font!")


class PDFService:

    page_size = "a4"  # "a4" or "a4_landscape"
    title = "Hello Report !!"

    def get_buffer(self):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
        p.setTitle(self.title)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.setTitle(self.title)
        p.drawString(250, 800, "SAMPLE REPORT")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return buffer
