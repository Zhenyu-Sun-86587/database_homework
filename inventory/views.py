from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db import transaction
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal
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
        创建交易记录时：
        1. 检查库存是否充足
        2. 自动记录成本价（用于利润计算）
        3. 扣减用户余额
        注意：库存扣减由数据库触发器 after_transaction_insert 自动完成
        """
        from users.models import AppUser
        from resources.models import BizProduct
        
        with transaction.atomic():
            # 获取商品的成本价
            product_id = self.request.data.get('product')
            machine_id = self.request.data.get('machine')
            
            try:
                product = BizProduct.objects.get(pk=product_id)
                cost_price = product.cost_price
            except BizProduct.DoesNotExist:
                cost_price = Decimal('0')
            
            # 检查库存是否充足（触发器会扣减，这里只检查）
            try:
                inventory = BizInventory.objects.get(
                    machine_id=machine_id,
                    product_id=product_id
                )
                if inventory.current_stock <= 0:
                    raise Exception("Inventory not sufficient")
            except BizInventory.DoesNotExist:
                raise Exception("Inventory record not found")
            
            # 保存交易记录，包含成本价
            # 触发器会自动扣减库存
            instance = serializer.save(cost_price=cost_price)
            
            # 扣减用户余额
            try:
                user = AppUser.objects.select_for_update().get(pk=instance.user.id)
                if user.balance < instance.amount:
                    raise Exception("Insufficient balance")
                user.balance -= instance.amount
                user.save()
            except AppUser.DoesNotExist:
                raise Exception("User not found")

    def perform_destroy(self, instance):
        """
        删除交易记录时（退货）：
        1. 恢复用户余额
        2. 恢复库存（需要手动，因为触发器只处理INSERT）
        """
        from users.models import AppUser
        
        with transaction.atomic():
            # 1. 恢复用户余额
            try:
                user = AppUser.objects.select_for_update().get(pk=instance.user.id)
                user.balance += instance.amount
                user.save()
            except AppUser.DoesNotExist:
                pass
            
            # 2. 恢复库存（触发器不处理DELETE，需要手动）
            try:
                inventory = BizInventory.objects.select_for_update().get(
                    machine=instance.machine,
                    product=instance.product
                )
                inventory.current_stock += 1
                if inventory.current_stock > inventory.max_capacity:
                    inventory.current_stock = inventory.max_capacity
                inventory.save()
            except BizInventory.DoesNotExist:
                pass
            
            # 3. 删除记录
            instance.delete()

    def create(self, request, *args, **kwargs):
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """
        财务统计 API
        支持 period 参数: today, week, month
        """
        period = request.query_params.get('period', 'today')
        today = timezone.now().date()
        
        if period == 'today':
            start_date = today
        elif period == 'week':
            start_date = today - timedelta(days=7)
        elif period == 'month':
            start_date = today - timedelta(days=30)
        else:
            start_date = today
        
        transactions = LogTransaction.objects.filter(created_at__date__gte=start_date)
        
        total_revenue = transactions.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')
        total_cost = transactions.aggregate(Sum('cost_price'))['cost_price__sum'] or Decimal('0')
        total_profit = total_revenue - total_cost
        order_count = transactions.count()
        
        return Response({
            'period': period,
            'total_revenue': float(total_revenue),
            'total_cost': float(total_cost),
            'total_profit': float(total_profit),
            'order_count': order_count,
        })


class LogRestockViewSet(viewsets.ModelViewSet):
    queryset = LogRestock.objects.all()
    serializer_class = LogRestockSerializer

    def perform_create(self, serializer):
        """
        创建补货记录时：
        1. 自动计算成本
        注意：库存增加由数据库触发器 after_restock_insert 自动完成
        """
        from resources.models import BizProduct
        
        with transaction.atomic():
            # 获取商品进价
            product_id = self.request.data.get('product')
            quantity = int(self.request.data.get('quantity', 0))
            
            try:
                product = BizProduct.objects.get(pk=product_id)
                unit_cost = product.cost_price
                total_cost = unit_cost * quantity
            except BizProduct.DoesNotExist:
                unit_cost = Decimal('0')
                total_cost = Decimal('0')
            
            # 保存补货记录，包含单位成本信息
            # 触发器会自动增加库存
            # total_cost 通过 @property 自动计算，无需存储
            serializer.save(unit_cost=unit_cost)

    def perform_destroy(self, instance):
        """
        删除补货记录时：回滚库存（需要手动，因为触发器只处理INSERT）
        """
        with transaction.atomic():
            try:
                inventory = BizInventory.objects.select_for_update().get(
                    machine=instance.machine,
                    product=instance.product
                )
                inventory.current_stock -= instance.quantity
                if inventory.current_stock < 0:
                    inventory.current_stock = 0
                inventory.save()
            except BizInventory.DoesNotExist:
                pass
            
            instance.delete()

    @action(detail=False, methods=['get'])
    def cost_statistics(self, request):
        """
        补货成本统计 API
        """
        period = request.query_params.get('period', 'month')
        today = timezone.now().date()
        
        if period == 'week':
            start_date = today - timedelta(days=7)
        else:
            start_date = today - timedelta(days=30)
        
        restocks = LogRestock.objects.filter(created_at__date__gte=start_date)
        
        # 由于 total_cost 是计算属性，需要在 Python 中求和
        total_cost = sum(r.total_cost for r in restocks)
        total_quantity = restocks.aggregate(Sum('quantity'))['quantity__sum'] or 0
        
        return Response({
            'period': period,
            'total_cost': float(total_cost),
            'total_quantity': total_quantity,
            'restock_count': restocks.count()
        })
