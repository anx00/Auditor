
from __future__ import absolute_import, unicode_literals

from celery import shared_task

from modo_monitor.network_scanner.scan_ap import scanner


@shared_task
def prueba_suma(interfaz, mac, timeout, time):
        data = scanner(interfaz, mac, timeout)
        return data
