# Generated by Django 5.1.1 on 2025-02-14 06:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0021_packing_used_carton_alter_packing_used_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='packing',
            name='used_carton',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='الكرتون للتعبئة'),
        ),
    ]
