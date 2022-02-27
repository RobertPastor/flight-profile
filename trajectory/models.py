from django.db import models

# Create your models here.

class Aircraft(models.Model):
    AircraftICAOcode = models.CharField(max_length = 100, primary_key = True)
    Manufacturer = models.CharField(max_length = 100)
    AircraftModel = models.CharField(max_length = 100)
    AircraftFile = models.CharField(max_length = 100)
    useSynonym = models.BooleanField(default = False)
    
class WayPoint(models.Model):
    WayPointName = models.CharField(max_length = 100, primary_key = True)
    Type = models.CharField(max_length = 100)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
