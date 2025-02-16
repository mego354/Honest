# Generated by Django 5.1.1 on 2025-02-16 01:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0034_alter_packing_size_amount'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='packing',
            name='size_amount',
        ),
        migrations.AlterField(
            model_name='sizeamount',
            name='Packing_per_carton',
            field=models.PositiveIntegerField(choices=[(12, '12'), (24, '24'), (36, '36'), (48, '48')], default=24, verbose_name='القطع في الكرتونة'),
        ),
    ]
