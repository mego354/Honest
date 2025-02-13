from django.db import models
from django.db.models import Q, Sum, F
from django.utils.timezone import localtime, now

from django.db import models
from django.db.models import Sum
from django.utils.timezone import now


class Model(models.Model):
    DOZENS_CHOICES = [
        (12, "12"),
        (24, "24"),
        (36, "36"),
        (48, "48"),
    ]

    id = models.AutoField(primary_key=True, verbose_name="الرمز")
    model_number = models.CharField(max_length=50, verbose_name="رقم الموديل", unique=True)
    created_at = models.DateTimeField(verbose_name="تاريخ الإنشاء", default=now)
    ended_at = models.DateTimeField(verbose_name="تاريخ الانتهاء", blank=True, null=True)
    shipped_at = models.DateTimeField(verbose_name="تاريخ الشحن", blank=True, null=True)
    is_archive = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)

    Packing_per_carton = models.PositiveIntegerField(
        verbose_name="القطع في الكرتونة", choices=DOZENS_CHOICES, default=12
    )
    available_carton = models.IntegerField(verbose_name="الكراتين المتبقية", blank=True, default=0)
    used_carton = models.IntegerField(verbose_name="الكراتين المستخدمة", blank=True, default=0)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.model_number

    def is_active(self):
        return self.pieces.filter(available_amount__gt=0).exists()

    def comments_count(self):
        return self.pieces.filter(productions__comment__gt="").count()

    def get_usage_percentage(self):
        sizes = self.size_amounts.all()
        pieces = self.pieces.all()
        sizes_count = sizes.count()

        if sizes_count == 0:
            return {
                "production_total_amount": 0,
                "production_used_amount": 0,
                "production_percent": 0,
                "production_percent_style": "",
                "production_type_usage": [],
                "packaging_total_amount": 0,
                "packaging_used_amount": 0,
                "packaging_percent": 0,
                "packaging_percent_style": "",
            }

        pieces_count = pieces.count() / sizes_count

        total_amount = sum(size.amount * pieces_count for size in sizes)
        used_amount = sum(piece.used_amount for piece in pieces)
        percent = (used_amount / total_amount * 100) if total_amount else 0

        percent_style = self.get_percentage_style(percent)

        # Calculate usage percentage for each type
        type_usage = []
        type_names = set(pieces.values_list("type", flat=True))

        for type_name in type_names:
            type_pieces = pieces.filter(type=type_name)
            type_total_amount = total_amount / pieces_count
            type_used_amount = sum(piece.used_amount for piece in type_pieces)
            type_percent = (type_used_amount / type_total_amount * 100) if type_total_amount else 0

            type_usage.append({
                "type": type_name,
                "total_amount": int(type_total_amount),
                "used_amount": int(type_used_amount),
                "percent": int(type_percent),
                "percent_style": self.get_percentage_style(type_percent),
            })

        # Packaging calculations
        total_sizes_pieces = self.size_amounts.aggregate(total=Sum("amount"))["total"] or 0
        packaging_total_carton = total_sizes_pieces / self.Packing_per_carton
        packaging_used_carton = sum(self.packings.values_list("used_carton", flat=True))
        packaging_percent = (packaging_used_carton / packaging_total_carton * 100) if packaging_total_carton else 0

        return {
            "production_total_amount": int(total_amount),
            "production_used_amount": int(used_amount),
            "production_percent": int(percent),
            "production_percent_style": percent_style,
            "production_type_usage": type_usage,
            "packaging_total_amount": int(packaging_total_carton),
            "packaging_used_amount": int(packaging_used_carton),
            "packaging_percent": int(packaging_percent),
            "packaging_percent_style": self.get_percentage_style(packaging_percent),
        }

    @staticmethod
    def get_percentage_style(percent):
        if percent > 80:
            return "bg-danger"
        elif percent > 60:
            return "bg-warning"
        elif percent > 40:
            return "bg-info"
        elif percent > 20:
            return "bg-success"
        return ""

    def update_available_carton(self, *args, **kwargs):
        total_sizes_pieces = self.size_amounts.aggregate(total=Sum("amount"))["total"] or 0
        total_cartons = total_sizes_pieces / self.Packing_per_carton
        used_cartons = sum(self.packings.values_list("used_carton", flat=True))
        self.available_carton = total_cartons - used_cartons

        super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        if self.pk:
            original = Model.objects.filter(pk=self.pk).only("Packing_per_carton").first()
            if original and self.Packing_per_carton != original.Packing_per_carton:
                self.update_available_carton(*args, **kwargs)
            else:
                super().save(*args, **kwargs)
        else:
            super().save(*args, **kwargs)
        
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

        model = self.piece.model
        production_pieces = list(model.pieces.filter(productions__isnull=False))
        if len(production_pieces) == 0:
            model.created_at = localtime(now())
            model.save()
        
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.piece.available_amount += self.used_amount
        self.piece.used_amount -= self.used_amount
        self.piece.save()
        super().delete(*args, **kwargs)
        
        
class Carton(models.Model):
    TYPE_CHOICES = [
        ("شماعة", "شماعة"),
        ("تطبيق", "تطبيق"),
    ]

    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="cartons")
    length = models.CharField(max_length=50, verbose_name="الطول", blank=True)
    width = models.CharField(max_length=50, verbose_name="العرض", blank=True)
    height = models.CharField(max_length=50, verbose_name="الارتفاع", blank=True)
    type = models.CharField(verbose_name="النوع", choices=TYPE_CHOICES, max_length=10, default="تطبيق")
    comment = models.CharField(max_length=100, verbose_name="المقاسات داخل الكرتونة", blank=True)

    def __str__(self):
        return f"{self.length}*{self.width}*{self.height} ({self.type})"

class Packing(models.Model):
    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="packings")
    carton = models.ForeignKey(Carton, verbose_name="الكرتونة", on_delete=models.CASCADE, related_name="packings")
    created_at = models.DateTimeField(verbose_name="تاريخ الإنشاء", default=now)
    used_carton = models.PositiveIntegerField(verbose_name="الكرتون للتعبئة", blank=True, default=0)    

    class Meta:
        ordering = ['-created_at']


    def save(self, *args, **kwargs):
        if self.pk:
            original = Packing.objects.get(pk=self.pk)
            diff = self.used_carton - original.used_carton
            self.model.available_carton -= diff
            self.model.used_carton += diff
        else:
            self.model.available_carton -= self.used_carton
            self.model.used_carton += self.used_carton
        self.model.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.model.available_carton += self.used_carton
        self.model.used_carton -= self.used_carton
        self.model.save()
        super().delete(*args, **kwargs)
