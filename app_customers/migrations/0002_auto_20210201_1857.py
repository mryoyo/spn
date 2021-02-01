# Generated by Django 3.1.5 on 2021-02-01 18:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_customers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='address_registered',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.RESTRICT, related_name='customer_registered', to='app_customers.customeraddress', verbose_name='ที่อยู่ตามทะเบียนบ้าน'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='address',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='app_customers.customeraddress', verbose_name='ที่อยู่ปัจจุบัน'),
        ),
    ]