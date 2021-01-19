# Generated by Django 3.1.4 on 2021-01-18 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app_employee', '0007_auto_20210103_1125'),
        ('app_contracts', '0004_auto_20210117_1902'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceiptBook',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('book_no', models.CharField(db_index=True, max_length=10, unique=True, verbose_name='เล่มที่ใบเสร็จ')),
                ('remark', models.CharField(blank=True, max_length=256, null=True, verbose_name='หมายเหตุ')),
                ('tr_from', models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49')], default='50', max_length=2, verbose_name='ถึงเลขที่')),
                ('requested_at', models.DateField(blank=True, null=True, verbose_name='วันที่เบิก')),
                ('approved_at', models.DateField(blank=True, null=True, verbose_name='วันที่ทำรายการ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='วันที่สร้างรายการ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='วันที่แก้ไขรายการล่าสุด')),
                ('approver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='receipt_approver', to='app_employee.employee', verbose_name='ผู้อนุมัติ')),
                ('requester', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, related_name='receipt_requester', to='app_employee.employee', verbose_name='ผู้เบิก')),
            ],
            options={
                'verbose_name': 'เล่มใบเสร็จ',
                'verbose_name_plural': 'เล่มใบเสร็จ',
            },
        ),
    ]