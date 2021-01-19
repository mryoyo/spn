# Generated by Django 3.1.4 on 2021-01-18 18:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_contracts', '0005_receiptbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptbook',
            name='tr_to',
            field=models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49')], default='50', max_length=2, verbose_name='ถึงเลขที่'),
        ),
        migrations.AlterField(
            model_name='receiptbook',
            name='tr_from',
            field=models.CharField(choices=[('01', '01'), ('02', '02'), ('03', '03'), ('04', '04'), ('05', '05'), ('06', '06'), ('07', '07'), ('08', '08'), ('09', '09'), ('10', '10'), ('11', '11'), ('12', '12'), ('13', '13'), ('14', '14'), ('15', '15'), ('16', '16'), ('17', '17'), ('18', '18'), ('19', '19'), ('20', '20'), ('21', '21'), ('22', '22'), ('23', '23'), ('24', '24'), ('25', '25'), ('26', '26'), ('27', '27'), ('28', '28'), ('29', '29'), ('30', '30'), ('31', '31'), ('32', '32'), ('33', '33'), ('34', '34'), ('35', '35'), ('36', '36'), ('37', '37'), ('38', '38'), ('39', '39'), ('40', '40'), ('41', '41'), ('42', '42'), ('43', '43'), ('44', '44'), ('45', '45'), ('46', '46'), ('47', '47'), ('48', '48'), ('49', '49')], default='01', max_length=2, verbose_name='ตั้งแต่เลขที่'),
        ),
    ]