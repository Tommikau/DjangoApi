from django.db import models

# Create your models here.

class Kulutus(models.Model):
    nimi = models.CharField(max_length=100, default='')
    hinta = models.DecimalField(max_digits=10, decimal_places=2)
    lasku_päivämäärä = models.DateField()

  
    
    
        