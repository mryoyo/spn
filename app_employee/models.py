from django.db import models
from django.db.models import signals
from django.utils.translation import gettext_lazy as _


class Employee(models.Model):

    class EmployeeRole(models.TextChoices):
        SELLER = '1', _('พนักงานขาย')
        COLLECTOR = '2', _('พนักงานเก็บเงิน')
        AUDITOR = '3', _('พนักงานตรวจสอบ')
        CLERK = '4', _('พนักงานธุรการ')
        MANGER = '5', _('ผู้จัดการสาขา')
        OTHERS = '9', _('อื่นๆ')

    code = models.CharField(
        verbose_name="รหัสพนักงาน",
        max_length=30,
        db_index=True,
        unique=True,
    )

    id_card_no = models.CharField(
        verbose_name="รหัสประจำตัวประชาชน",
        max_length=17,
        db_index=True,
        unique=True,
        help_text="ตัวอย่าง 6-1234-12345-67-8"
    )
    name = models.CharField(
        verbose_name="ชื่อ-นามสกุล",
        max_length=256,
        blank=False,
        help_text="ตัวอย่างเช่น นาย สมชาย ขายเก่ง"
    )
    tel_no = models.CharField(
        verbose_name="เบอร์โทรติดต่อ",
        max_length=12,
        blank=False
    )
    tel_no_2 = models.CharField(
        verbose_name="เบอร์โทรสำรอง",
        max_length=12,
        blank=True
    )
    role = models.CharField(
        verbose_name="ตำแหน่งงาน",
        max_length=1,
        choices=EmployeeRole.choices,
        default=EmployeeRole.SELLER,
    )
    work_lines = models.ManyToManyField(
        'WorkLine',
        verbose_name='สายเก็บเงิน',
        through='Membership'
    )
    created_at = models.DateTimeField(
        verbose_name="วันที่สร้างรายการ",
        auto_now_add=True,
        editable=False
    )
    updated_at = models.DateTimeField(
        verbose_name="วันที่แก้ไขรายการ",
        auto_now=True
    )

    def __str__(self):
        return f'{self.code}: {self.name}'

    class Meta:
        verbose_name = "พนักงาน"
        verbose_name_plural = "พนักงาน"


class WorkLine(models.Model):
    name = models.CharField(
        verbose_name="ชื่อสายเก็บเงิน",
        max_length=128,
        blank=False
    )
    is_active = models.BooleanField(
        verbose_name="แสดงในระบบ",
        db_index=True,
        default=True,
    )
    members = models.ManyToManyField(
        'Employee',
        verbose_name='พนักงานในสาย',
        through='Membership'
    )
    created_at = models.DateTimeField(
        verbose_name="วันที่สร้างรายการ",
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="วันที่แก้ไขรายการ",
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "สายเก็บเงิน"
        verbose_name_plural = "สายเก็บเงิน"


class MemberShip(models.Model):
    employee = models.ForeignKey(
        'Employee',
        verbose_name="พนักงาน",
        on_delete=models.CASCADE
    )
    workline = models.ForeignKey(
        'WorkLine',
        verbose_name="สายงาน",
        on_delete=models.CASCADE,
    )
    is_current = models.BooleanField(
        verbose_name="เป็นพนักงานประจำสายปัจจุบัน",
        default=True,
        db_index=True,
    )
    date_joined = models.DateField(
        verbose_name="วันที่เข้าประจำสาย",
        blank=True
    )
    created_at = models.DateTimeField(
        verbose_name="วันที่สร้างรายการ",
        auto_now_add=True,
        editable=False,
    )
    updated_at = models.DateTimeField(
        verbose_name="วันที่แก้ไขรายการ",
        auto_now=True,
    )

    def __str__(self):
        return 'พนักงานประจำสาย'

    class Meta:
        verbose_name = "พนักงานประจำสาย"
        verbose_name_plural = "พนักงานประจำสาย"
        unique_together = (('employee', 'workline'),)


class WorkLineReport(models.Model):
    work_line = models.OneToOneField(
        'WorkLine',
        verbose_name="สายเก็บเงิน",
        on_delete=models.CASCADE,
        primary_key=True,
    )

    def __str__(self):
        return f'รายงาน {self.work_line.name}'

    class Meta:
        verbose_name = "รายงานสายเก็บเงินพนักงาน"
        verbose_name_plural = "รายงานสายเก็บเงินพนักงาน"


def auto_create_report(sender, instance, created, **kwargs):
    if created:
        WorkLineReport.objects.create(work_line=instance)


signals.post_save.connect(auto_create_report, sender=WorkLine,
                          weak=False, dispatch_uid='models.auto_create_report')
