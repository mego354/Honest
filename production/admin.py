from django.contrib import admin
from django.utils.html import format_html
from .models import Model, SizeAmount, Piece, ProductionPiece, Carton, Packing


class SizeAmountInline(admin.TabularInline):
    model = SizeAmount
    extra = 1


class PieceInline(admin.TabularInline):
    model = Piece
    extra = 1


class PackingInline(admin.TabularInline):
    model = Packing
    extra = 1


class ProductionPieceInline(admin.TabularInline):
    model = ProductionPiece
    extra = 1


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ("id", "model_number", "created_at", "ended_at", "is_active", "is_archive", "usage_percentage_display")
    list_filter = ("created_at", "ended_at", "is_archive")
    search_fields = ("model_number",)
    inlines = [SizeAmountInline, PieceInline]  # Keep the inlines that relate to Model

    def is_active(self, obj):
        return obj.is_active()
    is_active.boolean = True

    def usage_percentage_display(self, obj):
        data = obj.get_usage_percentage()
        return format_html(
            '<div style="width:100px; background-color:{}; color:white; padding:3px; text-align:center;">{}%</div>',
            data["percent_style"],
            data["percent"]
        )
    usage_percentage_display.short_description = "Usage Percentage"


@admin.register(SizeAmount)
class SizeAmountAdmin(admin.ModelAdmin):
    list_display = ("model", "size", "amount", "editable")
    list_filter = ("editable",)
    search_fields = ("model__model_number", "size")


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ("model", "type", "size", "available_amount", "used_amount", "packing_available_amount", "packing_used_amount")
    list_filter = ("type", "size")
    search_fields = ("model__model_number", "type", "size")
    inlines = [PackingInline]  # Packing has a ForeignKey to Piece


@admin.register(ProductionPiece)
class ProductionPieceAdmin(admin.ModelAdmin):
    list_display = ("piece", "used_amount", "factory", "comment", "created_at")
    list_filter = ("created_at", "factory")
    search_fields = ("piece__model__model_number", "factory")


@admin.register(Carton)
class CartonAdmin(admin.ModelAdmin):
    list_display = ("model", "length", "width", "height", "comment")
    search_fields = ("model__model_number",)


@admin.register(Packing)
class PackingAdmin(admin.ModelAdmin):
    list_display = ("piece", "carton", "used_amount", "created_at")
    list_filter = ("created_at",)
    search_fields = ("piece__model__model_number",)
