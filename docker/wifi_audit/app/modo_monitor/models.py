from django.db import models

# Create your models here.

class access_point(models.Model):

    id = models.BigAutoField(primary_key=True)
    ssid = models.CharField(max_length=40)
    bssid = models.CharField(max_length=40)
    channel = models.IntegerField()
    rssi = models.IntegerField()
    signal_quality = models.IntegerField()
    frecuency = models.IntegerField()
    central_channel = models.IntegerField()
    spectrum = models.CharField(max_length=20)
    distance_ap = models.IntegerField()
    channel_bandwidth = models.CharField(max_length=30)
    beacons = models.IntegerField()
    security_protocol = models.CharField(max_length=40)
    auth_crypto = models.CharField(max_length=30)
    cipher_algorithm = models.CharField(max_length=30)
    rates = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=50)
    deauth_frames = models.IntegerField()
    deauth_first_seen = models.CharField(max_length=50)
    deauth_last_seen = models.CharField(max_length=50)
    device_id = models.CharField(max_length=30)
    timestamp = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Access Point'

    def __str__(self):
        return self.ssid


class device(models.Model):

    id = models.BigAutoField(primary_key=True)
    mac = models.CharField(max_length=40)
    connected_to = models.CharField(max_length=40)
    manufacturer = models.CharField(max_length=50)
    device_id = models.CharField(max_length=30)
    ap_id = models.ForeignKey(access_point, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Device'

    def __str__(self):
        return self.mac
