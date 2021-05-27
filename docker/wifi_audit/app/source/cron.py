from django.core import serializers
import requests
from modo_monitor.models import access_point, device
from analizador_wifi.models import dispositivos
from env import SERVER_ENDPOINT

def upload_db():

    aps = access_point.objects.all().order_by('id')
    devices = dispositivos.objects.all().order_by('id')
    connected_devices = device.objects.all().order_by('id')

    data_aps = serializers.serialize("json", aps)
    data_devices = serializers.serialize("json", devices)
    data_connected_devices = serializers.serialize("json", connected_devices)

    data = [data_aps, data_devices, data_connected_devices]

    request = requests.post(url=SERVER_ENDPOINT, json=data)
    print(request)

