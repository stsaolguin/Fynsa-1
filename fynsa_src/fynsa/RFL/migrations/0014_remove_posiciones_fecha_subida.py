# Generated by Django 2.2.5 on 2021-02-04 22:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('RFL', '0013_auto_20210204_2213'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='posiciones',
            name='fecha_subida',
        ),
    ]
