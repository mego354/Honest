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

    def is_active(self):
        available_pieces = sum(piece.available_amount for piece in self.pieces.filter(available_amount__gt=0))  # using the Django ORM filter condition
        return available_pieces > 0
    
    def get_usage_percentage(self):
        sizes = self.size_amounts.all()
        pieces = self.pieces.all()
        pieces_count = pieces.count() / sizes.count()

        total_amount = sum( size.amount * pieces_count for size in sizes )
        available_amount = sum(piece.available_amount for piece in pieces.filter(available_amount__gte=0))
        used_amount = total_amount - available_amount
        # used_amount = total_amount * 0.81
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
        print(int(total_amount))
        return {
            "total_amount": int(total_amount),
            "used_amount": int(used_amount),
            "percent": int(percent),
            "percent_style": percent_style,
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