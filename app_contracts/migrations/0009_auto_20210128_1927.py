# Generated by Django 3.1.5 on 2021-01-28 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contracts', '0008_auto_20210128_1925'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptbookreceive',
            name='approved_at',
            field=models.DateField(blank=True, null=True, verbose_name='วันที่รับรอง'),
        ),
        migrations.AlterField(
            model_name='receiptbookreceive',
            name='received_at',
            field=models.DateField(blank=True, null=True, verbose_name='วันที่รับ'),
        ),
    ]
