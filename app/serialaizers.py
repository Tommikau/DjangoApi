from rest_framework import serializers
from .models import Kulutus
from django.contrib.auth.models import User

from rest_framework import serializers
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User 
        fields = ['id', 'username', 'password', 'email']
            
class KulutusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kulutus
        fields = ['id', 'user', 'nimi', 'hinta', 'lasku_päivämäärä']
        
    def to_representation(self, instance):
        if instance is not None:
            request = self.context.get('request')
            if request and request.user.is_authenticated:
                user = request.user
                if instance.user == user:
                    return super().to_representation(instance)
                else:
                    return None
        return super().to_representation(instance)