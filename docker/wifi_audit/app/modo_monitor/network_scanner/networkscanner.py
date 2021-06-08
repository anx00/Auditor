from multiprocessing import Process

from scapy.all import *
from scapy.layers.dot11 import *

from modo_monitor import utils
from env import MONITOR_INTERFACE

ap_list = []
ap_dict = {}
client_dict = {}
cliente_usado = []
black_list = [None, "ff:ff:ff:ff:ff:ff"]
deauth_dict = {}
dissas_dict = {}

# Return reason code from Deauth frames

# Return Channel width
channel_width = {0: "20Mhz", 1: "20Mhz+40Mhz"}

# Return central channel given its frecuency
channel_frecuency = {
    2412: 1,
    2417: 2,
    2422: 3,
    2427: 4,
    2432: 5,
    2437: 6,
    2442: 7,
    2447: 8,
    2452: 9,
    2457: 10,
    2462: 11,
    2467: 12,
    2472: 13,
    2484: 14,
    5070: 12,
    5180: 36,
    5200: 40,
    5220: 44,
    5240: 48
}

# Return security suite
suite = {
    0x00: "Reserved",
    0x01: "802.1X",
    0x02: "PSK",
    0x03: "FT-802.1X",
    0x04: "FT-PSK",
    0x05: "WPA-SHA256",
    0x06: "PSK-SHA256",
    0x07: "TDLS",
    0x08: "SAE",
    0x09: "FT-SAE",
    0x0A: "AP-PEER-KEY",
    0x0B: "WPA-SHA256-SUITE-B",
    0x0C: "WPA-SHA384-SUITE-B",
    0x0D: "FT-802.1X-SHA384",
    0x0E: "FILS-SHA256",
    0x0F: "FILS-SHA384",
    0x10: "FT-FILS-SHA256",
    0x11: "FT-FILS-SHA384",
    0x12: "OWE"
}

# Return used cipher
cifrado = {
    0x00: "Use group cipher suite",
    0x01: "WEP-40",
    0x02: "TKIP",
    0x03: "OCB",
    0x04: "CCMP-128",
    0x05: "WEP-104",
    0x06: "BIP-CMAC-128",
    0x07: "Group addressed traffic not allowed",
    0x08: "GCMP-128",
    0x09: "GCMP-256",
    0x0A: "CCMP-256",
    0x0B: "BIP-GMAC-128",
    0x0C: "BIP-GMAC-256",
    0x0D: "BIP-CMAC-256"
}

# Return frame type
dot11_types = {
    0: "Management",
    1: "Control",
    2: "Data",
    3: "Reserved"
}

# return frame subtype
dot11_subtypes = {
    0: {  # Management
        0: "Association Request",
        1: "Association Response",
        2: "Reassociation Request",
        3: "Reassociation Response",
        4: "Probe Request",
        5: "Probe Response",
        6: "Timing Advertisement",
        8: "Beacon",
        9: "ATIM",
        10: "Disassociation",
        11: "Authentication",
        12: "Deauthentification",
        13: "Action",
        14: "Action No Ack",
    },
    1: {  # Control
        0: "Reserved",
        1: "Reserved",
        2: "Trigger",
        3: "TACK",
        4: "Beamforming Report Poll",
        5: "VHT NDP Announcement",
        6: "Control Frame Extension",
        7: "Control Wrapper",
        8: "Block Ack Request",
        9: "Block Ack",
        10: "PS-Poll",
        11: "RTS",
        12: "CTS",
        13: "Ack",
        14: "CF-End",
        15: "CF-End+CF-Ack",
    },
    2: {  # Data
        0: "Data",
        1: "Data+CF-Ack",
        2: "Data+CF-Poll",
        3: "Data+CF-Ack+CF-Poll",
        4: "Null (no data)",
        5: "CF-Ack (no data)",
        6: "CF-Poll (no data)",
        7: "CF-Ack+CF-Poll (no data)",
        8: "QoS Data",
        9: "QoS Data+CF-Ack",
        10: "QoS Data+CF-Poll",
        11: "QoS Data+CF-Ack+CF-Poll",
        12: "QoS Null (no data)",
        14: "QoS CF-Poll (no data)",
        15: "QoS CF-Ack+CF-Poll (no data)"
    },
    3: {  # Extension
        0: "DMG Beacon",
        1: "S1G Beacon"
    }
}


