from django.db import models
from django.db.models import Sum, F, FloatField
from django.db.models.functions import Cast
from django.utils.timezone import localtime, now

from django.db import models
from django.db.models import Sum
from django.utils.timezone import now


class Model(models.Model):
    id = models.AutoField(primary_key=True, verbose_name="الرمز")
    model_number = models.CharField(max_length=50, verbose_name="رقم الموديل", unique=True)
    created_at = models.DateTimeField(verbose_name="تاريخ الإنشاء", default=now)
    ended_at = models.DateTimeField(verbose_name="تاريخ الانتهاء", blank=True, null=True)
    shipped_at = models.DateTimeField(verbose_name="تاريخ الشحن", blank=True, null=True)
    is_archive = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)
    
    available_carton = models.IntegerField(verbose_name="الكراتين المتبقية", blank=True, default=0)
    used_carton = models.IntegerField(verbose_name="الكراتين المستخدمة", blank=True, default=0)
    
    class Meta:
        ordering = ["-created_at"]
    
    def __str__(self):
        return self.model_number

    # Utility Methods
    def is_active(self):
        return self.pieces.filter(available_amount__gt=0).exists()
    
    def comments_count(self):
        return self.pieces.filter(productions__comment__gt="").count()
    
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
    
    # Carton Calculations
    def update_available_carton(self, *args, **kwargs):
        self.available_carton = self.get_total_available_carton()
        self.used_carton = self.get_total_used_cartons()
        super().save(*args, **kwargs)
    
    def get_total_available_carton(self):
        # if self.model_number == '36DG':
        #     print(SizeAmount.objects.filter(model=self).values_list('amount', 'Packing_per_carton'))
        # return int(SizeAmount.objects.filter(model=self, Packing_per_carton__gt=0).aggregate(
        #     total_cartons=Sum(Cast(F('amount'), FloatField()) / Cast(F('Packing_per_carton'), FloatField()))
        # )['total_cartons'] or 0)

        total = 0.0
        for item in SizeAmount.objects.filter(model=self):
            total += float(item.amount) / float(item.Packing_per_carton)
        return int(round(total, 1))


    def get_total_used_cartons(self):
        return Packing.objects.filter(model=self).aggregate(
            used_cartons=Sum('used_carton')
        )['used_cartons'] or 0
            
    def get_total_sizes_pieces(self):
        return self.size_amounts.aggregate(total=Sum('amount'))['total'] or 0
    
    # Usage Percentage Calculation
    def get_model_usage(self):
        sizes = self.size_amounts.all()
        pieces = self.pieces.all()
        sizes_count = sizes.count()

        if sizes_count == 0:
            return self._get_empty_usage_stats()

        pieces_count = pieces.count() / sizes_count
        total_amount = sum(size.amount * pieces_count for size in sizes)
        used_amount = sum(piece.used_amount for piece in pieces)
        percent = (used_amount / total_amount * 100) if total_amount else 0
        percent_style = self.get_percentage_style(percent)

        # Calculate usage percentage for each type
        type_usage = self._calculate_type_usage(pieces, total_amount, pieces_count)

        # Packaging calculations
        packaging_total_carton = self.get_total_available_carton()
        packaging_used_carton = self.get_total_used_cartons()
        packaging_percent = (packaging_used_carton / packaging_total_carton * 100) if packaging_total_carton else 0

        # Calculate usage for each carton
        carton_usage = self._calculate_carton_usage(self.cartons.all())

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
            "packaging_carton_usage": carton_usage,
        }
    
    def _calculate_type_usage(self, pieces, total_amount, pieces_count):
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
        
        return type_usage

    def _calculate_carton_usage(self, carton_models):
        carton_usage = []
        
        for carton_model in carton_models:

            carton_usage.append({
                "name": str(carton_model),
                "comment": carton_model.comment,
                "used_carton": carton_model.get_carton_usage(),
            })
        
        return carton_usage
    
    def _get_empty_usage_stats(self):
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
        
class SizeAmount(models.Model):
    DOZENS_CHOICES = [
        (12, "12"),
        (24, "24"),
        (36, "36"),
        (48, "48"),
    ]
    model = models.ForeignKey(Model, verbose_name="الموديل", on_delete=models.CASCADE, related_name="size_amounts")
    size = models.CharField(max_length=50, verbose_name="المقاس")
    amount = models.PositiveIntegerField(verbose_name="الكمية")
    editable = models.BooleanField(default=True)

    Packing_per_carton = models.PositiveIntegerField(
        verbose_name="القطع في الكرتونة", choices=DOZENS_CHOICES, default=24
    )

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
    
    def get_carton_usage(self):
        return sum(packing.used_carton for packing in Packing.objects.filter(carton=self) )

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
            Model.objects.filter(id=self.model.id).update(
                used_carton=F('used_carton') + diff
            )
        else:
            self.model.used_carton += self.used_carton
        self.model.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.model.used_carton -= self.used_carton
        self.model.save()
        super().delete(*args, **kwargs)

