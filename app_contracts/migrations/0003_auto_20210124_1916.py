# Generated by Django 3.1.5 on 2021-01-24 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contracts', '0002_auto_20210124_1848'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contract',
            name='comm_rate',
            field=models.IntegerField(choices=[(4, '4%'), (6, '6%'), (8, '8%')], verbose_name='จ่ายคอมมิสชั่น'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='down_rate',
            field=models.IntegerField(choices=[(100, '100%'), (75, '75%'), (50, '50%'), (0, '0%')], verbose_name='ดาวน์'),
        ),
        migrations.AlterField(
            model_name='contract',
            name='time_count',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20'), (21, '21'), (22, '22'), (23, '23'), (24, '24')], verbose_name='จำนวนงวด'),
        ),
        migrations.DeleteModel(
            name='ActualPay',
        ),
    ]