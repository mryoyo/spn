from django.db.models import F, Count, Sum
from django.contrib import admin
from django.forms import TextInput
from .models import *
from mysite.admin import custom_admin, ModelAdminWithPDF
from service_report.services import PDFService


@admin.register(ProductInfo, site=custom_admin)
class ProductInfoAdmin(admin.ModelAdmin):

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }
    autocomplete_fields = ('type', 'brand')
    search_fields = ('type__name', 'brand__name', 'model')
    list_display = (
        'code',
        'get_type_name',
        'get_brand_name',
        'model',
        'get_active_contract_count',
        'get_stock_count',
        'is_enabled',
    )
    list_filter = ('created_at', 'type__name')

    fieldsets = (
        ('รายละเอียด', {'fields': ('code', 'type',
                                   'brand', 'model',)}),
        ('เพิ่มเติม', {
            'fields': ('note', 'is_enabled'),
            'classes': ('collapse',)}),
        ('', {'fields': (['created_at', 'updated_at'])})
    )

    readonly_fields = ['created_at', 'updated_at', 'is_enabled']

    def get_queryset(self, request):
        qs = super(ProductInfoAdmin, self).get_queryset(request)
        qs = qs.annotate(stock_count=Count('productstock'))
        return qs

    def get_type_name(self, obj):
        return obj.type.name
    get_type_name.short_description = "ประเภท"
    get_type_name.admin_order_field = 'type__name'

    def get_brand_name(self, obj):
        return obj.brand.name
    get_brand_name.short_description = "ยี่ห้อ"
    get_brand_name.admin_order_field = 'brand__name'

    def get_stock_count(self, obj):
        # print(dir(obj))
        return obj.productstock_set.count()
    get_stock_count.short_description = "สินค้าคงคลัง"
    get_stock_count.admin_order_field = 'stock_count'

    def get_active_contract_count(self, obj):
        return 0
    get_active_contract_count.short_description = "สัญญาปัจจุบัน"
    # get_stock_count.admin_order_field = 'active_contract_count'


@admin.register(ProductType, site=custom_admin)
class ProductTypeAdmin(admin.ModelAdmin):
    # disable from admin index
    def has_module_permission(self, request):
        return False

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }
    search_fields = ['name']


@admin.register(ProductBrand, site=custom_admin)
class ProductBrandAdmin(admin.ModelAdmin):
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }
    search_fields = ['name']

    # disable from admin index
    def has_module_permission(self, request):
        return False


@admin.register(PurchaseOrder, site=custom_admin)
class PurchaseOrderAdmin(ModelAdminWithPDF):

    class StockInline(admin.TabularInline):
        model = PurchaseOrder.items.through
        extra = 1
        max_num = 10

    inlines = [StockInline]

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }

    list_filter = ('date',)

    list_display = (
        'code',
        'date',
        'get_item_count',
        'get_total_cost_price',
    )

    def get_queryset(self, request):
        qs = super(PurchaseOrderAdmin, self).get_queryset(request)
        qs = qs.annotate(
            item_count=Count('productstock'),
            total_cost_price=Sum('productstock__cost_price'),
        )
        return qs

    def get_item_count(self, obj):
        return obj.productstock_set.count()
    get_item_count.short_description = "จำนวนสินค้า"
    get_item_count.admin_order_field = "item_count"

    def get_total_cost_price(self, obj):
        return obj.productstock_set.all().aggregate(result=Sum('cost_price'))['result']
    get_total_cost_price.short_description = "รวมต้นทุน"
    get_total_cost_price.admin_order_field = "total_cost_price"

    def report_view(self, request, object_id):
        order = PurchaseOrder.objects.get(id=object_id)
        items = {}
        for item in order.productstock_set.all():
            product_code = item.product.code
            if (product_code in items):
                items[product_code]['serial_numbers'].append(
                    item.serial_number)
                items[product_code]['total'] += item.cost_price
            else:
                items[product_code] = {
                    'product_code': item.product.code,
                    'product_name': f'{item.product.type} {item.product.brand} {item.product.model}',
                    'serial_numbers': [item.serial_number],
                    'cost_price': item.cost_price,
                    'total': item.cost_price
                }
        pdf = PurchaseOrderReportPDF()
        pdf.data_po_no = order.code
        pdf.data_po_items = list(items.values())
        buffer = pdf.get_buffer()
        from django.http import FileResponse
        return FileResponse(buffer, as_attachment=False, filename='hello.pdf')


class PurchaseOrderReportPDF(PDFService):
    title = "รายงานรับเข้าสินค้า"
    signature_role_left = "ผู้รับสินค้า"

    def get_content(self):
        data = [
            [
                self.data_po_no if i == 0 else '',
                item['product_code'],
                item['product_name'],
                '\n'.join(item['serial_numbers']),
                len(item['serial_numbers']),
                f"{item['cost_price']:,.2F}",
                f"{item['total']:,.2F}"
            ] for i, item in enumerate(self.data_po_items)
        ]
        from reportlab.lib.units import cm
        row_heights = [0.7 * cm] + \
            [((len(i['serial_numbers']) * 0.40) +
              0.30) * cm for i in self.data_po_items]
        print(row_heights)
        table = self.create_table(
            col_name_and_widths={
                'เลขที่รับเข้า': 2,
                'รหัสสินค้า': 1.8,
                'รายการสินค้า/รุ่นสินค้า': 5.5,
                'หมายเลขเครื่อง': 3.5,
                'จำนวน': 1.2,
                'ต้นทุน/หน่วย': 2,
                'ต้นทุน (บาท)': 2
            },
            data=data,
            row_heights=row_heights
        )
        from reportlab.lib import colors
        table._addCommand(('GRID', (0, 0), (-1, -1), 0.25, colors.grey))
        table._addCommand(('ALIGN', (-3, 1), (-3, -1), 'CENTER'))
        table._addCommand(('ALIGN', (-2, 1), (-1, -1), 'RIGHT'))
        table._addCommand(('SPAN', (0, 1), (0, -1)))
        return table


@admin.register(ProductStock, site=custom_admin)
class ProductStockAdmin(admin.ModelAdmin):
    def has_module_permission(self, obj):
        return False

    search_fields = ('product__code', 'serial_number')
    list_display = ('product', 'serial_number',
                    'cost_price', 'related_contract')

    def related_contract(self, obj):
        contracts = obj.contract_set.all()
        return f'{contracts.first()}' if contracts.exists() else ''
    related_contract.short_description = "สัญญาเช่าซื้อ"
