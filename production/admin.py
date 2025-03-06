from django.contrib import admin
from django.utils.html import format_html
from .models import Factory, Model, SizeAmount, Piece, ProductionPiece, Carton, Packing


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
    list_display = ('id', 'model_number', 'created_at', 'is_archive', 'is_active_display', 'comments_count_display')
    search_fields = ('model_number',)
    list_filter = ('is_archive', 'created_at')
    ordering = ('-created_at',)
    inlines = [SizeAmountInline, PieceInline, PackingInline]
    readonly_fields = ('is_active_display', 'comments_count_display')

    def is_active_display(self, obj):
        return obj.is_active()
    is_active_display.short_description = "نشط"

    def comments_count_display(self, obj):
        return obj.comments_count()
    comments_count_display.short_description = "عدد التعليقات"


@admin.register(SizeAmount)
class SizeAmountAdmin(admin.ModelAdmin):
    list_display = ("model", "size", "amount", 'Packing_per_carton', "editable")
    list_filter = ("editable", 'Packing_per_carton',)
    search_fields = ("model__model_number", "size")


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ("model", "type", "size", "available_amount", "used_amount")
    list_filter = ("type", "size")
    search_fields = ("model__model_number", "type", "size")


@admin.register(ProductionPiece)
class ProductionPieceAdmin(admin.ModelAdmin):
    list_display = ("piece", "used_amount", "worked_factory", "comment", "created_at")
    list_filter = ("created_at", "worked_factory")
    search_fields = ("piece__model__model_number", "worked_factory")


@admin.register(Carton)
class CartonAdmin(admin.ModelAdmin):
    list_display = ("model", "length", "width", "height", "comment")
    search_fields = ("model__model_number",)


@admin.register(Packing)
class PackingAdmin(admin.ModelAdmin):
    list_display = ("model", "carton", "used_carton", "created_at")
    list_filter = ("created_at",)
    search_fields = ("piece__model__model_number",)

@admin.register(Factory)
class FactoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "statue")
    list_filter = ("statue",)
    search_fields = ("name",)
