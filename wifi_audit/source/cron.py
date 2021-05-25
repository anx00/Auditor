from django.core import serializers
import requests
from modo_monitor.models import access_point, device
from analizador_wifi.models import dispositivos

SERVER_ENDPOINT = "http://127.0.0.1:7000/api"

def upload_mongo():

    aps = access_point.objects.all().order_by('id')
    devices = dispositivos.objects.all().order_by('id')
    connected_devices = device.objects.all().order_by('id')

    data_aps = serializers.serialize("json", aps)
    data_devices = serializers.serialize("json", devices)
    data_connected_devices = serializers.serialize("json", connected_devices)

    data = [data_aps, data_devices, data_connected_devices]

    server_url = SERVER_ENDPOINT
    request = requests.post(url=server_url, json=data)

