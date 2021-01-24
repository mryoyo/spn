from django.contrib import admin
from django.utils.html import format_html
from django.utils.formats import date_format
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
from app_employee.models import Employee
from app_products.models import ProductStock
from mysite.admin import custom_admin, multi_line


@admin.register(Contract, site=custom_admin)
class ContractAdmin(admin.ModelAdmin):
    autocomplete_fields = (
        # 'product_stock',
        'customer',
        'customer_co',
        'bondsman',
        'bondsman_co',)
    # readonly_fields = ('contract_no', )
    fieldsets = (
        (_('สินค้า'), {
         'fields': (
             'contract_no',
             'status',
             'product',
             'product_stock',
         )}),
        (_('เช่าซื้อ'), {
         'fields': (
             'sales_price',
             'down_rate',
             'down_price',
             'time_count',
             'per_time_price',
             'comm_rate',
             'date_start',
             'date_effective',
             'day_to_pay',
         )}),
        (_('ผู้ซื้อ / ผู้ค้ำประกัน'), {
            'fields': ('customer', 'customer_co', 'bondsman', 'bondsman_co')}),
        (_('พนักงานขาย / ตรวจสอบ'), {
            'fields': ('seller', 'auditor')}),
    )

    list_display = (
        'contract_no',
        'contract_info',
        'product_info',
        'customer_info',
    )

    search_fields = ('contract_no',)
    list_filter = ('status', 'date_start')

    def contract_info(self, obj):
        raw = multi_line({
            "สถานะ": f'<strong>{obj.get_status_display()}</strong>',
            "ทำสัญญา": f'<strong>{date_format(obj.date_start, use_l10n=True)}</strong>',
            "งวดแรก": f'<strong>{date_format(obj.date_effective, use_l10n=True)}</strong>',
            "ราคาเช่าซื้อ": f'<strong>{obj.sales_price:,.0f} บาท</strong>',
            "ค่างวด": f'<strong>{obj.per_time_price:,.0f} บาท x {obj.time_count} งวด</strong>',
        })
        return format_html(raw)
    contract_info.short_description = "ข้อมูลสัญญา"

    def product_info(self, obj):
        product_stock = obj.product_stock
        product = product_stock.product
        raw = multi_line({
            "รหัสสินค้า": f'<strong>{product.code}</strong>',
            "สินค้า": f'<strong>{product.brand.name} {product.model}</strong>',
            "หมายเลขเครื่อง": f'<strong>{product_stock.serial_number}</strong>',
        })
        return format_html(raw)
    product_info.short_description = "ข้อมูลสินค้า"

    def customer_info(self, obj):
        raw = {
            "ผู้ซื้อ 1": f'<strong>{obj.customer}</strong>',
        }
        if obj.customer_co != None:
            raw["ผู้ซื้อ 2"] = f'<strong>{obj.customer_co if obj.customer_co != None else "ไม่ระบุ"}</strong>'
        if obj.bondsman != None:
            raw["ผู้ค้ำ 1"] = f'<strong>{obj.bondsman if obj.bondsman != None else "ไม่ระบุ"}</strong>'
        if obj.bondsman_co != None:
            raw["ผู้ค้ำ 2"] = f'<strong>{obj.bondsman_co if obj.bondsman_co != None else "ไม่ระบุ"}</strong>'
        return format_html(multi_line(raw))
    customer_info.short_description = "ผู้ซื้อ/ผู้ค้ำ"

    def date_multi_line(self, obj):
        raw = multi_line({
            "วันที่ทำสัญญา": f'<strong>{obj.date_start:%d %B %Y}</strong>',
            "วันที่กำหนดชำระ": f'<strong>{obj.date_effective:%d %B %Y}</strong>',
        })
        return format_html(raw)
    date_multi_line.short_description = "วันที่ทำสัญญา/วันที่กำหนดชำระ"

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        object_id = request.resolver_match.kwargs.get('object_id', None)
        if db_field.name == "seller":
            kwargs["queryset"] = Employee.objects.filter(
                role=Employee.EmployeeRole.SELLER).order_by('code')
        elif db_field.name == "auditor":
            kwargs["queryset"] = Employee.objects.filter(
                role=Employee.EmployeeRole.AUDITOR).order_by('code')
        elif db_field.name == "product_stock":
            kwargs["queryset"] = ProductStock.objects.filter(

            )
        return super().formfield_for_foreignkey(db_field, request, **kwargs)


@admin.register(ReceiptBook, site=custom_admin)
class ReceiptBookAdmin(admin.ModelAdmin):
    readonly_fields = ('item_no',)
    fields = (
        'item_no',
        'book_no',
        'book_group',
        'tr_from',
        'tr_to',
        'remark',
        'requester',
        'requested_at',
        'approver',
        'approved_at',
    )

    list_display = (
        'item_no',
        'book_no',
        'tr_from',
        'tr_to',
        'requester',
        'requested_at',
    )

    list_filter = (
        'requested_at',
        'approved_at'
    )

    search_fields = ('book_no',)

    def item_no(self, obj):
        return f'WDBIL{obj.id:08d}' if obj.id != None else ""
    item_no.short_description = "เลขที่รายการ"
    item_no.admin_order_field = 'id'


@admin.register(MonthlyPayment, site=custom_admin)
class MonthlyPaymentAdmin(admin.ModelAdmin):
    autocomplete_fields = ('contract', )
    search_fields = ('contract__contract_no',)


@admin.register(ActualPay, site=custom_admin)
class ActualPayAdmin(admin.ModelAdmin):
    autocomplete_fields = ('tr_book_no',)

    fieldsets = (
        ('รายการชำระเงิน', {
            'fields': (
                'contract',
                'for_month',
                'amount',
                'collector',
                'tr_book_no',
                'tr_no',
                'date_pay',
                'date_add')
        }),
        ('การรับรอง', {
            'fields': ('approver', 'date_approve')
        })
    )
