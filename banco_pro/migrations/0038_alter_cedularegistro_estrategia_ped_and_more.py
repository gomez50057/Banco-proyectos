# Generated by Django 5.0.6 on 2024-09-19 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0037_alter_cedularegistro_estrategia_ped_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cedularegistro',
            name='estrategia_ped',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cedularegistro',
            name='indicador_ped',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cedularegistro',
            name='objetivo_ped',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cedularegistro',
            name='objetivo_programa',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='cedularegistro',
            name='programa_sectorial',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]