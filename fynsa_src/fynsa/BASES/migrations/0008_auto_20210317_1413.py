# Generated by Django 2.2.5 on 2021-03-17 14:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BASES', '0007_auto_20201214_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bases',
            name='fynsa',
            field=models.TextField(blank=True, choices=[('NO', 'NO'), ('SI', 'SI')], null=True),
        ),
        migrations.AlterField(
            model_name='bases',
            name='otc_tr',
            field=models.TextField(blank=True, choices=[('OTC', 'OTC'), ('TR', 'TR')], null=True),
        ),
        migrations.AlterField(
            model_name='bases',
            name='tipo_de_pago',
            field=models.TextField(blank=True, choices=[('PM', 'PM'), ('PH', 'PH')], null=True),
        ),
    ]
