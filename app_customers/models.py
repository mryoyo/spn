from django.db import models
from django.utils.translation import gettext, gettext_lazy as _


class Customer(models.Model):
    class Meta:
        verbose_name = "ข้อมูลลูกค้า"
        verbose_name_plural = "ข้อมูลลูกค้า"

    id_card_no = models.CharField(
        max_length=17,
        db_index=True,
        unique=True,
        help_text="x-xxxx-xxxxx-xx-x"
    )
    title = models.CharField(
        _('title'),
        max_length=4,
        choices=(('mr', 'นาย'), ('mrs', 'นาง'), ('miss', 'นางสาว'))
    )

    first_name = models.CharField(
        _('first name'),
        max_length=32,
        blank=False
    )

    last_name = models.CharField(
        _('last name'),
        max_length=32,
        blank=False
    )

    date_of_birth = models.DateField()
    marital_status = models.CharField(
        _("marital status"),
        max_length=1,
        choices=(
            ('S', 'โสด'), ('M', 'สมรส'), ('D', 'หย่าร้าง'), ('W', 'หม้าย')
        )
    )

    address = models.ForeignKey('CustomerAddress', on_delete=models.RESTRICT)

    def get_full_name(self):
        return f'{self.get_title_display()}{self.first_name} {self.last_name}'

    def __str__(self):
        return self.get_full_name()


class CustomerAddress(models.Model):
    class Meta:
        verbose_name = "ข้อมูลที่อยู่"
        verbose_name_plural = verbose_name

    first_line = models.CharField(_('บ้านเลขที่'), max_length=256)
    second_line = models.CharField(
        _('หมู่/ซอย/ถนน'), max_length=256, blank=False)
    sub_district = models.CharField(_('ตำบล'), max_length=64, blank=False)
    district = models.CharField(_('อำเภอ'), max_length=64, blank=False)
    province = models.CharField(_('จังหวัด'), max_length=64, blank=False)

    def __str__(self):
        return f'{self.first_line}\n{self.second_line}\n{self.sub_district} {self.district} {self.province}'