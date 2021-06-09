from django.db import models

# Create your models here.

class dispositivos(models.Model):

    id = models.BigAutoField(primary_key=True)
    ip = models.CharField(max_length=20)
    mac = models.CharField(max_length=20)
    manufacturer = models.CharField(max_length=50)
    os_system = models.CharField(max_length=100)
    os_family = models.CharField(max_length=50)
    device_type = models.CharField(max_length=50)
    hostname = models.CharField(max_length=40)
    timestamp = models.CharField(max_length=40)
    connected_to = models.CharField(max_length=40)
    device_id = models.CharField(max_length=30)

    class Meta:
        verbose_name = 'Dispositivo'

    def __str__(self):
        return self.ip