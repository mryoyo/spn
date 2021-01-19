from django.db.models import F, Count, Sum
from django.contrib import admin
from django.forms import TextInput
from .models import *
from mysite.admin import custom_admin, ModelAdminWithPDF


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

    # def report_view(self, request, *args, **kwargs):
    #     pass

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


@admin.register(ProductStock, site=custom_admin)
class ProductStockAdmin(admin.ModelAdmin):

    search_fields = ('product__code', 'serial_number')
