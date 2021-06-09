from django.shortcuts import render

from analizador_wifi.local_scanner.scanner import arp_scan, get_connected_bssid, get_connected_ssid, os_detection
from analizador_wifi.models import dispositivos
from django.contrib.auth.decorators import login_required
from env import LOCAL_NETWORK
from django.conf import settings


# Create your views here.
@login_required(login_url='login')
def analizador_wifi(request):
    result = arp_scan(LOCAL_NETWORK)
    # result = arp_scan("10.25.131.197/16")

    connected_ap = get_connected_bssid()
    device_id = settings.DEVICE_ID

    for mapping in result:
        if dispositivos.objects.filter(ip=mapping['IP']).exists() == False:
            dispositivos.objects.create(ip=mapping['IP'], mac=mapping['MAC'], hostname=mapping['name'],
                                        timestamp=mapping['last_seen'], connected_to=connected_ap,
                                        manufacturer=mapping['vendor'], os_system="Unknown", os_family="Unknown", device_type="Unknown",
                                        device_id=device_id)
        else:
            dispositivos.objects.filter(ip=mapping['IP']).update(timestamp=mapping['last_seen'])

    dispositivo = dispositivos.objects.filter(connected_to=connected_ap).order_by('id')

    context = {"dispositivo": dispositivo}

    return render(request, "analizador_wifi/analizador_wifi.html", context)


@login_required(login_url='login')
def ver_dispositivos(request):
    # interfaces = connect_to_ap.check_interface_mode("managed")

    connected_ap = get_connected_bssid()

    dispositivo = dispositivos.objects.filter(connected_to=connected_ap).order_by('id')

    context = {"dispositivo": dispositivo, 'ap_bssid': connected_ap, "interfaces": "wlo1"}

    return render(request, "analizador_wifi/ver_dispositivos.html", context)


@login_required(login_url='login')
def dispositivo_info(request, id):
    dispositivo = dispositivos.objects.get(id=id)

    connected_ap = get_connected_ssid()
    data = {"name": dispositivo.os_system, "osfamily": dispositivo.os_family, "type": dispositivo.device_type}

    if dispositivo.os_system == "Unknown" and dispositivo.os_family == "Unknown" and dispositivo.device_type == "Unknown":
        data = os_detection(dispositivo.ip)

        dispositivos.objects.filter(id=id).update(os_system=data['name'], os_family=data['osfamily'], device_type=data['type'])
        context = {"dispositivo": dispositivo, "connected_ap": connected_ap, "data": data}

        return render(request, "analizador_wifi/dispositivo_info.html", context)

    context = {"dispositivo": dispositivo, "connected_ap": connected_ap, "data": data}

    return render(request, "analizador_wifi/dispositivo_info.html", context)
