from rest_framework import viewsets
from .models import SysAdmin, SysStaff, AppUser
from .serializers import SysAdminSerializer, SysStaffSerializer, AppUserSerializer

class SysAdminViewSet(viewsets.ModelViewSet):
    queryset = SysAdmin.objects.all()
    serializer_class = SysAdminSerializer

class SysStaffViewSet(viewsets.ModelViewSet):
    queryset = SysStaff.objects.all()
    serializer_class = SysStaffSerializer

class AppUserViewSet(viewsets.ModelViewSet):
    queryset = AppUser.objects.all()
    serializer_class = AppUserSerializer
