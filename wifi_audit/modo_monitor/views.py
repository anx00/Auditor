import ast
import datetime

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_celery_results.models import TaskResult

from modo_monitor.models import access_point, device
from modo_monitor.network_scanner import networkscanner, connect_to_ap
from wifi_audit.celery import app
from . import utils
from .tasks import intensive_scan
from env import MONITOR_INTERFACE
from django.conf import settings

# Create your views here.
@login_required(login_url='login')
def modo_monitor(request):

    aps_temp = networkscanner.start_sniffing(MONITOR_INTERFACE)

    for ap in aps_temp:
        bssid = ap.upper()
        ssid = aps_temp[ap]['ssid']
        rssi = aps_temp[ap]['rssi']
        channel = aps_temp[ap]['channel']
        security_protocol = utils.convert_list_to_string(aps_temp[ap]['crypto'], ', ')
        spectrum = aps_temp[ap]['spectrum']
        frecuency = aps_temp[ap]['frecuency']
        signal_quality = aps_temp[ap]['signal_quality']
        rates = utils.convert_list_to_string(aps_temp[ap]['rates'], ', ')
        central_channel = aps_temp[ap]['central_channel']
        channel_bandwidth = aps_temp[ap]['channel_bandwidth']
        distance_ap = aps_temp[ap]['fspl']
        manufacturer = aps_temp[ap]['manufacturer']
        cipher_algorithm = aps_temp[ap]['cipher']
        auth_crypto = aps_temp[ap]['suite']
        beacons = aps_temp[ap]['beacons']
        timestamp = aps_temp[ap]['timestamp']
        clientes = aps_temp[ap]['clients']
        device_id = settings.DEVICE_ID

        if networkscanner.deauth_packets(ap) != 1:
            deauth_frames = networkscanner.deauth_packets(ap)['contador']
            deauth_frames_first_seen = networkscanner.deauth_packets(ap)['first_seen']
            deauth_frames_last_seen = networkscanner.deauth_packets(ap)['last_seen']

        else:
            deauth_frames = 0
            deauth_frames_first_seen = ""
            deauth_frames_last_seen = ""

        if access_point.objects.filter(bssid=ap.upper()).exists() == False:
            access_point.objects.create(ssid=ssid, bssid=bssid, device_id=device_id, rssi=rssi, channel=channel, security_protocol=security_protocol,
                                        spectrum=spectrum, frecuency=frecuency, signal_quality=signal_quality,
                                        rates=rates, manufacturer=manufacturer, central_channel=central_channel,
                                        channel_bandwidth=channel_bandwidth, distance_ap=distance_ap, cipher_algorithm=cipher_algorithm, auth_crypto=auth_crypto,
                                        beacons=beacons, timestamp=timestamp, deauth_frames=deauth_frames,
                                        deauth_last_seen=deauth_frames_last_seen,
                                        deauth_first_seen=deauth_frames_first_seen)

        else:
            access_point.objects.filter(bssid=bssid).update(rssi=rssi, channel=channel, frecuency=frecuency,
                                                            signal_quality=signal_quality, rates=rates,
                                                            central_channel=central_channel,
                                                            channel_bandwidth=channel_bandwidth, distance_ap=distance_ap,
                                                            cipher_algorithm=cipher_algorithm, auth_crypto=auth_crypto, beacons=beacons,
                                                            timestamp=timestamp,
                                                            deauth_frames=deauth_frames,
                                                            deauth_last_seen=deauth_frames_last_seen,
                                                            deauth_first_seen=deauth_frames_first_seen)
            if clientes is not []:
                for client in clientes:
                    cliente = client['mac'].upper()
                    connected_to = client['connected_to'].upper()
                    manufacturer = client['manufacturer']
                    device_id = settings.DEVICE_ID
                    if device.objects.filter(mac=cliente).exists() == False:
                        device.objects.create(connected_to=connected_to, mac=cliente, manufacturer=manufacturer,
                                              ap_id=access_point.objects.get(bssid=connected_to), device_id=device_id)

    aps = access_point.objects.all().order_by('-rssi')
    context = {"aps": aps}

    return render(request, "modo_monitor/modo_monitor.html", context)


