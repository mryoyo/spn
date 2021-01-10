from django.contrib import admin
from django.forms import TextInput
from .models import *
from django.utils.translation import gettext_lazy as _

from mysite.admin import custom_admin

# from django.contrib.admin import AdminSite
# from django.contrib import admin
# from django.http import HttpResponse

# from django.urls import path


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

    def work_lines_name(self, obj):
        return ','.join([str(i.name) for i in obj.work_lines.order_by('name')])
    work_lines_name.short_description = "สายงาน"


@admin.register(WorkLine, site=custom_admin)
class WorkLineAdmin(admin.ModelAdmin):
    class MemberInline(admin.TabularInline):
        model = WorkLine.members.through
        extra = 0
        can_delete = False
        readonly_fields = ('employee', 'is_current', 'date_joined')

        def has_add_permission(self, request, obj):
            return False

    formfield_overrides = {
        models.CharField: {'widget': TextInput(attrs={'autocomplete': 'off', 'class': 'vTextField'})},
    }
    fieldsets = (
        (_(''), {
         'fields': ('name', 'is_active',)}),
        # (_('ข้อมูลพนักงาน'), {
        #     'fields': ('members',)}),
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


@admin.register(WorkLineReport, site=custom_admin)
class WorkLineReportAdmin(admin.ModelAdmin):

    change_form_template = "admin/report_work_line.html"

    def has_add_permission(self, request):
        return False

    def has_view_permission(self, request, obj=None):
        return True

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return True

    list_display = ['work_line_name']

    def work_line_name(self, obj):
        return f'{obj.work_line.name}'
    work_line_name.short_description = "สายเก็บเงิน"
