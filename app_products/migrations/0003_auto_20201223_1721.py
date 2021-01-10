# Generated by Django 3.1.4 on 2020-12-23 10:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_products', '0002_productinfo_model'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productbrand',
            options={'verbose_name': 'ยี่ห้อ', 'verbose_name_plural': 'ยี่ห้อ'},
        ),
        migrations.AlterModelOptions(
            name='productinfo',
            options={'verbose_name': 'รหัสสินค้า', 'verbose_name_plural': 'รหัสสินค้า'},
        ),
        migrations.AlterModelOptions(
            name='producttype',
            options={'verbose_name': 'ประเภท', 'verbose_name_plural': 'ประเภท'},
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_products.productbrand', verbose_name='ยี่ห้อ'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='code',
            field=models.CharField(db_index=True, max_length=64, unique=True, verbose_name='รหัสสินค้า'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='model',
            field=models.CharField(blank=True, max_length=128, verbose_name='รุ่น'),
        ),
        migrations.AlterField(
            model_name='productinfo',
            name='type',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_products.producttype', verbose_name='ประเภท'),
        ),
    ]
