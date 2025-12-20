from rest_framework import serializers
from .models import LogAlert, StatDaily


class LogAlertSerializer(serializers.ModelSerializer):
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)

    class Meta:
        model = LogAlert
        fields = '__all__'


class StatDailySerializer(serializers.ModelSerializer):
    machine_code = serializers.CharField(source='machine.machine_code', read_only=True)
    total_profit = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = StatDaily
        fields = '__all__'

