from django.contrib import admin
from .models import (
    CartonSupplies, CartonStock, PackagingCarton, ReturnCarton,
    HangerSupplies, HangerStock, PackagingHanger, ReturnHanger,
    SizerSupplies, SizerStock, PackagingSizer, ReturnSizer,
    BagSupplies, BagStock, PackagingBag, ReturnBag,
    HangTagSupplies, HangTagStock, PackagingHangTag, ReturnHangTag,
    HeatSealSupplies, HeatSealStock, PackagingHeatSeal, ReturnHeatSeal,
    TicketSatanSupplies, TicketSatanStock, PackagingTicketSatan, ReturnTicketSatan,
    TicketSupplies, TicketStock, PackagingTicket, ReturnTicket,
    TicketPriceSupplies, TicketPriceStock, PackagingTicketPrice, ReturnTicketPrice,
    KardonSupplies, KardonStock, PackagingKardon, ReturnKardon,
    RubberSupplies, RubberStock, PackagingRubber, ReturnRubber,
    ThreadSupplies, ThreadStock, PackagingThread,
    GlueSupplies, GlueStock, PackagingGlue
)

# Carton Models
@admin.register(CartonSupplies)
class CartonSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "model_number", "length", "width", "height", "bundle_count", "quantity_per_bundle", "excess", "total_quantity"]

@admin.register(CartonStock)
class CartonStockAdmin(admin.ModelAdmin):
    list_display = ["model_number", "length", "width", "height", "total_quantity"]

@admin.register(PackagingCarton)
class PackagingCartonAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "model_number", "length", "width", "height", "carton_count"]

@admin.register(ReturnCarton)
class ReturnCartonAdmin(admin.ModelAdmin):
    list_display = ["date", "model_number", "length", "width", "height", "carton_count"]

# Hanger Models
@admin.register(HangerSupplies)
class HangerSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "hanger_number", "color", "sets_count", "hangers_count"]

@admin.register(HangerStock)
class HangerStockAdmin(admin.ModelAdmin):
    list_display = ["hanger_number", "color", "sets_count", "hangers_count"]

@admin.register(PackagingHanger)
class PackagingHangerAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "hanger_number", "color", "sets_count", "hangers_count"]

@admin.register(ReturnHanger)
class ReturnHangerAdmin(admin.ModelAdmin):
    list_display = ["date", "hanger_number", "color", "sets_count", "hangers_count"]

# Sizer Models
@admin.register(SizerSupplies)
class SizerSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "size", "color", "sizer_count"]

@admin.register(SizerStock)
class SizerStockAdmin(admin.ModelAdmin):
    list_display = ["size", "color", "sizer_count"]

@admin.register(PackagingSizer)
class PackagingSizerAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "size", "color", "sizer_count"]

@admin.register(ReturnSizer)
class ReturnSizerAdmin(admin.ModelAdmin):
    list_display = ["date", "size", "color", "sizer_count"]

# Bag Models
@admin.register(BagSupplies)
class BagSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "bag_length", "bag_width", "weight", "bags_per_kilo", "weight"]

@admin.register(BagStock)
class BagStockAdmin(admin.ModelAdmin):
    list_display = ["bag_length", "bag_width", "weight", "bags_per_kilo", "weight"]

@admin.register(PackagingBag)
class PackagingBagAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "bag_length", "bag_width", "weight", "weight"]

@admin.register(ReturnBag)
class ReturnBagAdmin(admin.ModelAdmin):
    list_display = ["date", "bag_length", "bag_width", "weight", "weight"]

# HangTag Models
@admin.register(HangTagSupplies)
class HangTagSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "type", "quantity"]

@admin.register(HangTagStock)
class HangTagStockAdmin(admin.ModelAdmin):
    list_display = ["type", "quantity"]

@admin.register(PackagingHangTag)
class PackagingHangTagAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "type", "quantity"]

@admin.register(ReturnHangTag)
class ReturnHangTagAdmin(admin.ModelAdmin):
    list_display = ["date", "type", "quantity"]

# HeatSeal Models
@admin.register(HeatSealSupplies)
class HeatSealSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "type", "quantity", "size"]

