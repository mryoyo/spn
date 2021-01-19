# Generated by Django 3.1.4 on 2021-01-18 19:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_contracts', '0008_monthlypayment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='monthlypayment',
            name='contract',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_contracts.contract', verbose_name='สัญญา'),
        ),
        migrations.AlterField(
            model_name='monthlypayment',
            name='for_month',
            field=models.CharField(choices=[('6401', 'มกราคม 2564'), ('6402', 'กุมภาพันธ์ 2564'), ('6403', 'มีนาคม 2564'), ('6404', 'เมษายน 2564'), ('6405', 'พฤษภาคม 2564'), ('6406', 'มิถุนายน 2564'), ('6407', 'กรกฎาคม 2564'), ('6408', 'สิงหาคม 2564'), ('6409', 'กันยายน 2564'), ('6410', 'ตุลาคม 2564'), ('6411', 'พฤศจิกายน 2564'), ('6412', 'ธันวาคม 2564')], max_length=4, verbose_name='ประจำเดือน'),
        ),
    ]
