from django.db import models 
from django.utils import timezone
import random 

# Create your models here.
"""
Status : 
0 : enregistré
1 : envoyé
2 : livré
"""
class Parcel(models.Model):   
    tracking_number = models.CharField(max_length=11, unique=True) # FR3563HD
    adress_dep = models.CharField(max_length=100)
    adress_arr = models.CharField(max_length=100)
    weight = models.IntegerField()
    status = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.tracking_number:
            self.tracking_number = 'FR' + str(random.randint(111, 999))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Colis N°{self.id} - {self.weight}kg - {self.tracking_number}"