# Generated by Django 5.1.1 on 2025-03-06 02:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0036_factory_productionpiece_worked_factory'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productionpiece',
            name='factory',
        ),
    ]
