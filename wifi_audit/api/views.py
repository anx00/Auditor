from rest_framework import generics
from rest_framework import mixins

from analizador_wifi.models import dispositivos
from modo_monitor.models import access_point, device
from .serializers import APSerializer, DeviceSerializer, ClientsSerializer


# Create your views here.

class APIApView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = APSerializer
    queryset = access_point.objects.all().order_by('id')

    def get(self, request):
        return self.list(request)

class APDeviceView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = DeviceSerializer
    queryset = dispositivos.objects.all().order_by('id')

    def get(self, request):
        return self.list(request)


class APClientsView(generics.GenericAPIView, mixins.ListModelMixin):
    serializer_class = ClientsSerializer
    queryset = device.objects.all().order_by('id')

    def get(self, request):
        return self.list(request)
