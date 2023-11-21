from django.db import models
from django.contrib.auth.models import User



# Create your models here.

class Kulutus(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    nimi = models.CharField(max_length=100, default='')
    hinta = models.DecimalField(max_digits=10, decimal_places=2)
    lasku_päivämäärä = models.DateField()
    
    def __str__(self):
        return self.nimi

  
    
    
        #)",
        #"created_at": "2021-11-20T13:34:21.837Z",
        #"updated_at": "2021-11-20T13:34:21.837Z",
        #"id": "1"

  
    
    
        