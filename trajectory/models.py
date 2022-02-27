from django.db import models
from django.template.defaultfilters import default

# Create your models here.

class Aircrafts(models.Model):
    AircraftICAOcode = models.CharField(max_length=100, primary_key = True)
    Manufacturer = models.CharField(max_length=100)
    AircraftModel = models.CharField(max_length=100)
    AircraftFile = models.CharField(max_length=100)
    useSynonym = models.BooleanField(default = False)