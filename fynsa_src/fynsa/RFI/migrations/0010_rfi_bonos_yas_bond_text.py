# Generated by Django 2.2.5 on 2021-06-04 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFI', '0009_rfi_bonos_yas_bond_porcentaje'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfi_bonos',
            name='yas_bond_text',
            field=models.TextField(blank=True, null=True),
        ),
    ]