# Detect Beacon frames to detect AP and characteristics
def beacon_packet(time, packet):
    # Get SSID of AP
    raw_ssid = packet[Dot11Elt].info.decode('utf-8')
    ssid = raw_ssid.strip() if '\x00' not in raw_ssid and raw_ssid != '' else '[HIDDEN SSID]'

    # Get BSSID of AP
    bssid = packet[Dot11].addr3

    # Get RadioTap layer for further use
    radiotap = packet.getlayer(RadioTap)

    # Get RSSI of AP
    rssi = radiotap.dBm_AntSignal

    # Get Signal Quality of AP (not all Antennas are capable of get this variable)
    try:
        signal_quality = radiotap.Lock_Quality
        if signal_quality == "null":
            signal_quality = 0
    except:
        signal_quality = 0

    # Get Channel Flags for further use
    channelflags = str(radiotap.ChannelFlags)

    # Get Spectrum Frecuency of AP
    spectrum = channelflags.split('+')[1]
    if spectrum[0] == '2':
        spectrum = '2.4Ghz'

    # Get Frecuency of AP
    frecuency = radiotap.ChannelFrequency

    # Get Central Channel of AP based in its Frecuency
    try:
        central_channel = channel_frecuency[frecuency]
    except:
        central_channel = 0

    # Get Channel Bandwidth of AP
    try:
        channel_bandwidth = channel_width[packet[Dot11EltHTCapabilities].Supported_Channel_Width][:-3]
    except:
        channel_bandwidth = "0"

    # Get nstats for further use
    nstats = packet[Dot11Beacon].network_stats()

    # Return YES if the AP has any Security Method
    capability = packet.sprintf("{Dot11Beacon:%Dot11Beacon.cap%}\
                    {Dot11ProbeResp:%Dot11ProbeResp.cap%}")
    if re.search("privacy", capability):
        enc = 'YES'
    else:
        enc = 'NO'

    # Get Security type of AP
    cryp = nstats['crypto']
    crypto = []
    for element in cryp:
        var = element.split("/")[0]
        crypto.append(var)

    # Get Manufacturer of AP
    manufacturer = utils.manf2(bssid.upper()[:8])

    # Get Actual Channel of AP
    channel = 0
    try:
        channel = packet[Dot11EltDSSSet].channel
        # dsss = packet[Dot11EltDSSSet].id
    except:
        channel = central_channel

    # Get Supported and Extended Rates of AP
    rates = nstats['rates']
    newrates = []
    for rate in rates:
        newrates.append(str(rate))

    # Get FSPL = Distance between AP and Monitor
    distance = (27.55 - (20 * math.log10(frecuency)) + math.fabs(rssi)) / 20.0
    fspl = math.pow(10, distance)

    # Get Cipher Suite of AP
    try:
        suit = suite[packet[AKMSuite].suite]
    except:
        suit = "None"

    # Get Cipher Security of AP
    try:
        cipher = cifrado[packet[RSNCipherSuite].cipher]
    except:
        cipher = "None"

    timestamp = time

    # Make sure that AP is not already on list and update neccesary data if we already scanned it
    if bssid not in ap_list:  # HACER COMPROBACIÓN DE QUE TAMBIÉN TENGAN DISTINTO NOMBRE PQ PUEDEN TENER MISMA MAC Y UNA 5G Y OTRA 2G
        ap_list.append(bssid)

        lowest_fspl = fspl
        beacons = 1

        ap_dict[bssid] = {'bssid': bssid.upper(), 'ssid': ssid, 'channel': channel, 'rssi': rssi,
                          'signal_quality': signal_quality,
                          'spectrum': spectrum, 'manufacturer': manufacturer, 'enc': enc, 'crypto': crypto,
                          'frecuency': frecuency, 'rates': newrates, 'central_channel': central_channel,
                          'channel_bandwidth': channel_bandwidth, 'fspl': lowest_fspl, 'cipher': cipher, 'suite': suit,
                          'beacons': beacons, 'timestamp': timestamp, 'clients': []}

    # Update fspl if lower fspl found
    else:
        lowest_fspl = ap_dict[bssid]['fspl']
        if fspl < lowest_fspl:
            lowest_fspl = fspl

        beacons = ap_dict[bssid]['beacons'] + 1

        ap_dict[bssid] = {'bssid': bssid.upper(), 'ssid': ssid, 'channel': channel, 'rssi': rssi,
                          'signal_quality': signal_quality,
                          'spectrum': spectrum, 'manufacturer': manufacturer, 'enc': enc, 'crypto': crypto,
                          'frecuency': frecuency, 'rates': newrates, 'central_channel': central_channel,
                          'channel_bandwidth': channel_bandwidth, 'fspl': lowest_fspl, 'cipher': cipher, 'suite': suit,
                          'beacons': beacons, 'timestamp': timestamp, 'clients': []}


