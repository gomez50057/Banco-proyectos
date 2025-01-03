# Generated by Django 5.0.6 on 2024-08-12 04:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0011_alter_formproject_estatus'),
    ]

    operations = [
        migrations.AddField(
            model_name='formproject',
            name='apellido_materno',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formproject',
            name='apellido_paterno',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formproject',
            name='area_adscripcion',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formproject',
            name='correo_institucional',
            field=models.EmailField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formproject',
            name='correo_personal',
            field=models.EmailField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formproject',
            name='nombre_dependencia',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formproject',
            name='nombre_registrante',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AddField(
            model_name='formproject',
            name='telefono_oficina',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AddField(
            model_name='formproject',
            name='telefono_oficina_ext',
            field=models.CharField(blank=True, default='', max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='formproject',
            name='telefono_particular',
            field=models.CharField(default='', max_length=10),
        ),
    ]
