from django.http import FileResponse
from service_report.services import PDFService


class WorkLineReport(PDFService):
    title = "รายงานสายเก็บเงินพนักงาน"


def work_line_report(request):
    pdf = WorkLineReport()
    buffer = pdf.get_buffer()
    return FileResponse(buffer, as_attachment=False, filename='hello.pdf')
