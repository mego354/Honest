# Generated by Django 5.1.1 on 2025-02-01 09:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0012_productionpiece_factory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='productionpiece',
            options={'ordering': ['-created_at']},
        ),
        migrations.AddField(
            model_name='model',
            name='is_archive',
            field=models.BooleanField(default=False),
        ),
    ]
