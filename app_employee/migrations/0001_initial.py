# Generated by Django 3.1.4 on 2021-01-02 06:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_card_no', models.CharField(db_index=True, help_text='x-xxxx-xxxxx-xx-x', max_length=17, unique=True, verbose_name='รหัสประจำตัวประชาชน')),
                ('name', models.CharField(max_length=256, verbose_name='ชื่อ-นามสกุล')),
                ('tel_no', models.CharField(blank=True, max_length=12, verbose_name='เบอร์โทรศัพท์ติดต่อ')),
                ('role', models.CharField(choices=[('1', 'พนักงานขาย'), ('2', 'พนักงานเก็บเงิน'), ('3', 'พนักงานตรวจสอบ'), ('9', 'อื่นๆ')], default='1', max_length=1, verbose_name='')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='วันที่สร้างรายการ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='วันที่แก้ไขรายการ')),
            ],
        ),
        migrations.CreateModel(
            name='MemberShip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_current', models.BooleanField(db_index=True, default=True, verbose_name='เป็นพนักงานประจำสายปัจจุบัน')),
                ('date_joined', models.DateField(blank=True, verbose_name='วันที่เข้าประจำสาย')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='วันที่สร้างรายการ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='วันที่แก้ไขรายการ')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_employee.employee', verbose_name='พนักงาน')),
            ],
        ),
        migrations.CreateModel(
            name='WorkLine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='ชื่อสายงาน')),
                ('is_active', models.BooleanField(db_index=True, default=True, verbose_name='แสดงในระบบ')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='วันที่สร้างรายการ')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='วันที่แก้ไขรายการ')),
                ('members', models.ManyToManyField(through='app_employee.MemberShip', to='app_employee.Employee', verbose_name='พนักงานในสาย')),
            ],
        ),
        migrations.AddField(
            model_name='membership',
            name='workline',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app_employee.workline', verbose_name='สายงาน'),
        ),
    ]
