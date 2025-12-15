from django.contrib import admin
from .models import SysAdmin, SysStaff, AppUser


@admin.register(SysAdmin)
class SysAdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'permission', 'created_at']
    search_fields = ['username']


@admin.register(SysStaff)
class SysStaffAdmin(admin.ModelAdmin):
    list_display = ['staff_id', 'name', 'phone', 'region_code', 'created_at']
    search_fields = ['staff_id', 'name', 'phone']
    list_filter = ['region_code']


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'balance', 'created_at']
    search_fields = ['username']
