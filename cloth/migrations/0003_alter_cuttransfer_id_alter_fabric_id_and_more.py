# Generated by Django 5.1.1 on 2024-12-29 18:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cloth', '0002_alter_cuttransfer_id_alter_fabric_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cuttransfer',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز'),
        ),
        migrations.AlterField(
            model_name='fabric',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز'),
        ),
        migrations.AlterField(
            model_name='returntransfer',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز'),
        ),
        migrations.AlterField(
            model_name='statistics',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز'),
        ),
    ]
