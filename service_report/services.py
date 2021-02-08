import io
import copy

from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm, inch
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus.tables import LongTable, Table, TableStyle
from reportlab.lib.styles import ListStyle

_fonts = {
    "THSarabunNew": "service_report/THSarabunNew/THSarabunNew.ttf",
    "THSarabunNewBd": "service_report/THSarabunNew/THSarabunNew Bold.ttf",
    "THSarabunNewBI": "service_report/THSarabunNew/THSarabunNew BoldItalic.ttf",
    "THSarabunNewIt": "service_report/THSarabunNew/THSarabunNew Italic.ttf",
}
for font_name, font_path in _fonts.items():
    pdfmetrics.registerFont(TTFont(font_name, font_path))


styles = getSampleStyleSheet()
styles['title'].fontName = "THSarabunNewBd"
styles['Normal'].fontName = "THSarabunNew"
styles['h1'].fontName = "THSarabunNewBd"
styles['h2'].fontName = "THSarabunNewBd"


class PDFService:

    page_size = "a4"  # "a4" or "a4_landscape"
    title = "Hello Report !!"
    title_alignment = 1
    title_fontSize = 22
    default_fontSize = 12.5
    show_signature_footer = True
    signature_role_left = "ผู้จัดทำ"
    signature_role_right = "ผู้จัดการ"

    def get_title(self):
        style = copy.copy(styles['title'])
        style.alignment = self.title_alignment
        style.fontSize = self.title_fontSize
        return Paragraph(self.title, style=style)

    def get_subtitle(self):
        style = TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('FONT', (0, 0), (-1, -1), 'THSarabunNew'),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
        ])
        data = [
            ['สาขา', '', 'page 1 of 1'],
            ['สำหรับวันที่', 'ถึงวันที่']
        ]
        widths = [5 * cm, 10.5 * cm, 2.5 * cm]
        return Table(data, widths, 2 * [0.7 * cm], style=style, spaceBefore=0.6*cm)

    def get_date_range(self):
        style = copy.copy(styles['h2'])
        style.fontSize = 14
        return Paragraph("สำหรับวันที่ ......................... ถึงวันที่ .........................", style=style)

    def get_content(self):
        style = copy.copy(styles['title'])
        return Paragraph("No Content", style=style)

    def get_signature_footer(self):
        style = TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), self.default_fontSize),
            ('FONT', (0, 0), (-1, -1), 'THSarabunNew'),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
        ])
        name1_field = f"ลงชื่อ {20 * '...'} ({self.signature_role_left})"
        name2_field = f"ลงชื่อ {20 * '...'} ({self.signature_role_right})"
        date_field = f"วันที่ ({15 * '.'}/{15 * '.'}/{15 * '.'})"
        data = [[name1_field, name2_field], [date_field, date_field]]
        return Table(data, 2 * [3.5 * inch], 2 * [0.7 * cm], style=style, spaceBefore=1*cm)

    def create_table(self, col_name_and_widths={'test': 1}, data=[], row_heights=[]):
        from reportlab.lib import colors

        colWidths = [i * cm for i in col_name_and_widths.values()]
        # print(colWidths)
        style = TableStyle([
            ('FONTSIZE', (0, 0), (-1, -1), self.default_fontSize),
            ('FONT', (0, 0), (-1, 0), 'THSarabunNewBd'),  # header
            ('FONT', (0, 0), (-1, -1), 'THSarabunNew'),  # body
            ('GRID', (0, 0), (-1, 0), 1, colors.black),
            ('BOX', (0, 0), (-1, -1), 1, colors.black),
            ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('TOPPADDING', (0, 0), (-1, -1), 0),
        ])
        _data = [
            [i for i in col_name_and_widths.keys()],
        ] + data
        # print(_data)
        rowHeights = len(_data) * \
            [0.7 * cm] if len(row_heights) == 0 else row_heights
        return Table(_data, colWidths, rowHeights, style=style, spaceBefore=0.4*cm)

    def get_buffer(self):
        # print(styles.list())
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=1.5 * cm,
            leftMargin=1.5 * cm,
            topMargin=0.5 * cm,
            bottomMargin=0,)

        elements = []
        elements.append(self.get_title())
        elements.append(self.get_subtitle())
        # elements.append(self.get_date_range())
        elements.append(self.get_content())

        if self.get_signature_footer:
            elements.append(self.get_signature_footer())

        doc.build(elements)
        buffer.seek(0)
        return buffer

    def get_bufferx(self):
        # Create a file-like buffer to receive PDF data.
        buffer = io.BytesIO()

        # Create the PDF object, using the buffer as its "file."
        p = canvas.Canvas(buffer)
        p.setTitle(self.title)

        # Draw things on the PDF. Here's where the PDF generation happens.
        # See the ReportLab documentation for the full list of functionality.
        p.setTitle(self.title)
        p.setFont("THSarabunNewBd", 15)
        p.drawString(250, 800, "ตัวอย่างรายงาน")

        # Close the PDF object cleanly, and we're done.
        p.showPage()
        p.save()

        # FileResponse sets the Content-Disposition header so that browsers
        # present the option to save the file.
        buffer.seek(0)
        return buffer
