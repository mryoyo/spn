from django.contrib import admin
from django.forms import TextInput
from .models import *
from django.utils.translation import gettext_lazy as _
from service_report.services import PDFService
from mysite.admin import custom_admin, ModelAdminWithPDF, toThaiDate


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

    def report_view(self, request, object_id):
        workline = WorkLine.objects.get(id=object_id)
        members = [[
            toThaiDate(i.date_joined),
            i.workline,
            i.employee.__str__() if i.is_current == False else "-",
            i.employee.__str__() if i.is_current else "-",
            ""]
            for i in workline.membership_set.all()]

        pdf = WorklineReportPDF()
        pdf.table_data = members
        buffer = pdf.get_buffer()
        from django.http import FileResponse
        return FileResponse(buffer, as_attachment=False, filename='hello.pdf')


class WorklineReportPDF(PDFService):
    title = "รายงานสายเก็บเงินพนักงาน"
    table_data = []

    def get_content(self):
        table = self.create_table(
            col_name_and_widths={
                'วันที่': 2,
                'สายเก็บเงิน': 2,
                'พนักงานเดิม': 5,
                'พนักงานประจำสายปัจจุบัน': 5,
                'หมายเหตุ': 4
            },
            data=self.table_data
        )
        table._addCommand(['ALIGN', (0, 0), (1, -1), 'CENTER'])
        return table


@ admin.register(MemberShip, site=custom_admin)
class MemberShipAdmin(admin.ModelAdmin):
    def has_module_permission(self, obj):
        return False

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
