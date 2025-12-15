from rest_framework import serializers
from .models import SysAdmin, SysStaff, AppUser

class SysAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysAdmin
        fields = '__all__'

class SysStaffSerializer(serializers.ModelSerializer):
    class Meta:
        model = SysStaff
        fields = '__all__'

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = '__all__'
