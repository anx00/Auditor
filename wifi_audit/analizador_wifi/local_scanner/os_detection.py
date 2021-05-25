import nmap3


def os_detection(target):

    nm = nmap3.Nmap()
    os_results = nm.nmap_os_detection(target)
    os_scan = {}
    for key in os_results:
        if 'osmatch' in os_results[key]:
            os_name = os_results[key]['osmatch'][0]['name']
            os_type = os_results[key]['osmatch'][0]['osclass']['type']
            os_vendor = os_results[key]['osmatch'][0]['osclass']['vendor']
            os_scan = {"name": os_name, "type": os_type, "vendor": os_vendor}

    print(os_scan)


os_detection("192.168.1.67")