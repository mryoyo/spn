import calendar
from django.db import models
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _


class Contract(models.Model):
    contract_no = models.CharField(
        verbose_name="เลขที่สัญญา",
        max_length=30,
        unique=True, db_index=True,
        # editable=False
    )

    status = models.CharField(
        verbose_name="สถานะ",
        choices=(('1', format_html('<span style="color:green; weight:bold;">เปิดบัญชีการผ่อน</span>')),
                 ('0', 'ปิดบัญชีการผ่อน')),
        default='1',
        max_length=1,
        db_index=True,
    )

    product_stock = models.ForeignKey(
        'app_products.ProductStock',
        verbose_name='สินค้ารับเข้า',
        on_delete=models.RESTRICT
    )

    customer = models.ForeignKey(
        'app_customers.Customer',
        verbose_name="ผู้ซื้อ",
        on_delete=models.RESTRICT,
        related_name="customer"
    )

    customer_co = models.ForeignKey(
        'app_customers.Customer',
        verbose_name="ผู้ซื้อ 2",
        on_delete=models.RESTRICT,
        related_name="customer_co",
        null=True,
        blank=True,
    )

    bondsman = models.ForeignKey(
        'app_customers.Customer',
        verbose_name="ผู้ค้ำ 1",
        on_delete=models.RESTRICT,
        related_name="bondsman",
        null=True,
        blank=True,
    )

    bondsman_co = models.ForeignKey(
        'app_customers.Customer',
        verbose_name="ผู้ค้ำ 2",
        on_delete=models.RESTRICT,
        related_name="bondsman_co",
        null=True,
        blank=True,
    )

    seller = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="พนักงานขาย",
        on_delete=models.RESTRICT,
        related_name="seller",
    )

    auditor = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="พนักงานตรวจสอบ",
        on_delete=models.RESTRICT,
        related_name="auditor"
    )

    day_to_pay = models.IntegerField(
        verbose_name="นัดเก็บทุกวันที่",
        default=10,
        choices=[(i, i) for i in range(1, 31)]
    )

    date_start = models.DateField(
        verbose_name="วันที่ทำสัญญา",
    )

    date_end = models.DateField(
        verbose_name="วันที่ครบกำหนดชำระ",
        null=True,
        blank=True,
    )

    date_effective = models.DateField(
        verbose_name="วันนัดชำระงวดแรก",
    )

    date_close = models.DateField(
        verbose_name="วันที่ปิดสัญญา",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name="วันที่สร้างรายการ",
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        verbose_name="วันที่แก้ไขรายการล่าสุด",
        auto_now=True,
    )

    def __str__(self):
        return f'สัญญาเลขที่ {self.contract_no}'

    class Meta:
        verbose_name = "สัญญาเช่าซื้อ"
        verbose_name_plural = "สัญญาเช่าซื้อ"


class ReceiptBook(models.Model):
    book_no = models.CharField(
        verbose_name="เล่มที่ใบเสร็จ",
        max_length=10,
        unique=True,
        db_index=True,
    )

    book_group = models.CharField(
        verbose_name="หมวด",
        max_length=16,
        null=True,
        blank=True,
    )

    remark = models.CharField(
        verbose_name="หมายเหตุ",
        max_length=256,
        null=True,
        blank=True,
    )

    tr_from = models.CharField(
        verbose_name="ตั้งแต่เลขที่",
        max_length=2,
        default='01',
        choices=[(f'{x:02d}', f'{x:02d}') for x in range(1, 51)],
    )

    tr_to = models.CharField(
        verbose_name="ถึงเลขที่",
        max_length=2,
        default='50',
        choices=[(f'{x:02d}', f'{x:02d}') for x in range(1, 51)],
    )

    requester = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="ผู้เบิก",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="receipt_requester"
    )

    approver = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="ผู้อนุมัติ",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="receipt_approver"
    )

    requested_at = models.DateField(
        verbose_name="วันที่เบิก",
        null=True,
        blank=True,
    )

    approved_at = models.DateField(
        verbose_name="วันที่ทำรายการ",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name="วันที่สร้างรายการ",
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        verbose_name="วันที่แก้ไขรายการล่าสุด",
        auto_now=True,
    )

    def __str__(self):
        return f'เล่มใบเสร็จที่ {self.book_no}'

    class Meta:
        verbose_name = "เล่มใบเสร็จ"
        verbose_name_plural = "เล่มใบเสร็จ"


class MonthlyPayment(models.Model):
    contract = models.ForeignKey(
        'app_contracts.Contract',
        verbose_name="สัญญา",
        on_delete=models.CASCADE,
    )

    for_month = models.CharField(
        verbose_name="ประจำเดือน",
        max_length=4,
        choices=[(f'64{x:02d}', _(calendar.month_name[x]) + " 2564")
                 for x in range(1, 13)]
    )

    payment_type = models.CharField(
        verbose_name="ประเภท",
        max_length=1,
        choices=(('1', 'ปกติ'), ('2', 'เกินกำหนด')),
        default='1'
    )

    def __str__(self):
        return f'งวดชำระเดือน {self.get_for_month_display()} {self.contract}'

    class Meta:
        verbose_name = "งวดชำระประจำเดือน"
        verbose_name_plural = "งวดชำระประจำเดือน"


class ActualPay(models.Model):
    for_month = models.ForeignKey(
        'app_contracts.MonthlyPayment',
        verbose_name="ประจำเดือน",
        on_delete=models.CASCADE
    )

    amount = models.DecimalField(
        verbose_name="จำนวนเงิน (บาท)",
        max_digits=8,
        decimal_places=2,
        help_text="ตัวอย่างเช่น 1500.50 หรือ 100 เป็นต้น"
    )

    collector = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="พนักงานเก็บเงิน",
        on_delete=models.RESTRICT,
        related_name="pay_collector",
    )

    approver = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="ผู้รับรอง",
        on_delete=models.RESTRICT,
        related_name="pay_approver",
        null=True,
        blank=True,
    )

    date_pay = models.DateField(
        verbose_name="วันที่ใช้ใบเสร็จ",
    )

    date_add = models.DateField(
        verbose_name="วันที่บันทึก",
    )

    date_approve = models.DateField(
        verbose_name="วันที่รับรอง",
        null=True,
        blank=True,
    )

    tr_book_no = models.ForeignKey(
        'app_contracts.ReceiptBook',
        verbose_name="ใบเสร็จ เล่มที่",
        on_delete=models.CASCADE,
        default=1
    )

    tr_no = models.CharField(
        verbose_name="ใบเสร็จ เลขที่",
        max_length=2,
        default='01'
    )

    created_at = models.DateTimeField(
        verbose_name="วันที่สร้างรายการ",
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        verbose_name="วันที่แก้ไขรายการล่าสุด",
        auto_now=True,
    )

    def __str__(self):
        return f'รับชำระเงิน {self.for_month}'

    class Meta:
        verbose_name = "รับชำระเงิน"
        verbose_name_plural = "รับชำระเงิน"
