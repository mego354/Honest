from django.db import models
from django.core.validators import MinValueValidator

class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="الرمز")
    model_number = models.CharField(max_length=50, verbose_name="رقم الموديل", unique=True)

    def __str__(self):
        return f"{self.model_number}"


class Piece(models.Model):
    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="pieces")
    type = models.CharField(max_length=50, verbose_name="النوع", null=True, blank=True)
    size = models.CharField(max_length=50, verbose_name="المقاس", null=True, blank=True)
    available_amount = models.IntegerField(verbose_name="الكمية المتبقية", null=True, blank=True)
    used_amount = models.IntegerField(verbose_name="الكمية المستخدمة", default=0, null=True, blank=True)

    def __str__(self):
        return f"{self.model.model_number} - {self.type}"


class SizeAmount(models.Model):
    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="size_amounts")
    size = models.CharField(max_length=50, verbose_name="المقاس", null=True, blank=True)
    amount = models.IntegerField(verbose_name="الكمية", null=True, blank=True)

    def __str__(self):
        return f"{self.model.model_number} - {self.type} - Size: {self.size}, Amount: {self.amount}"
