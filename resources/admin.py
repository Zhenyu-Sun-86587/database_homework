from django.contrib import admin
from .models import BizSupplier, BizMachine, BizProduct


@admin.register(BizSupplier)
class BizSupplierAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'contact', 'created_at']
    search_fields = ['name', 'contact']


@admin.register(BizMachine)
class BizMachineAdmin(admin.ModelAdmin):
    list_display = ['machine_code', 'location', 'status', 'region_code', 'created_at']
    search_fields = ['machine_code', 'location']
    list_filter = ['status', 'region_code']


@admin.register(BizProduct)
class BizProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'cost_price', 'sell_price', 'supplier', 'created_at']
    search_fields = ['name']
    list_filter = ['supplier']
