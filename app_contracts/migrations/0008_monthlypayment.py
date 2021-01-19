# Generated by Django 3.1.4 on 2021-01-18 19:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_contracts', '0007_auto_20210118_1837'),
    ]

    operations = [
        migrations.CreateModel(
            name='MonthlyPayment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('for_month', models.CharField(choices=[('1', 'January'), ('2', 'February'), ('3', 'March'), ('4', 'April'), ('5', 'May'), ('6', 'June'), ('7', 'July'), ('8', 'August'), ('9', 'September'), ('10', 'October'), ('11', 'November'), ('12', 'December')], max_length=2, verbose_name='ประจำเดือน')),
                ('payment_type', models.CharField(choices=[('1', 'ปกติ'), ('2', 'เกินกำหนด')], default='1', max_length=1, verbose_name='ประเภท')),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_contracts.contract', verbose_name='')),
            ],
        ),
    ]
