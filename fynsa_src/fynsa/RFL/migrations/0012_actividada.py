# Generated by Django 2.2.5 on 2021-01-25 18:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RFL', '0011_bonos_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='actividad',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('accion', models.TextField()),
                ('usuario', models.TextField()),
                ('fecha', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]