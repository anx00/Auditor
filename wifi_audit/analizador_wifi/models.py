from django.db import models

# Create your models here.

class dispositivos(models.Model):

    id = models.BigAutoField(primary_key=True)
    ip = models.CharField(max_length=20)
    mac = models.CharField(max_length=20)
    vendor = models.CharField(max_length=50)
    os = models.CharField(max_length=100)
    osfamily = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    nombre_dispositivo = models.CharField(max_length=40)
    last_seen = models.CharField(max_length=40) #Cambiar estos dos a datetimefield
    connected_to = models.CharField(max_length=40)

    class Meta:
        verbose_name = 'Dispositivo'

    def __str__(self):
        return self.ip