# Sniff Data & Control Frames to detect connected devices to AP
def datacontrol_packet(packet):
    if utils.noise_filter(packet.addr1, packet.addr2):
        return

    sn = packet.getlayer(Dot11).addr2
    rc = packet.getlayer(Dot11).addr1
    if sn not in black_list and rc not in black_list:
        if sn in ap_list:
            if rc not in cliente_usado:
                client_dict = {'mac': rc, 'connected_to': sn, 'manufacturer': utils.manf2(rc.upper()[:8])}
                ap_dict[sn]['clients'].append(client_dict)
                cliente_usado.append(rc)

        elif rc in ap_list:
            if sn not in cliente_usado:
                client_dict = {'mac': sn, 'connected_to': rc, 'manufacturer': utils.manf2(sn.upper()[:8])}
                ap_dict[rc]['clients'].append(client_dict)
                cliente_usado.append(sn)


# Detect Deauthentication frames
def deauth_packet(time, packet):
    ap = packet[Dot11].addr3
    victim = packet[Dot11].addr1
    reason = packet[Dot11Deauth].reason
    if ap not in deauth_dict:
        deauth_dict[ap] = {'first_seen': time, 'contador': 1, 'last_seen': time, 'victim': [], 'reason': [reason]}
    else:
        deauth_dict[ap]['contador'] += 1
        deauth_dict[ap]['last_seen'] = time
        if deauth_dict[ap]['reason'] != [reason]:
            deauth_dict[ap]['reason'].append(reason)


# Sniff the traffic and classify it
def sniffer(p):
    time = str(datetime.today().strftime("%Y-%m-%d %H:%M:%S"))

    if p.haslayer(Dot11):

        if p.haslayer(Dot11Deauth):

            deauth_packet(time, p)

        elif p.haslayer(Dot11Beacon):

            beacon_packet(time, p)

        elif p.getlayer(Dot11).type in [1, 2]:
            datacontrol_packet(p)


# Classify deauth packets
def deauth_packets(ap):
    if ap in deauth_dict:
        return deauth_dict[ap]
    else:
        return 1


# Changes channel randomly in range(1,15)
def channel_hopper():
    list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 36, 40, 44, 48]
    # Definimos la interfaz
    interface = MONITOR_INTERFACE
    while True:
        try:
            # channel = random.randrange(1, 15)
            channel = random.choice(list)
            os.system("iwconfig %s channel %d" % (interface, channel))
            time.sleep(1)
        except KeyboardInterrupt:
            break
            # Capture interrupt signal and cleanup before exiting


# Function to sniff the packages
def start_sniffing(interface):
    # Restarting Card because it's bugged
    utils.restart_interface()

    # Creating a multi process to perform channel hoping
    p = Process(target=channel_hopper)
    p.start()

    # Start Sniffing
    sniff(iface=interface, prn=sniffer, count=25)

    p.terminate()
    p.join()

    return ap_dict
