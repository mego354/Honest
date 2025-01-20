from django.contrib import admin
from .models import Model, Piece, SizeAmount


class PieceInline(admin.TabularInline):  # Use TabularInline for related Pieces
    model = Piece
    extra = 1  # Number of empty rows to display for adding new pieces
    fields = ('type', 'size', 'available_amount', 'used_amount')  # Editable fields in the inline
    verbose_name_plural = "القطع"  # Name for the inline section in the admin


class SizeAmountInline(admin.TabularInline):  # Inline configuration for related SizeAmounts
    model = SizeAmount
    extra = 1  # Number of empty rows to display for adding new size amounts
    fields = ('size', 'amount')  # Editable fields in the inline
    verbose_name_plural = "المقاسات والكمية"  # Name for the inline section in the admin


@admin.register(Model)
class ModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'model_number')  # Display these fields in the list view
    search_fields = ('model_number',)  # Enable search by model number
    list_filter = ('model_number',)  # Add filters for model number
    ordering = ('id',)  # Order models by ID
    inlines = [PieceInline, SizeAmountInline]  # Include related models inline


@admin.register(Piece)
class PieceAdmin(admin.ModelAdmin):
    list_display = ('model', 'type', 'size', 'available_amount', 'used_amount')  # Fields to display
    search_fields = ('type', 'size', 'model__model_number')  # Enable search for type, size, and model number
    list_filter = ('type', 'size', 'model')  # Filters for type, size, and model
    ordering = ('model', 'type')  # Order by model and type


@admin.register(SizeAmount)
class SizeAmountAdmin(admin.ModelAdmin):
    list_display = ('model', 'size', 'amount')  # Fields to display
    search_fields = ('size', 'model__model_number')  # Enable search for size and model number
    list_filter = ('size', 'model')  # Filters for size and model
    ordering = ('model', 'size')  # Order by model and size
 