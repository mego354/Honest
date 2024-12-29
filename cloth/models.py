from django.db import models

class Base(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="الرمز")
    fabric_code = models.CharField(max_length=100, verbose_name="كود الخامه", db_index=True, null=True, blank=True)
    fabric_name = models.CharField(max_length=200, verbose_name="اسم الخامه", null=True, blank=True)
    color = models.CharField(max_length=100, verbose_name="اللون", null=True, blank=True)
    roll = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="عدد الاتواب", null=True, blank=True)
    weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="الوزن", null=True, blank=True)
    date = models.CharField(max_length=100,verbose_name="التاريخ", null=True, blank=True)

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Automatically assign an ID if not provided
        if not self.id:
            # Generate the next ID (maximum existing ID + 1)
            max_id = type(self).objects.aggregate(models.Max('id'))['id__max'] or 0
            self.id = max_id + 1
        super().save(*args, **kwargs)
        
        
class Fabric(Base):
    dyehouse_name = models.CharField(max_length=200, verbose_name="اسم المصبغة", null=True, blank=True)

class CutTransfer(Base):
    model_number = models.CharField(max_length=100, verbose_name="رقم الموديل", null=True, blank=True)

class ReturnTransfer(Base):
    model_number = models.CharField(max_length=100, verbose_name="رقم الموديل", null=True, blank=True)

class Statistics(Base):
    dyehouse_name = models.CharField(max_length=200, verbose_name="اسم المصبغة", null=True, blank=True)
    model_number = models.CharField(max_length=100, verbose_name="رقم الموديل", null=True, blank=True)
    movement_type = models.CharField(max_length=100, verbose_name="نوع الحركه", null=True, blank=True)
