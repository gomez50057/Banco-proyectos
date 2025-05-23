# Generated by Django 5.0.6 on 2025-02-07 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0002_remove_formproject_isblocked_situacion_actual_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='formproject',
            name='isBlocked_situacion_actual',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='formproject',
            name='observacion_situacion_actual',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='formproject',
            name='situacion_actual',
            field=models.ImageField(blank=True, null=True, upload_to='documentos/situacion_actual/'),
        ),
    ]
