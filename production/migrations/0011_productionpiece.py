# Generated by Django 5.1.1 on 2025-01-26 12:43

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('production', '0010_alter_model_options_sizeamount_editable'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductionPiece',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, verbose_name='تاريخ الإنشاء')),
                ('used_amount', models.IntegerField(blank=True, default=0, verbose_name='الكمية للانتاج')),
                ('piece', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='productions', to='production.piece', verbose_name='القطعة')),
            ],
        ),
    ]
