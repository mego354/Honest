from django.db import models

class BaseModel(models.Model):
    date = models.DateField("التاريخ", null=True, blank=True)

    class Meta:
        abstract = True

class SupplierBaseModel(BaseModel):
    supplier_name = models.CharField("اسم المورد", max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

class PackagingBaseModel(BaseModel):
    factory = models.CharField("المصنع", max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

class IDBaseModel(models.Model):
    id = models.IntegerField(primary_key=True, verbose_name="الرمز")

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        # Automatically assign an ID if not provided
        if not self.id:
            # Generate the next ID (maximum existing ID + 1)
            max_id = type(self).objects.aggregate(models.Max('id'))['id__max'] or 0
            self.id = max_id + 1
        super().save(*args, **kwargs)

class CartonBaseModel(IDBaseModel):
    model_number = models.CharField("رقم الموديل", max_length=255, null=True, blank=True)
    length = models.CharField("المقاس (الطول)", max_length=255, null=True, blank=True)
    width = models.CharField("المقاس (العرض)", max_length=255, null=True, blank=True)
    height = models.CharField("المقاس (الارتفاع)", max_length=255, null=True, blank=True)
    total_quantity = models.IntegerField("العدد الإجمالي", null=True, blank=True)

    class Meta:
        abstract = True

class HangerBaseModel(IDBaseModel):
    hanger_number = models.CharField("رقم الشماعة", max_length=255, null=True, blank=True)
    color = models.CharField("اللون", max_length=255, null=True, blank=True)
    sets_count = models.IntegerField("عدد الدست", null=True, blank=True)
    hangers_count = models.IntegerField("عدد الشماعات", null=True, blank=True)

    class Meta:
        abstract = True

class SizerBaseModel(IDBaseModel):
    size = models.CharField("المقاس", max_length=255, null=True, blank=True)
    color = models.CharField("اللون", max_length=255, null=True, blank=True)
    sizer_count = models.IntegerField("عدد السيزر", null=True, blank=True)

    class Meta:
        abstract = True

class BagBaseModel(IDBaseModel):
    bag_length = models.CharField("مقاس الكيس (الطول)", max_length=255, null=True, blank=True)
    bag_width = models.CharField("مقاس الكيس (العرض)", max_length=255, null=True, blank=True)
    weight = models.FloatField("الوزن", null=True, blank=True)
    bags_per_kilo = models.IntegerField("عدد الاكياس في الكيلو", null=True, blank=True)
    bags_quantity = models.IntegerField("عدد الاكياس", null=True, blank=True)

    class Meta:
        abstract = True

class HangTagBaseModel(IDBaseModel):
    type = models.CharField("النوع", max_length=255, null=True, blank=True)
    quantity = models.IntegerField("العدد", null=True, blank=True)

    class Meta:
        abstract = True

class HeatSealBaseModel(IDBaseModel):
    type = models.CharField("النوع", max_length=255, null=True, blank=True)
    quantity = models.IntegerField("العدد", null=True, blank=True)
    size = models.CharField("المقاس", max_length=255, null=True, blank=True)

    class Meta:
        abstract = True

class TicketSatanBaseModel(IDBaseModel):
    model_number = models.CharField("رقم الموديل", max_length=255, null=True, blank=True)
    size = models.CharField("المقاس", max_length=255, null=True, blank=True)
    cotton_percentage = models.CharField("نسبة القطن", max_length=255, null=True, blank=True)
    polyester_percentage = models.CharField("نسبة البوليستر", max_length=255, null=True, blank=True)
    upc_number = models.CharField("UPC Number", max_length=255, null=True, blank=True)
    pieces_count = models.IntegerField("عدد القطع", null=True, blank=True)

    class Meta:
        abstract = True

class TicketBaseModel(IDBaseModel):
    type = models.CharField("النوع", max_length=255, null=True, blank=True)
    size = models.CharField("المقاس", max_length=255, null=True, blank=True)
    pieces_count = models.IntegerField("عدد القطع", null=True, blank=True)

    class Meta:
        abstract = True

class TicketPriceBaseModel(IDBaseModel):
    model_number = models.CharField("رقم الموديل", max_length=255, null=True, blank=True)
    size = models.CharField("المقاس", max_length=255, null=True, blank=True)
    total = models.FloatField("الاجمالي", null=True, blank=True)

    class Meta:
        abstract = True

class KardonBaseModel(IDBaseModel):
    color = models.CharField("اللون", max_length=255, null=True, blank=True)
    meters_count = models.IntegerField("عدد الامتار", null=True, blank=True)

    class Meta:
        abstract = True

class RubberBaseModel(IDBaseModel):
    width = models.CharField("عرض الاستك", max_length=255, null=True, blank=True)
    total_weight = models.FloatField("الوزن الاجمالي", null=True, blank=True)

    class Meta:
        abstract = True

class ThreadBaseModel(IDBaseModel):
    thread_code = models.CharField("كود الخيط", max_length=255, null=True, blank=True)
    color = models.CharField("اللون", max_length=255, null=True, blank=True)
    spools_count = models.IntegerField("عدد البكر", null=True, blank=True)

    class Meta:
        abstract = True

class GlueBaseModel(IDBaseModel):
    width = models.CharField("عرض اللزق", max_length=255, null=True, blank=True)
    cartons_count = models.IntegerField("عدد الكراتين", null=True, blank=True)

    class Meta:
        abstract = True

# Carton Models
class CartonSupplies(SupplierBaseModel, CartonBaseModel):
    bundle_count = models.IntegerField("عدد الربط", null=True, blank=True)
    quantity_per_bundle = models.IntegerField("الكمية في الربطة", null=True, blank=True)
    excess = models.IntegerField("الفرط", null=True, blank=True)

class CartonStock(BaseModel, CartonBaseModel):
    pass

class PackagingCarton(PackagingBaseModel, CartonBaseModel):
    carton_count = models.IntegerField("عدد الكرتون", null=True, blank=True)

class ReturnCarton(BaseModel, CartonBaseModel):
    carton_count = models.IntegerField("عدد الكرتون", null=True, blank=True)

# Hanger Models
class HangerSupplies(SupplierBaseModel, HangerBaseModel):
    pass

class HangerStock(BaseModel, HangerBaseModel):
    pass

class PackagingHanger(PackagingBaseModel, HangerBaseModel):
    pass

class ReturnHanger(BaseModel, HangerBaseModel):
    pass

# Sizer Models
class SizerSupplies(SupplierBaseModel, SizerBaseModel):
    pass

class SizerStock(BaseModel, SizerBaseModel):
    pass

class PackagingSizer(PackagingBaseModel, SizerBaseModel):
    pass

class ReturnSizer(BaseModel, SizerBaseModel):
    pass

# Bag Models
class BagSupplies(SupplierBaseModel, BagBaseModel):
    pass

class BagStock(BaseModel, BagBaseModel):
    pass

class PackagingBag(PackagingBaseModel, BagBaseModel):
    pass

class ReturnBag(BaseModel, BagBaseModel):
    pass

# HangTag Models
class HangTagSupplies(SupplierBaseModel, HangTagBaseModel):
    pass

class HangTagStock(BaseModel, HangTagBaseModel):
    pass

class PackagingHangTag(PackagingBaseModel, HangTagBaseModel):
    pass

class ReturnHangTag(BaseModel, HangTagBaseModel):
    pass

# HeatSeal Models
class HeatSealSupplies(SupplierBaseModel, HeatSealBaseModel):
    pass

class HeatSealStock(BaseModel, HeatSealBaseModel):
    pass

class PackagingHeatSeal(PackagingBaseModel, HeatSealBaseModel):
    pass

class ReturnHeatSeal(BaseModel, HeatSealBaseModel):
    pass

# TicketSatan Models
class TicketSatanSupplies(SupplierBaseModel, TicketSatanBaseModel):
    pass

class TicketSatanStock(BaseModel, TicketSatanBaseModel):
    code = models.CharField("الرمز", max_length=255, null=True, blank=True)

class PackagingTicketSatan(PackagingBaseModel, TicketSatanBaseModel):
    pass

class ReturnTicketSatan(BaseModel, TicketSatanBaseModel):
    pass

# Ticket Models
class TicketSupplies(SupplierBaseModel, TicketBaseModel):
    pass

class TicketStock(BaseModel, TicketBaseModel):
    pass

class PackagingTicket(PackagingBaseModel, TicketBaseModel):
    pass

class ReturnTicket(BaseModel, TicketBaseModel):
    pass

# TicketPrice Models
class TicketPriceSupplies(SupplierBaseModel, TicketPriceBaseModel):
    pass

class TicketPriceStock(BaseModel, TicketPriceBaseModel):
    pass

class PackagingTicketPrice(PackagingBaseModel, TicketPriceBaseModel):
    pass

class ReturnTicketPrice(BaseModel, TicketPriceBaseModel):
    pass

# Kardon Models
class KardonSupplies(SupplierBaseModel, KardonBaseModel):
    pass

class KardonStock(BaseModel, KardonBaseModel):
    pass

class PackagingKardon(PackagingBaseModel, KardonBaseModel):
    pass

class ReturnKardon(BaseModel, KardonBaseModel):
    pass

# Rubber Models
class RubberSupplies(SupplierBaseModel, RubberBaseModel):
    pass

class RubberStock(BaseModel, RubberBaseModel):
    pass

class PackagingRubber(PackagingBaseModel, RubberBaseModel):
    pass

class ReturnRubber(BaseModel, RubberBaseModel):
    pass

# Thread Models
class ThreadSupplies(SupplierBaseModel, ThreadBaseModel):
    pass

class ThreadStock(BaseModel, ThreadBaseModel):
    pass

class PackagingThread(PackagingBaseModel, ThreadBaseModel):
    pass

# Glue Models
class GlueSupplies(SupplierBaseModel, GlueBaseModel):
    pass

class GlueStock(BaseModel, GlueBaseModel):
    pass

class PackagingGlue(PackagingBaseModel, GlueBaseModel):
    pass

class Updates(models.Model):
    date = models.DateTimeField(auto_now_add=True)
