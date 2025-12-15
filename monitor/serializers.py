from rest_framework import serializers
from .models import LogAlert, StatDaily


class LogAlertSerializer(serializers.ModelSerializer):
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)

    class Meta:
        model = LogAlert
        fields = '__all__'


class StatDailySerializer(serializers.ModelSerializer):
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)

    class Meta:
        model = StatDaily
        fields = '__all__'
