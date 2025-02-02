from django.db import models
from django.db.models import F, Value
from django.db.models.functions import Trim
from django.utils.timezone import localtime, now

class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="الرمز")
    model_number = models.CharField(max_length=50, verbose_name="رقم الموديل", unique=True)
    created_at = models.DateTimeField(verbose_name="تاريخ الإنشاء", default=now)
    ended_at = models.DateTimeField(verbose_name="تاريخ الانتهاء", blank=True, null=True)
    is_archive = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        
    def __str__(self):
        return f"{self.model_number}"

    def is_active(self):
        available_pieces = sum(piece.available_amount for piece in self.pieces.filter(available_amount__gt=0))  # using the Django ORM filter condition
        return available_pieces > 0
    
    def get_usage_percentage(self):
        sizes = self.size_amounts.all()
        pieces = self.pieces.all()
        pieces_count = pieces.count() / sizes.count()

        total_amount = sum(size.amount * pieces_count for size in sizes)
        used_amount = sum(piece.used_amount for piece in pieces)

        percent = (used_amount / total_amount) * 100

        if percent > 80:
            percent_style = "bg-danger"
        elif percent > 60:
            percent_style = "bg-warning"
        elif percent > 40:
            percent_style = "bg-info"
        elif percent > 20:
            percent_style = "bg-success"
        else:
            percent_style = ""

        # Calculate usage percentage for each type
        type_usage = []
        type_names = set(pieces.values_list('type', flat=True))
        for type_name in type_names:
            type_pieces = pieces.filter(type=type_name)
            type_total_amount = total_amount / pieces_count
            type_used_amount = sum(piece.used_amount for piece in type_pieces)
            type_percent = (type_used_amount / type_total_amount) * 100 if type_total_amount > 0 else 0

            if type_percent > 80:
                type_percent_style = "bg-danger"
            elif type_percent > 60:
                type_percent_style = "bg-warning"
            elif type_percent > 40:
                type_percent_style = "bg-info"
            elif type_percent > 20:
                type_percent_style = "bg-success"
            else:
                type_percent_style = ""

            type_usage.append({
                "type": type_name,
                "total_amount": int(type_total_amount),
                "used_amount": int(type_used_amount),
                "percent": int(type_percent),
                "percent_style": type_percent_style,
            })

        return {
            "total_amount": int(total_amount),
            "used_amount": int(used_amount),
            "percent": int(percent),
            "percent_style": percent_style,
            "type_usage": type_usage,
        }
        
class SizeAmount(models.Model):
    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="size_amounts")
    size = models.CharField(max_length=50, verbose_name="المقاس")
    amount = models.PositiveIntegerField(verbose_name="الكمية")
    editable = models.BooleanField(default=True)

    class Meta:
        unique_together = ('model', 'size')
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
    
class ProductionPiece(models.Model):
    piece = models.ForeignKey(Piece, verbose_name="القطعة", on_delete=models.CASCADE, related_name="productions")
    created_at = models.DateTimeField(verbose_name="تاريخ الإنشاء", default=now)
    used_amount = models.IntegerField(verbose_name="الكمية للانتاج", default=0, blank=True)
    factory = models.CharField(max_length=50, verbose_name="المصنع", blank=True)
    comment = models.CharField(max_length=100, verbose_name="الملاحظات", blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if self.pk:
            original = ProductionPiece.objects.get(pk=self.pk)
            diff = self.used_amount - original.used_amount
            self.piece.available_amount -= diff
            self.piece.used_amount += diff
        else:
            self.piece.available_amount -= self.used_amount
            self.piece.used_amount += self.used_amount
        
        self.piece.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.piece.available_amount += self.used_amount
        self.piece.used_amount -= self.used_amount
        self.piece.save()
        super().delete(*args, **kwargs)