"""
URL configuration for vending_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import SysAdminViewSet, SysStaffViewSet, AppUserViewSet
from resources.views import BizSupplierViewSet, BizMachineViewSet, BizProductViewSet
from inventory.views import BizInventoryViewSet, LogTransactionViewSet, LogRestockViewSet
from monitor.views import LogAlertViewSet, StatDailyViewSet

router = DefaultRouter()
# Users
router.register(r'sys-admins', SysAdminViewSet)
router.register(r'sys-staffs', SysStaffViewSet)
router.register(r'app-users', AppUserViewSet)
# Resources
router.register(r'suppliers', BizSupplierViewSet)
router.register(r'machines', BizMachineViewSet)
router.register(r'products', BizProductViewSet)
# Inventory
router.register(r'inventories', BizInventoryViewSet)
router.register(r'transactions', LogTransactionViewSet)
router.register(r'restocks', LogRestockViewSet)
# Monitor
router.register(r'alerts', LogAlertViewSet)
router.register(r'stat-daily', StatDailyViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
]

