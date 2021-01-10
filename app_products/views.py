from django.http import FileResponse
from service_report.services import PDFService
from .models import PurchaseOrder


class PurchaseOrderReport(PDFService):
    title = "รายงานการรับเข้าสินค้า"


def purchase_order_report(request):
    po_id = request.GET['po_id']
    obj = PurchaseOrder.objects.get(id=po_id)
    pdf = PurchaseOrderReport()
    pdf.title += f' {obj.date}'
    buffer = pdf.get_buffer()
    return FileResponse(buffer, as_attachment=False, filename='hello.pdf')
