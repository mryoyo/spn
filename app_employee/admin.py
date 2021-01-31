from django.contrib import admin
from django.forms import TextInput
from .models import *
from django.utils.translation import gettext_lazy as _

from mysite.admin import custom_admin, ModelAdminWithPDF


@admin.register(Employee, site=custom_admin)
class EmployeeAdmin(admin.ModelAdmin):
    class WorkLineInline(admin.TabularInline):
        model = Employee.work_lines.through
        extra = 0
    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }
    # autocomplete_fields = ('type', 'brand')
    # search_fields = ('type__name', 'brand__name', 'model')
    list_display = ('code', 'name',
                    'role', 'tel_no',
                    # 'created_at', 'updated_at',
                    'work_lines_name'
                    )
    ordering = ['code', ]
    list_filter = ('work_lines__name', 'role', 'updated_at')
    fieldsets = (
        (_('ข้อมูลส่วนตัว'), {
         'fields': ('id_card_no', 'name', 'tel_no', 'tel_no_2',)}),
        (_('ข้อมูลพนักงาน'), {
            'fields': ('code', 'role',)}),
    )
    inlines = [WorkLineInline]
    search_fields = ('code', 'name',)

    def work_lines_name(self, obj):
        return ','.join([str(i.name) for i in obj.work_lines.order_by('name')])
    work_lines_name.short_description = "สายงาน"


@admin.register(WorkLine, site=custom_admin)
class WorkLineAdmin(ModelAdminWithPDF):
    class MemberInline(admin.TabularInline):
        model = WorkLine.members.through
        extra = 0
        can_delete = False
        # readonly_fields = ('employee', 'is_current', 'date_joined')

        def has_add_permission(self, request, obj):
            return True

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }
    fieldsets = (
        (_(''), {
         'fields': ('name', 'is_active',)}),
    )
    inlines = [MemberInline]
    list_display = ('name',
                    'get_current_member_count', 'get_old_member_count',
                    'created_at', 'updated_at',
                    )

    ordering = ['name', 'created_at']
    list_filter = ['created_at', ]

    def get_current_member_count(self, obj):
        return obj.members.filter(membership__is_current=True).count()
    get_current_member_count.short_description = "พนักงานปัจจุบัน"

    def get_old_member_count(self, obj):
        return obj.members.filter(membership__is_current=False).count()
    get_old_member_count.short_description = "พนักงานเดิม"


@admin.register(MemberShip, site=custom_admin)
class MemberShipAdmin(admin.ModelAdmin):
    fields = (
        'workline',
        'employee',
        'date_joined'
    )

    list_display = (
        'workline',
        'employee'
    )

    list_display_links = (
        'workline',
        'employee'
    )

    list_filter = (
        'workline__name',
    )
