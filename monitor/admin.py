from django.contrib import admin
from .models import LogAlert, StatDaily


@admin.register(LogAlert)
class LogAlertAdmin(admin.ModelAdmin):
    list_display = ['id', 'machine', 'alert_type', 'message', 'created_at']
    search_fields = ['machine__machine_code', 'message']
    list_filter = ['alert_type', 'machine', 'created_at']
    date_hierarchy = 'created_at'
    readonly_fields = ['machine', 'alert_type', 'message', 'created_at']  # 只读，由触发器自动生成


@admin.register(StatDaily)
class StatDailyAdmin(admin.ModelAdmin):
    list_display = ['id', 'date', 'machine', 'total_revenue', 'order_count', 'alert_count']
    search_fields = ['machine__machine_code']
    list_filter = ['machine', 'date']
    date_hierarchy = 'date'
