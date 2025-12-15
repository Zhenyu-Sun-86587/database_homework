from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db import transaction
from .models import BizInventory, LogTransaction, LogRestock
from .serializers import BizInventorySerializer, LogTransactionSerializer, LogRestockSerializer

class BizInventoryViewSet(viewsets.ModelViewSet):
    queryset = BizInventory.objects.all()
    serializer_class = BizInventorySerializer

class LogTransactionViewSet(viewsets.ModelViewSet):
    queryset = LogTransaction.objects.all()
    serializer_class = LogTransactionSerializer

    def perform_create(self, serializer):
        """
        模拟数据库触发器：创建交易记录时，自动扣减对应库存和用户余额
        """
        from users.models import AppUser
        
        with transaction.atomic():
            instance = serializer.save()
            
            # 1. 扣减用户余额
            try:
                user = AppUser.objects.select_for_update().get(pk=instance.user.id)
                if user.balance < instance.amount:
                    raise Exception("Insufficient balance")
                user.balance -= instance.amount
                user.save()
            except AppUser.DoesNotExist:
                raise Exception("User not found")
            
            # 2. 获取对应的库存记录并扣减
            try:
                inventory = BizInventory.objects.select_for_update().get(
                    machine=instance.machine,
                    product=instance.product
                )
                
                if inventory.current_stock > 0:
                    inventory.current_stock -= 1
                    inventory.save()
                else:
                    raise Exception("Inventory not sufficient")
            except BizInventory.DoesNotExist:
                raise Exception("Inventory record not found")

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class LogRestockViewSet(viewsets.ModelViewSet):
    queryset = LogRestock.objects.all()
    serializer_class = LogRestockSerializer

    def perform_create(self, serializer):
        """
        模拟数据库触发器：创建补货记录时，自动增加对应库存
        """
        with transaction.atomic():
            instance = serializer.save()
            
            # 获取对应的库存记录
            try:
                inventory = BizInventory.objects.select_for_update().get(
                    machine=instance.machine,
                    product=instance.product
                )
                
                inventory.current_stock += instance.quantity
                # 确保不超过最大容量
                if inventory.current_stock > inventory.max_capacity:
                    inventory.current_stock = inventory.max_capacity
                
                inventory.save()
            except BizInventory.DoesNotExist:
                # 如果没有库存记录，可能需要新建，这里简化处理，假设必须先有库存记录
                raise Exception("Inventory record not found")
