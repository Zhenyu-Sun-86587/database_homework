from django.contrib import admin
from .models import BizInventory, LogTransaction, LogRestock


@admin.register(BizInventory)
class BizInventoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'machine', 'product', 'current_stock', 'max_capacity']
    search_fields = ['machine__machine_code', 'product__name']
    list_filter = ['machine']


@admin.register(LogTransaction)
class LogTransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'machine', 'product', 'amount', 'created_at']
    search_fields = ['user__username', 'machine__machine_code', 'product__name']
    list_filter = ['machine', 'created_at']
    date_hierarchy = 'created_at'


@admin.register(LogRestock)
class LogRestockAdmin(admin.ModelAdmin):
    list_display = ['id', 'staff', 'machine', 'product', 'quantity', 'created_at']
    search_fields = ['staff__name', 'machine__machine_code', 'product__name']
    list_filter = ['machine', 'staff', 'created_at']
    date_hierarchy = 'created_at'
