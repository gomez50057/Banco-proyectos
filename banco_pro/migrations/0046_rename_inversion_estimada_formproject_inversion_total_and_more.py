# Generated by Django 5.0.6 on 2024-11-26 22:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0045_rename_isblocked_estado_inicial_formproject_isblocked_situacion_actual_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='formproject',
            old_name='inversion_estimada',
            new_name='inversion_total',
        ),
        migrations.RenameField(
            model_name='formproject',
            old_name='isBlocked_inversion_estimada',
            new_name='isBlocked_inversion_total',
        ),
        migrations.RenameField(
            model_name='formproject',
            old_name='observacion_inversion_estimada',
            new_name='observacion_inversion_total',
        ),
    ]
