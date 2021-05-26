from billiard.context import Process

from scapy.all import *
from scapy.layers.dot11 import *
from modo_monitor import utils

data = {}

# Detect Deauthentication frames
def deauth_packet(time, packet, ap):
    addr1 = packet[Dot11].addr1
    addr2 = packet[Dot11].addr2

    if addr1 == ap:
        target = addr2
    else:
        target = addr1

    reason = packet[Dot11Deauth].reason

    deauth_dict = {"target": target, "reason": reason, "time": time}

    return deauth_dict


# Detect Authentication frames
def auth_packet(time, packet, ap):
    addr1 = packet[Dot11].addr1
    addr2 = packet[Dot11].addr2

    if addr1 == ap:
        target = addr2
    else:
        target = addr1

    algo = packet[Dot11Auth].algo
    seqnum = packet[Dot11Auth].seqnum
    status = status_code[packet[Dot11Auth].status]

    auth_dict = {"target": target, "algo": algo, "seqnum": seqnum, "status": status, "time": time}

    return auth_dict


# Detect Disassociation frames
def disas_packet(time, packet, ap):
    addr1 = packet[Dot11].addr1
    addr2 = packet[Dot11].addr2
    if addr1 == ap:
        target = addr2
    else:
        target = addr1

    reason = packet[Dot11Disas].reason

    disas_dict = {"target": target, "reason": reason, "time": time}

    return disas_dict


# Detect Association Request frames
def assoreq_packet(time, packet, ap):
    addr1 = packet[Dot11].addr1
    addr2 = packet[Dot11].addr2

    if addr1 == ap:
        target = addr2
    else:
        target = addr1

    # capability = packet[Dot11AssoReq].cap
    listen_interval = packet[Dot11AssoReq].listen_interval

    assoreq_dict = {"target": target, "listen_interval": listen_interval, "time": time}

    return assoreq_dict


# Detect Association Response frames
def assoresp_packet(time, packet, ap):
    addr1 = packet[Dot11].addr1
    addr2 = packet[Dot11].addr2

    if addr1 == ap:
        target = addr2
    else:
        target = addr1

    # capability = packet[Dot11AssoResp].cap
    status = packet[Dot11AssoResp].status
    aid = packet[Dot11AssoResp].AID

    assoresp_dict = {"target": target, "status": status, "aid": aid, "time": time}

    return assoresp_dict


def sniffer(ap):
    # Sniffing de APs

    def sniff_packets(p):
        time = str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

        if p.haslayer(Dot11):
            print(p.summary())

            if p.haslayer(Dot11Deauth):
                if "deauth" in data:
                    data["deauth"].append(deauth_packet(time, p, ap))
                else:
                    data["deauth"] = [deauth_packet(time, p, ap)]

            elif p.haslayer(Dot11Auth):
                if "auth" in data:
                    data["auth"].append(auth_packet(time, p, ap))
                else:
                    data["auth"] = [auth_packet(time, p, ap)]

            elif p.haslayer(Dot11Disas):
                if "disas" in data:
                    data["disas"].append(disas_packet(time, p, ap))
                else:
                    data["disas"] = [disas_packet(time, p, ap)]

            elif p.haslayer(Dot11AssoReq):
                if "assoreq" in data:
                    data["assoreq"].append(assoreq_packet(time, p, ap))
                else:
                    data["assoreq"] = [assoreq_packet(time, p, ap)]

            elif p.haslayer(Dot11AssoResp):
                if "assoresp" in data:
                    data["assoresp"].append(assoresp_packet(time, p, ap))
                else:
                    data["assoresp"] = [assoresp_packet(time, p, ap)]

    return sniff_packets

def check_interface():
    interfaces = os.listdir("/sys/class/net")
    for interface in interfaces:
        mode = subprocess.check_output("cat /sys/class/net/%s/type" % interface, shell=True).decode('utf-8').rstrip(
            "\n")
        if mode == "803":
            return interface


def scanner(interfaz, mac, timeout):
    # Esto simplemente es temporal porque la tarjeta va como quiere
    utils.restart_interface()

    # Creamos un proceso de multithreading de manera que va haciendo channel hopping
    p = Process(target=channel_hopper)
    p.start()

    # Definimos la interfaz
    interface = interfaz
    filter = "ether host %s" % mac

    # Iniciamos el sniffing
    sniff(iface=interface, prn=sniffer(mac), filter=filter, timeout=timeout)

    p.terminate()
    p.join()

    data["ap"] = mac
    if "deauth" not in data:
        data["deauth"] = []
    if "auth" not in data:
        data["auth"] = []
    if "disas" not in data:
        data["disas"] = []
    if "assoresp" not in data:
        data["assoresp"] = []
    if "assoreq" not in data:
        data["assoreq"] = []

    return data

# Changes channel randomly in range(1,15)
def channel_hopper():
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 36, 40, 44, 48]
    # Definimos la interfaz
    interface = "wlxdc4ef405cd9f"
    while True:
        try:
            # channel = random.randrange(1, 15)
            channel = random.choice(list)
            os.system("iwconfig %s channel %d" % (interface, channel))
            time.sleep(1)
        except KeyboardInterrupt:
            break
            # Capture interrupt signal and cleanup before exiting
