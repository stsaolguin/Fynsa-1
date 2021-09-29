# Generated by Django 2.2.5 on 2021-08-23 17:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ordenes', '0007_carteras_bbg'),
    ]

    operations = [
        migrations.CreateModel(
            name='intenciones_pasadas_salida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_intencion_asignada', models.TextField(blank=True, null=True)),
                ('notas_intencion_asignada', models.TextField(blank=True, null=True)),
                ('intencion_pasada_asignada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.rfi_tsox_borrado')),
                ('orden_asignada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.rfi_tsox')),
            ],
        ),
        migrations.CreateModel(
            name='holders_salida',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_holder_asignada', models.TextField(blank=True, null=True)),
                ('notas_holder_asignada', models.TextField(blank=True, null=True)),
                ('holder_asignada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.carteras_bbg')),
                ('orden_asignada', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ordenes.rfi_tsox')),
            ],
        ),
    ]