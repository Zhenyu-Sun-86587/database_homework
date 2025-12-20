from rest_framework import serializers
from .models import BizInventory, LogTransaction, LogRestock

class BizInventorySerializer(serializers.ModelSerializer):
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = BizInventory
        fields = '__all__'

class LogTransactionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source='user.username', read_only=True)
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    profit = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = LogTransaction
        fields = '__all__'

class LogRestockSerializer(serializers.ModelSerializer):
    staff_name = serializers.CharField(source='staff.name', read_only=True)
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_cost = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = LogRestock
        fields = '__all__'

