# banco_pro/migrations/0057_alter_formproject_municipio_alter_formproject_region.py
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('banco_pro', '0056_alter_formproject_municipio_alter_formproject_region'),
    ]

    operations = [
        migrations.AlterField(
            model_name='formproject',
            name='municipio',
            field=models.JSONField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='formproject',
            name='region',
            field=models.JSONField(blank=True, null=True),
        ),
    ]
