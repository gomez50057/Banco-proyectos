# Generated by Django 5.0.6 on 2024-09-04 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0024_alter_cedularegistro_cobertura'),
    ]

    operations = [
        migrations.AddField(
            model_name='cedularegistro',
            name='Fotografia_Proyecto',
            field=models.FileField(blank=True, null=True, upload_to='anteProInv/fotos/'),
        ),
    ]