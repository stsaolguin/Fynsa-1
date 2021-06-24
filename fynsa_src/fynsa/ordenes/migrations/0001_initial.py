# Generated by Django 2.2.5 on 2021-06-08 12:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='rfi_tsox',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField()),
                ('trader', models.TextField(blank=True, null=True)),
                ('orden_tipo', models.TextField(blank=True, null=True)),
                ('isin', models.TextField(blank=True, null=True)),
                ('papel', models.TextField(blank=True, null=True)),
                ('cliente', models.TextField(blank=True, null=True)),
                ('rating', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('pais', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('duracion', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('nominales', models.BigIntegerField(blank=True, null=True)),
                ('sector', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('precio', models.DecimalField(blank=True, decimal_places=3, max_digits=6, null=True)),
                ('payment_rank', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), blank=True, null=True, size=None)),
                ('notas', models.TextField(blank=True, null=True)),
                ('status', models.TextField(blank=True, null=True)),
            ],
        ),
    ]
