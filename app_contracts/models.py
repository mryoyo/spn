import calendar
from django.db import models
from django.core.exceptions import ValidationError
from django.utils.html import format_html
from django.utils.translation import gettext, gettext_lazy as _

from smart_selects.db_fields import ChainedForeignKey


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

    product = models.ForeignKey(
        'app_products.ProductInfo',
        verbose_name="สินค้า",
        on_delete=models.RESTRICT
    )

    product_stock = ChainedForeignKey(
        'app_products.ProductStock',
        verbose_name='หมายเลขตัวเครื่อง',
        on_delete=models.RESTRICT,
        chained_field="product",
        chained_model_field="product",
        show_all=False,
        auto_choose=True,
        sort=True
    )

    sales_price = models.DecimalField(
        verbose_name="ราคาเช่าซื้อ (บาท)",
        max_digits=8,
        decimal_places=2,
        help_text="ตัวอย่างเช่น 1500.50 หรือ 100 เป็นต้น"
    )

    comm_rate = models.IntegerField(
        verbose_name="จ่ายคอมมิสชั่น",
        choices=((4, '4%'), (6, '6%'), (8, '8%'))
    )

    down_rate = models.IntegerField(
        verbose_name="ดาวน์",
        choices=((100, '100%'), (75, '75%'), (50, '50%'), (0, '0%'))
    )

    down_price = models.DecimalField(
        verbose_name="เงินดาวน์ (บาท)",
        max_digits=8,
        decimal_places=2,
        help_text="ตัวอย่างเช่น 1500.50 หรือ 100 เป็นต้น"
    )

    time_count = models.IntegerField(
        verbose_name="จำนวนงวด",
        choices=[(x, str(x)) for x in range(1, 25)]
    )

    per_time_price = models.DecimalField(
        verbose_name="ค่างวด (บาท)",
        max_digits=8,
        decimal_places=2,
        help_text="ตัวอย่างเช่น 1500.50 หรือ 100 เป็นต้น"
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

    book_receiving = models.ForeignKey(
        'app_contracts.ReceiptBookReceive',
        verbose_name="รับใบเสร็จ",
        on_delete=models.CASCADE,
        null=True,
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
        return f'{self.book_group}-{self.book_no}'

    @property
    def get_str(self):
        return self.__str__()

    class Meta:
        verbose_name = "เล่มใบเสร็จ"
        verbose_name_plural = "เล่มใบเสร็จ"


class ReceiptBookRequest(models.Model):
    book = models.OneToOneField(
        'ReceiptBook',
        verbose_name="เล่มใบเสร็จ",
        on_delete=models.RESTRICT,
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
        return f'เล่มใบเสร็จ {self.book.book_group}-{self.book.book_no}'

    class Meta:
        verbose_name = "เบิกเล่มใบเสร็จ"
        verbose_name_plural = "เบิกเล่มใบเสร็จ"


class ReceiptBookReceive(models.Model):
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

    book_no_from = models.PositiveIntegerField(
        verbose_name="ตั้งแต่เล่มที่",
    )

    book_no_to = models.PositiveIntegerField(
        verbose_name="ถึงเล่มที่",
    )

    receiver = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="ผู้รับ",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="receipt_receiver"
    )

    received_at = models.DateField(
        verbose_name="วันที่รับ",
        null=True,
        blank=True,
    )

    approver = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="ผู้รับรอง",
        on_delete=models.RESTRICT,
        null=True,
        blank=True,
        related_name="receipt_receive_approver"
    )

    approved_at = models.DateField(
        verbose_name="วันที่รับรอง",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name="วันที่สร้างรายการ",  # วันที่ทำรายการ
        auto_now_add=True,
        editable=False,
    )

    updated_at = models.DateTimeField(
        verbose_name="วันที่แก้ไขรายการล่าสุด",
        auto_now=True,
    )

    def clean(self):
        if (self.book_no_from >= self.book_no_to):
            raise ValidationError(
                '"ตั้งแต่เล่มที่" หรือ "ถึงเล่มที่" ไม่ถูกต้อง"')

    def __str__(self):
        return f'รับใบเสร็จตั้งแต่ {self.book_no_from} ถึง {self.book_no_to}'

    class Meta:
        verbose_name = "รับเล่มใบเสร็จ"
        verbose_name_plural = "รับเล่มใบเสร็จ"


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
        return f'{self.get_for_month_display()}'

    class Meta:
        verbose_name = "งวดชำระประจำเดือน"
        verbose_name_plural = "งวดชำระประจำเดือน"


class ReceiptBookActivity(models.Model):
    number = models.CharField(
        max_length=32,
        unique=True,
        verbose_name="เลขที่รายการ"
    )

    type = models.CharField(
        verbose_name="ประเภทการใช้",
        max_length=2,
        db_index=True,
        choices=(
            ('pa', "รับชำระ[ขายเช่าซื้อ]"),
            ('cp', "ยกเลิกการรับชำระ"),
            ('un', "ยกเลิกการใช้ใบเสร็จ"),
        )
    )

    contract = models.ForeignKey(
        'app_contracts.Contract',
        verbose_name="สัญญาเช่าซื้อ",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )

    customer = ChainedForeignKey(
        'app_customers.Customer',
        verbose_name="ลูกค้า",
        on_delete=models.CASCADE,
        chained_field="contract",
        chained_model_field="customer",
        show_all=False,
        auto_choose=True,
        sort=True,
        null=True,
        blank=True,
    )

    receipt_book = models.ForeignKey(
        'ReceiptBookRequest',
        verbose_name="เล่มที่ใบเสร็จ",
        on_delete=models.RESTRICT,
    )

    receipt_book_requester = ChainedForeignKey(
        'app_employee.Employee',
        chained_field='receipt_book',
        chained_model_field='receipt_requester',
        verbose_name="ผู้เบิกใบเสร็จ",
        on_delete=models.RESTRICT,
        related_name="activity_receipt_request",
        show_all=False,
        auto_choose=True,
    )

    receipt_no = models.CharField(
        verbose_name="เลขที่ใบเสร็จ",
        max_length=2,
        default='01',
        choices=[(f'{x:02d}', f'{x:02d}') for x in range(1, 51)],
    )

    amount = models.DecimalField(
        verbose_name="จำนวนเงินตามใบเสร็จ (บาท)",
        max_digits=8,
        decimal_places=2,
        help_text="ตัวอย่างเช่น 1500.50 หรือ 100 เป็นต้น",
        blank=True,
        null=True,
    )

    receipt_user = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="ผู้ใช้ใบเสร็จ",
        on_delete=models.RESTRICT,
        related_name="activity_receipt_use"
    )

    date_use = models.DateField(
        verbose_name="วันที่ใช้ใบเสร็จ",
    )

    receipt_approver = models.ForeignKey(
        'app_employee.Employee',
        verbose_name="ผู้รับรอง",
        on_delete=models.RESTRICT,
        related_name="activity_receipt_approve",
        null=True,
        blank=True,
    )

    date_approve = models.DateField(
        verbose_name="วันที่รับรอง",
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(
        verbose_name="วันที่บันทึก",
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
