# Generated by Django 2.2.5 on 2021-01-04 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFL', '0003_auto_20210104_1357'),
    ]

    operations = [
        migrations.AlterField(
            model_name='risk',
            name='monto_outstanding',
            field=models.BigIntegerField(default='0'),
        ),
        migrations.AlterField(
            model_name='risk',
            name='nemo',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='risk',
            name='riesgo',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='risk',
            name='tipo',
            field=models.TextField(),
        ),
    ]
