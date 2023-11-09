from rest_framework import serializers
from .models import Kulutus

class KulutusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kulutus
        fields = ['id','nimi', 'hinta', 'lasku_päivämäärä']