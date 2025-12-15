from rest_framework import serializers
from .models import BizSupplier, BizMachine, BizProduct

class BizSupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizSupplier
        fields = '__all__'

class BizMachineSerializer(serializers.ModelSerializer):
    class Meta:
        model = BizMachine
        fields = '__all__'

class BizProductSerializer(serializers.ModelSerializer):
    supplier_name = serializers.CharField(source='supplier.name', read_only=True)
    
    class Meta:
        model = BizProduct
        fields = '__all__'
