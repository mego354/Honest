# Generated by Django 5.1.1 on 2025-02-15 03:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0031_carton_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='model',
            name='Packing_per_carton',
        ),
        migrations.AddField(
            model_name='sizeamount',
            name='Packing_per_carton',
            field=models.PositiveIntegerField(choices=[(12, '12'), (24, '24'), (36, '36'), (48, '48')], default=12, verbose_name='القطع في الكرتونة'),
        ),
    ]
