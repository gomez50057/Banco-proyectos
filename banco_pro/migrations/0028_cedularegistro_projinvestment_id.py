# Generated by Django 5.0.6 on 2024-09-05 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0027_rename_expediente_tecnico_docu_cedularegistro_expediente_tecnico_docu_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cedularegistro',
            name='projInvestment_id',
            field=models.CharField(blank=True, max_length=20, null=True, unique=True),
        ),
    ]
