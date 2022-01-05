# Generated by Django 3.2.6 on 2021-12-29 13:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFI', '0011_rfi_beta_cliente'),
    ]

    operations = [
        migrations.AddField(
            model_name='rfi_beta',
            name='factor',
            field=models.DecimalField(blank=True, decimal_places=20, default=1.0, max_digits=22, null=True),
        ),
    ]