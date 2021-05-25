import json

from api.models import access_point, dispositivos, device


def save_data(data):
    aps = json.loads(data[0])
    devices = json.loads(data[1])
    connected_devices = json.loads(data[2])

    # Save AP Data
    for element in aps:
        fields = element['fields']

        if access_point.objects.filter(bssid=fields['bssid']).exists() == False:
            access_point.objects.create(local_id=element['pk'], essid=fields['essid'], bssid=fields['bssid'], rssi=fields['rssi'],
                                        canal=fields['canal'], encriptacion=fields['encriptacion'],
                                        spectrum=fields['spectrum'], frecuencia=fields['frecuencia'],
                                        signal_quality=fields['signal_quality'],
                                        rates=fields['rates'], manufacturer=fields['manufacturer'],
                                        central_channel=fields['central_channel'],
                                        channel_bandwidth=fields['channel_bandwidth'], fspl=fields['fspl'],
                                        cipher=fields['cipher'], suite=fields['suite'],
                                        beacons=fields['beacons'], deauth_frames=fields['deauth_frames'],
                                        deauth_last_seen=fields['deauth_last_seen'],
                                        deauth_first_seen=fields['deauth_first_seen'])
    # Save Devices Data
    for element in devices:
        fields = element['fields']

        if dispositivos.objects.filter(mac=fields['mac']).exists() == False:
            dispositivos.objects.create(ip=fields['ip'], mac=fields['mac'],
                                        nombre_dispositivo=fields['nombre_dispositivo'],
                                        last_seen=fields['last_seen'], connected_to=fields['connected_to'],
                                        vendor=fields['vendor'], os=fields['os'], osfamily=fields['osfamily'],
                                        type=fields['type'])

    # Save Connected Devices Data
    for element in connected_devices:
        fields = element['fields']

        if device.objects.filter(mac_device=fields['mac_device']).exists() == False:
            device.objects.create(connected_to=fields['connected_to'], mac_device=fields['mac_device'], manufacturer=fields['manufacturer'],
                                  ap=access_point.objects.get(bssid=fields['connected_to']))
