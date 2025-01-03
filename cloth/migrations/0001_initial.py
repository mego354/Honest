# Generated by Django 5.1.1 on 2024-12-21 03:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CutTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fabric_code', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='كود الخامه')),
                ('fabric_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم الخامه')),
                ('color', models.CharField(blank=True, max_length=100, null=True, verbose_name='اللون')),
                ('roll', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='عدد الاتواب')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='الوزن')),
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('model_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='رقم الموديل')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Fabric',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fabric_code', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='كود الخامه')),
                ('fabric_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم الخامه')),
                ('color', models.CharField(blank=True, max_length=100, null=True, verbose_name='اللون')),
                ('roll', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='عدد الاتواب')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='الوزن')),
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('dyehouse_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم المصبغة')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnTransfer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fabric_code', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='كود الخامه')),
                ('fabric_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم الخامه')),
                ('color', models.CharField(blank=True, max_length=100, null=True, verbose_name='اللون')),
                ('roll', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='عدد الاتواب')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='الوزن')),
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('model_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='رقم الموديل')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Statistics',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fabric_code', models.CharField(blank=True, db_index=True, max_length=100, null=True, verbose_name='كود الخامه')),
                ('fabric_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم الخامه')),
                ('color', models.CharField(blank=True, max_length=100, null=True, verbose_name='اللون')),
                ('roll', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='عدد الاتواب')),
                ('weight', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='الوزن')),
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('dyehouse_name', models.CharField(blank=True, max_length=200, null=True, verbose_name='اسم المصبغة')),
                ('model_number', models.CharField(blank=True, max_length=100, null=True, verbose_name='رقم الموديل')),
                ('movement_type', models.CharField(blank=True, max_length=100, null=True, verbose_name='نوع الحركه')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
