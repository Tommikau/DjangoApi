from rest_framework import viewsets
from .models import Kulutus
from .serialaizers import KulutusSerializer
# Create your views here.

class KulutusViewSets(viewsets.ModelViewSet):
    serializer_class = KulutusSerializer
    def get_queryset(self):
        queryset = Kulutus.objects.all()
        nimi = self.request.query_params.get("nimi")
        if nimi is not None:
            queryset = queryset.filter(nimi=nimi)
        return queryset