from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
from mysite.admin import custom_admin, multi_line


@admin.register(Customer, site=custom_admin)
class CustomerAdmin(admin.ModelAdmin):

    # class AddressInline(admin.StackedInline):
    #     model = CustomerAddress
    # inlines = [AddressInline]

    fieldsets = (
        (_('Personal info'), {
            'fields': (
                'id_card_no',
                'title',
                'first_name',
                'last_name',
                # 'date_of_birth',
                # 'marital_status',
                'date_of_birth_be',
                'occupation',
                'spouse_name',
            )}),
        (_('ที่อยู่อาศัย'), {
            'fields': ('address', 'address_registered')})
    )
    autocomplete_fields = ('address', 'address_registered')
    search_fields = ('first_name', 'last_name')

    list_display = (
        '__str__',
        'id_card_no',
        'get_address',
    )

    def get_address(self, obj):
        raw = multi_line({
            "ที่อยู่ปัจจุบัน": f'{obj.address if obj.address is not None else "-"}',
            "ที่อยู่ตามทะเบียนบ้าน": f'{obj.address_registered if obj.address_registered is not None else "-"}',
        })
        return format_html(raw)
    get_address.short_description = "ข้อมูลที่อยู่"


@admin.register(CustomerAddress, site=custom_admin)
class CustomerAddressAdmin(admin.ModelAdmin):
    def has_module_permission(self, request, **kwargs):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    search_fields = ('first_line', 'second_line',
                     'sub_district', 'district', 'province')
