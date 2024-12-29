from django.contrib import admin
from .models import Fabric, CutTransfer, ReturnTransfer, Statistics

class FabricAdmin(admin.ModelAdmin):
    list_display = ('id', 'fabric_code', 'fabric_name', 'color', 'roll', 'weight', 'date', 'dyehouse_name')
    search_fields = ('fabric_code', 'fabric_name', 'color')
    list_filter = ('dyehouse_name', 'date')

class CutTransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'fabric_code', 'fabric_name', 'color', 'roll', 'weight', 'date', 'model_number')
    search_fields = ('fabric_code', 'model_number')
    list_filter = ('date',)

class ReturnTransferAdmin(admin.ModelAdmin):
    list_display = ('id', 'fabric_code', 'fabric_name', 'color', 'roll', 'weight', 'date', 'model_number')
    search_fields = ('fabric_code', 'model_number')
    list_filter = ('date',)

class StatisticsAdmin(admin.ModelAdmin):
    list_display = ('id', 'fabric_code', 'fabric_name', 'color', 'roll', 'weight', 'date', 'dyehouse_name', 'model_number', 'movement_type')
    search_fields = ('fabric_code', 'model_number', 'movement_type')
    list_filter = ('dyehouse_name', 'movement_type', 'date')

# Register the models with the admin site
admin.site.register(Fabric, FabricAdmin)
admin.site.register(CutTransfer, CutTransferAdmin)
admin.site.register(ReturnTransfer, ReturnTransferAdmin)
admin.site.register(Statistics, StatisticsAdmin)
