from django.db import models

# Create your models here.

class access_point(models.Model):
    essid = models.CharField(max_length=40)
    bssid = models.CharField(max_length=40)
    encriptacion = models.CharField(max_length=40)
    spectrum = models.CharField(max_length=20)
    rates = models.CharField(max_length=100)
    manufacturer = models.CharField(max_length=50)
    channel_bandwidth = models.CharField(max_length=30)
    cipher = models.CharField(max_length=30)
    suite = models.CharField(max_length=30)
    deauth_last_seen = models.CharField(max_length=50)
    deauth_first_seen = models.CharField(max_length=50)


    signal_quality = models.IntegerField()
    central_channel = models.IntegerField()
    fspl = models.IntegerField()
    rssi = models.IntegerField()
    canal = models.IntegerField()
    frecuencia = models.IntegerField()
    beacons = models.IntegerField()
    deauth_frames = models.IntegerField()

    class Meta:
        verbose_name = 'Access Point'

    def __str__(self):
        return self.essid


class device(models.Model):

    connected_to = models.CharField(max_length=40)
    mac_device = models.CharField(max_length=40)
    manufacturer = models.CharField(max_length=50)

    ap = models.ForeignKey(access_point, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Device'

    def __str__(self):
        return self.mac_device
