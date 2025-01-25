from django.db import models
from django.utils.timezone import localtime, now

class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="الرمز")
    model_number = models.CharField(max_length=50, verbose_name="رقم الموديل", unique=True)
    created_at = models.DateTimeField(verbose_name="تاريخ الإنشاء", default=now)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.model_number}"


class SizeAmount(models.Model):
    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="size_amounts")
    size = models.CharField(max_length=50, verbose_name="المقاس")
    amount = models.PositiveIntegerField(verbose_name="الكمية")
    editable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('model', 'size')  # Ensure unique size per model
        ordering = ['size']
    def __str__(self):
        return f"{self.model.model_number} - Size: {self.size}, Amount: {self.amount}"


class Piece(models.Model):
    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="pieces")
    type = models.CharField(max_length=50, verbose_name="النوع", blank=True)
    size = models.CharField(max_length=50, verbose_name="المقاس", blank=True)
    available_amount = models.IntegerField(verbose_name="الكمية المتبقية", blank=True, default=0)
    used_amount = models.IntegerField(verbose_name="الكمية المستخدمة", default=0, blank=True)

    class Meta:
        ordering = ['size', 'type']
        
    def __str__(self):
        return f"{self.model.model_number} - Size: {self.size} - Type: {self.type}"