@login_required(login_url='login')
def ver_aps(request):
    interfaces = MONITOR_INTERFACE

    aps = access_point.objects.all().order_by('id')

    context = {"aps": aps, "interfaces": interfaces}

    return render(request, "modo_monitor/ver_aps.html", context)


@login_required(login_url='login')
def ap_info(request, id):
    ap = access_point.objects.get(id=id)
    devices = list(device.objects.filter(connected_to=ap.bssid))

    context = {"ap": ap, "devices": devices}

    return render(request, "modo_monitor/ap_info.html", context)


@login_required(login_url='login')
def ap_seguridad(request, id):
    ap = access_point.objects.get(id=id)

    context = {"ap": ap}

    return render(request, "modo_monitor/ap_seguridad.html", context)


@login_required(login_url='login')
def ap_senal(request, id):
    ap = access_point.objects.get(id=id)

    context = {"ap": ap}

    return render(request, "modo_monitor/ap_senal.html", context)


@login_required(login_url='login')
def connection(request, id):
    ap = access_point.objects.get(id=id)

    ssid = ap.ssid

    if connect_to_ap.check_connected(ssid) == 0:
        message = "Already connected to " + ssid
        context = {"message": message}
    else:
        context = {"ap": ap}

    return render(request, "modo_monitor/connection.html", context)


@login_required(login_url='login')
def connected(request, id):
    ap = access_point.objects.get(id=id)

    ssid = ap.ssid

    password = request.POST.get('password')

    news = connect_to_ap.connect(ssid, password)

    if news == []:
        message = "Incorrect Password or AP out of range"
        new_ssid = ""
        new_bssid = ""
    else:
        new_ssid = news[0]
        new_bssid = news[1]
        message = "Connected"

    context = {"ssid": new_ssid, "bssid": new_bssid, "message": message}

    return render(request, "modo_monitor/connected.html", context)


@login_required(login_url='login')
def captura_paquetes(request):
    return render(request, "modo_monitor/captura_paquetes.html")


@login_required(login_url='login')
@csrf_exempt
def personal_scan(request, id):
    ap = access_point.objects.get(id=id)
    mac = ap.bssid.lower()
    interfaces = MONITOR_INTERFACE
    time_created = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    try:
        running_tasks = app.control.inspect().active()
    except:
        running_tasks = None

    flag = 0
    if running_tasks is not None:
        for task in running_tasks:
            if running_tasks[task]:
                i = 0
                while i < len(running_tasks[task]):
                    running_bssid = running_tasks[task][i]['args'][1]
                    if running_bssid == mac:
                        flag = 1
                    i += 1

    if request.method == "POST":
        time = float(request.POST.get('scan_time')) * 60
        TaskResult.objects.filter(task_args__contains=mac).delete()
        intensive_scan.delay(interfaces, mac, time, time_created)

    task = TaskResult.objects.filter(task_args__contains=mac)

    if task:
        for element in task:
            if element.status == "SUCCESS":
                result = ast.literal_eval(element.result)
                date_created = element.task_args.strip('()"').split(",")[3].strip("'").replace(" '", "")
                date_finished = str(element.date_done.strftime("%Y-%m-%d %H:%M:%S"))
                deauth_frames = result["deauth"]
                auth_frames = result["auth"]
                disas_frames = result["disas"]
                assoreq_frames = result["assoreq"]
                assoresp_frames = result["assoresp"]

                context = {"result": task, "deauth": deauth_frames, "auth": auth_frames, "disas": disas_frames,
                           "assosreq": assoreq_frames,
                           "assoresp": assoresp_frames, "flag": flag, "date_created": date_created,
                           "date_finished": date_finished}

            else:
                context = {"flag": flag}

        return render(request, "modo_monitor/personal_scan.html", context)

    else:

        return render(request, "modo_monitor/personal_scan.html", context={"result": task, "flag": flag})
