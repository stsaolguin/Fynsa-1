# Generated by Django 3.2.6 on 2021-12-29 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFI', '0012_rfi_beta_factor'),
    ]

    operations = [
        migrations.CreateModel(
            name='ejecutivos_externos_bp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_completo', models.TextField(blank=True, null=True)),
                ('codigo', models.CharField(blank=True, max_length=3, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='rfi_beta',
            name='ejecutivo_bp_nombre',
            field=models.TextField(blank=True, null=True),
        ),
    ]