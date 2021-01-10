from django.db import models
from django.utils.translation import gettext_lazy as _


class ProductInfo(models.Model):
    code = models.CharField(
        verbose_name="รหัสสินค้า",
        max_length=64,
        unique=True, db_index=True
    )
    type = models.ForeignKey(
        'ProductType',
        verbose_name="ประเภทสินค้า",
        on_delete=models.CASCADE,
    )
    brand = models.ForeignKey(
        'ProductBrand',
        verbose_name="ยี่ห้อสินค้า",
        on_delete=models.CASCADE,
    )
    model = models.CharField(
        verbose_name="รุ่นสินค้า",
        max_length=128,
        blank=True,
        help_text="รายการ / รุ่น",
    )
    note = models.TextField(
        verbose_name="รายละเอียด/หมายเหตุ",
        blank=True,
    )
    is_enabled = models.BooleanField(
        verbose_name="แสดงในระบบ",
        default=True,
        db_index=True,
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
        return f'[{self.code}] {self.brand.name} {self.model}'

    class Meta:
        verbose_name = "รหัสสินค้า"
        verbose_name_plural = "รหัสสินค้า"


class ProductBrand(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ยี่ห้อ"
        verbose_name_plural = "ยี่ห้อ"


class ProductType(models.Model):

    class Category(models.TextChoices):
        NORMAL = '1', _('เครื่องใช้ไฟฟ้า')
        AIRCON_AND_COOLER = '2', _('แอร์/ตู้แช่')

    name = models.CharField(verbose_name="ประเภท", max_length=200)
    category = models.CharField(
        verbose_name="กลุ่ม",
        db_index=True,
        max_length=1,
        choices=Category.choices,
        default=Category.NORMAL)
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "ประเภท"
        verbose_name_plural = verbose_name


class PurchaseOrder(models.Model):
    code = models.CharField(
        verbose_name="เลขที่รับเข้า",
        max_length=32,
        db_index=True,
        unique=True,
        blank=False,
        help_text="ตัวอย่างเช่น ??"
    )
    date = models.DateField(
        verbose_name="วันที่รับเข้า",
        db_index=True,
        blank=False,
        help_text="ตัวอย่างเช่น ??"
    )
    items = models.ManyToManyField(
        'ProductInfo',
        verbose_name="สินค้า",
        through="ProductStock",
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
        return f'{self.code}'

    class Meta:
        verbose_name = "รับเข้าสินค้า"
        verbose_name_plural = "รับเข้าสินค้า"


class ProductStock(models.Model):
    product = models.ForeignKey(
        'ProductInfo',
        verbose_name='รหัสสินค้า',
        on_delete=models.RESTRICT,
        # related_query_name='stock',
    )
    purchase_order = models.ForeignKey(
        'PurchaseOrder',
        verbose_name="เลขที่รับเข้า",
        on_delete=models.RESTRICT,
    )
    serial_number = models.CharField(
        verbose_name="S/N",
        max_length=64,
        unique=True,
        db_index=True,
        help_text="หมายเลขเครื่อง"
    )
    cost_price = models.DecimalField(
        verbose_name="ราคาต้นทุน (บาท)",
        max_digits=8,
        decimal_places=2,
        help_text="ตัวอย่างเช่น 1500.50 หรือ 100 เป็นต้น"
    )

    def __str__(self):
        return "รายการสินค้ารับเข้า"

    class Meta:
        verbose_name = "รายการสินค้ารับเข้า"
        verbose_name_plural = "รายการสินค้ารับเข้า"
