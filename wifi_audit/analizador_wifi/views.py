from django.shortcuts import render

from analizador_wifi.local_scanner.scanner import arp_scan, get_connected_bssid, get_connected_ssid, os_detection
from analizador_wifi.models import dispositivos
from django.contrib.auth.decorators import login_required

# Create your views here.
@login_required(login_url='login')
def analizador_wifi(request):
    result = arp_scan("192.168.1.1/24")
    # result = arp_scan("10.25.131.197/16")

    connected_ap = get_connected_bssid()

    for mapping in result:
        if dispositivos.objects.filter(ip=mapping['IP']).exists() == False:
            dispositivos.objects.create(ip=mapping['IP'], mac=mapping['MAC'], nombre_dispositivo=mapping['name'],
                                        last_seen=mapping['last_seen'], connected_to=connected_ap,
                                        vendor=mapping['vendor'], os="", osfamily="", type="")
        else:
            dispositivos.objects.filter(ip=mapping['IP']).update(last_seen=mapping['last_seen'])

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
    data = {"name": dispositivo.os, "osfamily": dispositivo.osfamily, "type": dispositivo.type}

    if dispositivo.os == "" and dispositivo.osfamily == "" and dispositivo.type == "":
        data = os_detection(dispositivo.ip)

        dispositivos.objects.filter(id=id).update(os=data['name'], osfamily=data['osfamily'], type=data['type'])
        context = {"dispositivo": dispositivo, "connected_ap": connected_ap, "data": data}

        return render(request, "analizador_wifi/dispositivo_info.html", context)

    context = {"dispositivo": dispositivo, "connected_ap": connected_ap, "data": data}

    return render(request, "analizador_wifi/dispositivo_info.html", context)
