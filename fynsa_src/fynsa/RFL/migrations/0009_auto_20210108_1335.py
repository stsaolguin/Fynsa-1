# Generated by Django 2.2.5 on 2021-01-08 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFL', '0008_auto_20210106_1402'),
    ]

    operations = [
        migrations.AddField(
            model_name='risk',
            name='rol_rsk',
            field=models.TextField(default='color:green'),
        ),
        migrations.AddField(
            model_name='tr',
            name='rol_tr',
            field=models.TextField(default='color:red'),
        ),
    ]
