# Generated by Django 5.0.6 on 2024-07-01 19:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0002_alter_formproject_inversion_estimada_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formproject',
            name='analisis_alternativas',
            field=models.FileField(blank=True, null=True, upload_to='documentos/analisis_alternativas/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='analisis_costo_beneficio',
            field=models.FileField(blank=True, null=True, upload_to='documentos/analisis_costo_beneficio/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='estado_con_proyecto',
            field=models.ImageField(blank=True, null=True, upload_to='documentos/estado_con_proyecto/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='estado_inicial',
            field=models.ImageField(blank=True, null=True, upload_to='documentos/estado_inicial/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='estudios_factibilidad',
            field=models.FileField(blank=True, null=True, upload_to='documentos/estudios_factibilidad/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='estudios_prospectivos',
            field=models.FileField(blank=True, null=True, upload_to='documentos/estudios_prospectivos/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='expediente_tecnico',
            field=models.FileField(blank=True, null=True, upload_to='documentos/expediente_tecnico/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='liberacion_derecho_via',
            field=models.FileField(blank=True, null=True, upload_to='documentos/liberacion_derecho_via/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='manifestacion_impacto_ambiental',
            field=models.FileField(blank=True, null=True, upload_to='documentos/manifestacion_impacto_ambiental/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='otros_estudios',
            field=models.FileField(blank=True, null=True, upload_to='documentos/otros_estudios/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='proyecto_ejecutivo',
            field=models.FileField(blank=True, null=True, upload_to='documentos/proyecto_ejecutivo/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='situacion_con_proyecto_proyeccion',
            field=models.FileField(blank=True, null=True, upload_to='documentos/situacion_con_proyecto_proyeccion/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='situacion_sin_proyecto_fotografico',
            field=models.FileField(blank=True, null=True, upload_to='documentos/situacion_sin_proyecto_fotografico/'),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='validacion_normativa',
            field=models.FileField(blank=True, null=True, upload_to='documentos/validacion_normativa/'),
        ),
    ]
