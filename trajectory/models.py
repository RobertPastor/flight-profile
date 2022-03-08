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
    Continent = models.CharField(max_length = 100)
    Latitude = models.FloatField(blank = False)
    Longitude = models.FloatField(blank = False)

class Airport(models.Model):
    AirportICAOcode = models.CharField(max_length = 100, primary_key = True)
    AirportName = models.CharField(max_length = 100, unique = True)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    FieldElevationAboveSeaLevelMeters = models.FloatField(blank = False)
    Continent = models.CharField(max_length = 100)
    
