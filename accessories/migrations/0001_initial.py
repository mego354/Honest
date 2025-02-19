# Generated by Django 5.1.1 on 2025-02-19 05:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BagStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('bag_length', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (الطول)')),
                ('bag_width', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (العرض)')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='الوزن')),
                ('bags_per_kilo', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس في الكيلو')),
                ('total_bags', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BagSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('bag_length', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (الطول)')),
                ('bag_width', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (العرض)')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='الوزن')),
                ('bags_per_kilo', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس في الكيلو')),
                ('total_bags', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartonStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('length', models.FloatField(blank=True, null=True, verbose_name='المقاس (الطول)')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='المقاس (العرض)')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='المقاس (الارتفاع)')),
                ('total_quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد الإجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CartonSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('length', models.FloatField(blank=True, null=True, verbose_name='المقاس (الطول)')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='المقاس (العرض)')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='المقاس (الارتفاع)')),
                ('total_quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد الإجمالي')),
                ('bundle_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الربط')),
                ('quantity_per_bundle', models.IntegerField(blank=True, null=True, verbose_name='الكمية في الربطة')),
                ('excess', models.IntegerField(blank=True, null=True, verbose_name='الفرط')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlueStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='عرض اللزق')),
                ('cartons_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الكراتين')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GlueSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='عرض اللزق')),
                ('cartons_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الكراتين')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HangerStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('hanger_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الشماعة')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sets_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الدست')),
                ('hangers_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الشماعات')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HangerSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('hanger_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الشماعة')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sets_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الدست')),
                ('hangers_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الشماعات')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HangTagStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HangTagSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HeatSealStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='HeatSealSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KardonStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('meters_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الامتار')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='KardonSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('meters_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الامتار')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingBag',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('bag_length', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (الطول)')),
                ('bag_width', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (العرض)')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='الوزن')),
                ('bags_per_kilo', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس في الكيلو')),
                ('total_bags', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingCarton',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('length', models.FloatField(blank=True, null=True, verbose_name='المقاس (الطول)')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='المقاس (العرض)')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='المقاس (الارتفاع)')),
                ('total_quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد الإجمالي')),
                ('carton_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الكرتون')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingGlue',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='عرض اللزق')),
                ('cartons_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الكراتين')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingHanger',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('hanger_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الشماعة')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sets_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الدست')),
                ('hangers_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الشماعات')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingHangTag',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingHeatSeal',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingKardon',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('meters_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الامتار')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingRubber',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='عرض الاستك')),
                ('total_weight', models.FloatField(blank=True, null=True, verbose_name='الوزن الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingSizer',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sizer_count', models.IntegerField(blank=True, null=True, verbose_name='عدد السيزر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingThread',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('thread_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='كود الخيط')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('spools_count', models.IntegerField(blank=True, null=True, verbose_name='عدد البكر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingTicket',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingTicketPrice',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='PackagingTicketSatan',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('factory', models.CharField(blank=True, max_length=255, null=True, verbose_name='المصنع')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('cotton_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة القطن')),
                ('polyester_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة البوليستر')),
                ('upc_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='UPC Number')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnBag',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('bag_length', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (الطول)')),
                ('bag_width', models.FloatField(blank=True, null=True, verbose_name='مقاس الكيس (العرض)')),
                ('weight', models.FloatField(blank=True, null=True, verbose_name='الوزن')),
                ('bags_per_kilo', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس في الكيلو')),
                ('total_bags', models.IntegerField(blank=True, null=True, verbose_name='عدد الاكياس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnCarton',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('length', models.FloatField(blank=True, null=True, verbose_name='المقاس (الطول)')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='المقاس (العرض)')),
                ('height', models.FloatField(blank=True, null=True, verbose_name='المقاس (الارتفاع)')),
                ('total_quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد الإجمالي')),
                ('carton_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الكرتون')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnHanger',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('hanger_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الشماعة')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sets_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الدست')),
                ('hangers_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الشماعات')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnHangTag',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnHeatSeal',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('quantity', models.IntegerField(blank=True, null=True, verbose_name='العدد')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnKardon',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('meters_count', models.IntegerField(blank=True, null=True, verbose_name='عدد الامتار')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnRubber',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='عرض الاستك')),
                ('total_weight', models.FloatField(blank=True, null=True, verbose_name='الوزن الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnSizer',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sizer_count', models.IntegerField(blank=True, null=True, verbose_name='عدد السيزر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnTicket',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnTicketPrice',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ReturnTicketSatan',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('cotton_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة القطن')),
                ('polyester_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة البوليستر')),
                ('upc_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='UPC Number')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RubberStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='عرض الاستك')),
                ('total_weight', models.FloatField(blank=True, null=True, verbose_name='الوزن الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='RubberSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('width', models.FloatField(blank=True, null=True, verbose_name='عرض الاستك')),
                ('total_weight', models.FloatField(blank=True, null=True, verbose_name='الوزن الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SizerStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sizer_count', models.IntegerField(blank=True, null=True, verbose_name='عدد السيزر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SizerSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('sizer_count', models.IntegerField(blank=True, null=True, verbose_name='عدد السيزر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThreadStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('thread_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='كود الخيط')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('spools_count', models.IntegerField(blank=True, null=True, verbose_name='عدد البكر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ThreadSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('thread_code', models.CharField(blank=True, max_length=255, null=True, verbose_name='كود الخيط')),
                ('color', models.CharField(blank=True, max_length=255, null=True, verbose_name='اللون')),
                ('spools_count', models.IntegerField(blank=True, null=True, verbose_name='عدد البكر')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketPriceStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketPriceSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('total', models.FloatField(blank=True, null=True, verbose_name='الاجمالي')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketSatanStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('cotton_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة القطن')),
                ('polyester_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة البوليستر')),
                ('upc_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='UPC Number')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
                ('code', models.CharField(blank=True, max_length=255, null=True, verbose_name='الرمز')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketSatanSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('model_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='رقم الموديل')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('cotton_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة القطن')),
                ('polyester_percentage', models.FloatField(blank=True, null=True, verbose_name='نسبة البوليستر')),
                ('upc_number', models.CharField(blank=True, max_length=255, null=True, verbose_name='UPC Number')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketStock',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TicketSupplies',
            fields=[
                ('date', models.DateField(blank=True, null=True, verbose_name='التاريخ')),
                ('supplier_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='اسم المورد')),
                ('id', models.IntegerField(primary_key=True, serialize=False, verbose_name='الرمز')),
                ('type', models.CharField(blank=True, max_length=255, null=True, verbose_name='النوع')),
                ('size', models.CharField(blank=True, max_length=255, null=True, verbose_name='المقاس')),
                ('pieces_count', models.IntegerField(blank=True, null=True, verbose_name='عدد القطع')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
