# Generated by Django 3.1.4 on 2021-01-02 05:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_customers', '0002_auto_20201224_0112'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='customeraddress',
            options={'verbose_name': 'ข้อมูลที่อยู่', 'verbose_name_plural': 'ข้อมูลที่อยู่'},
        ),
        migrations.AlterField(
            model_name='customer',
            name='title',
            field=models.CharField(choices=[('mr', 'นาย'), ('mrs', 'นาง'), ('miss', 'นางสาว')], max_length=4, verbose_name='title'),
        ),
    ]