@admin.register(HeatSealStock)
class HeatSealStockAdmin(admin.ModelAdmin):
    list_display = ["type", "quantity", "size"]

@admin.register(PackagingHeatSeal)
class PackagingHeatSealAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "type", "quantity", "size"]

@admin.register(ReturnHeatSeal)
class ReturnHeatSealAdmin(admin.ModelAdmin):
    list_display = ["date", "type", "quantity", "size"]

# TicketSatan Models
@admin.register(TicketSatanSupplies)
class TicketSatanSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "model_number", "size", "cotton_percentage", "polyester_percentage", "upc_number", "pieces_count"]

@admin.register(TicketSatanStock)
class TicketSatanStockAdmin(admin.ModelAdmin):
    list_display = ["code", "model_number", "size", "cotton_percentage", "polyester_percentage", "upc_number", "pieces_count"]

@admin.register(PackagingTicketSatan)
class PackagingTicketSatanAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "model_number", "size", "cotton_percentage", "polyester_percentage", "pieces_count"]

@admin.register(ReturnTicketSatan)
class ReturnTicketSatanAdmin(admin.ModelAdmin):
    list_display = ["date", "model_number", "size", "cotton_percentage", "polyester_percentage", "pieces_count"]

# Ticket Models
@admin.register(TicketSupplies)
class TicketSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "type", "size", "pieces_count"]

@admin.register(TicketStock)
class TicketStockAdmin(admin.ModelAdmin):
    list_display = ["type", "size", "pieces_count"]

@admin.register(PackagingTicket)
class PackagingTicketAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "type", "size", "pieces_count"]

@admin.register(ReturnTicket)
class ReturnTicketAdmin(admin.ModelAdmin):
    list_display = ["date", "type", "size", "pieces_count"]

# TicketPrice Models
@admin.register(TicketPriceSupplies)
class TicketPriceSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "model_number", "size", "total"]

@admin.register(TicketPriceStock)
class TicketPriceStockAdmin(admin.ModelAdmin):
    list_display = ["model_number", "size", "total"]

@admin.register(PackagingTicketPrice)
class PackagingTicketPriceAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "model_number", "size", "total"]

@admin.register(ReturnTicketPrice)
class ReturnTicketPriceAdmin(admin.ModelAdmin):
    list_display = ["date", "model_number", "size", "total"]

# Kardon Models
@admin.register(KardonSupplies)
class KardonSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "color", "meters_count"]

@admin.register(KardonStock)
class KardonStockAdmin(admin.ModelAdmin):
    list_display = ["color", "meters_count"]

@admin.register(PackagingKardon)
class PackagingKardonAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "color", "meters_count"]

@admin.register(ReturnKardon)
class ReturnKardonAdmin(admin.ModelAdmin):
    list_display = ["date", "color", "meters_count"]

# Rubber Models
@admin.register(RubberSupplies)
class RubberSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "width", "total_weight"]

@admin.register(RubberStock)
class RubberStockAdmin(admin.ModelAdmin):
    list_display = ["width", "total_weight"]

@admin.register(PackagingRubber)
class PackagingRubberAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "width", "total_weight"]

@admin.register(ReturnRubber)
class ReturnRubberAdmin(admin.ModelAdmin):
    list_display = ["date", "width", "total_weight"]

# Thread Models
@admin.register(ThreadSupplies)
class ThreadSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "thread_code", "color", "spools_count"]

@admin.register(ThreadStock)
class ThreadStockAdmin(admin.ModelAdmin):
    list_display = ["thread_code", "color", "spools_count"]

@admin.register(PackagingThread)
class PackagingThreadAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "thread_code", "color", "spools_count"]

# Glue Models
@admin.register(GlueSupplies)
class GlueSuppliesAdmin(admin.ModelAdmin):
    list_display = ["date", "supplier_name", "width", "cartons_count"]

@admin.register(GlueStock)
class GlueStockAdmin(admin.ModelAdmin):
    list_display = ["width", "cartons_count"]

@admin.register(PackagingGlue)
class PackagingGlueAdmin(admin.ModelAdmin):
    list_display = ["date", "factory", "width", "cartons_count"]