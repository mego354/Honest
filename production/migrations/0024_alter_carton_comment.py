# Generated by Django 5.1.1 on 2025-02-14 06:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0023_alter_carton_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carton',
            name='comment',
            field=models.CharField(blank=True, max_length=100, verbose_name='المقاسات داخل الكرتونة'),
        ),
    ]
