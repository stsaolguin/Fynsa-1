# Generated by Django 2.2.5 on 2020-06-22 17:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BASES', '0003_serie_generacion_mensual'),
    ]

    operations = [
        migrations.AlterField(
            model_name='serie_generacion_mensual',
            name='clientes_80',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serie_generacion_mensual',
            name='clientes_activos',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serie_generacion_mensual',
            name='fecha',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serie_generacion_mensual',
            name='monto_bases',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serie_generacion_mensual',
            name='monto_depositos',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serie_generacion_mensual',
            name='monto_meta',
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='serie_generacion_mensual',
            name='monto_total',
            field=models.BigIntegerField(blank=True, null=True),
        ),
    ]
