from django.contrib import admin
from django.utils.translation import gettext, gettext_lazy as _
from .models import *
from mysite.admin import custom_admin


@admin.register(Customer, site=custom_admin)
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Personal info'), {
         'fields': ('id_card_no', 'title', 'first_name', 'last_name', 'date_of_birth')}),
        (_('ที่อยู่อาศัย'), {
            'fields': ('address',)})
    )
    autocomplete_fields = ('address', )
    search_fields = ('first_name', 'last_name')


@admin.register(CustomerAddress, site=custom_admin)
class CustomerAddressAdmin(admin.ModelAdmin):
    search_fields = ('first_line', 'second_line',
                     'sub_district', 'district', 'province')
