from rest_framework import viewsets
from .models import BizSupplier, BizMachine, BizProduct
from .serializers import BizSupplierSerializer, BizMachineSerializer, BizProductSerializer

class BizSupplierViewSet(viewsets.ModelViewSet):
    queryset = BizSupplier.objects.all()
    serializer_class = BizSupplierSerializer

class BizMachineViewSet(viewsets.ModelViewSet):
    queryset = BizMachine.objects.all()
    serializer_class = BizMachineSerializer

class BizProductViewSet(viewsets.ModelViewSet):
    queryset = BizProduct.objects.all()
    serializer_class = BizProductSerializer
