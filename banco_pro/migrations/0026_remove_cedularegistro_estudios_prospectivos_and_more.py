# Generated by Django 5.0.6 on 2024-09-04 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0025_cedularegistro_fotografia_proyecto'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cedularegistro',
            name='estudios_prospectivos',
        ),
        migrations.RemoveField(
            model_name='cedularegistro',
            name='prioridad',
        ),
        migrations.RemoveField(
            model_name='cedularegistro',
            name='situacion_con_proyecto_proyeccion',
        ),
        migrations.RemoveField(
            model_name='cedularegistro',
            name='situacion_sin_proyecto_fotografico',
        ),
        migrations.AddField(
            model_name='cedularegistro',
            name='expediente_Tecnico_Docu',
            field=models.FileField(blank=True, null=True, upload_to='anteProInv/expediente/tecnico/'),
        ),
    ]