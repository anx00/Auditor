from rest_framework import serializers
from modo_monitor.models import access_point, device
from analizador_wifi.models import dispositivos


class APSerializer(serializers.ModelSerializer):
    class Meta:
        model = access_point
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = dispositivos
        fields = '__all__'


class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = device
        fields = '__all__'
