# Generated by Django 5.1.1 on 2025-02-14 04:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0017_piece_packing_available_amount_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carton',
            name='height',
            field=models.CharField(blank=True, max_length=50, verbose_name='الارتفاع'),
        ),
        migrations.AlterField(
            model_name='carton',
            name='length',
            field=models.CharField(blank=True, max_length=50, verbose_name='الطول'),
        ),
        migrations.AlterField(
            model_name='carton',
            name='width',
            field=models.CharField(blank=True, max_length=50, verbose_name='العرض'),
        ),
    ]
