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
    
    
'''
    The Charles De Gaulle airport has 2 configurations, depending on the wind directions.
    However, in both configurations Eastward and Westward of Charles de Gaulle:
    - The Run-ways 08R/26L and 09L/27R (far from the terminal) are mainly used for landings.
    - The Run-ways 08L/26R and 09R/27L (near the terminal) are mainly used for take-offs. 
    
    Id, ICAO,Number, Length Meters, Length Feet, Orientation Degrees
    The run-way true heading is defined as the angle 
      1) expressed in degrees
      2) counted from the geographic NORTH, 
      3) clock-wise 
      4) with the run-way end point as the summit of the angle

    Lat-long are the position of the end of the runway
    1) end - if takeoff runway -  is the location the aircraft starts its ground run
    2) end - if landing runway - is the location where after the touch down and deceleration, the ac reaches the taxi speed
     
'''
class RunWay(models.Model):
    ''' example : 08R/26L and 09L/27R '''
    Name = models.CharField(max_length = 10)
    ''' foreign key on the related airport '''
    Airport = models.ForeignKey(Airport, on_delete=models.CASCADE)
    LengthFeet = models.FloatField(blank = False)
    TrueHeadingDegrees = models.FloatField(blank = False)
    LatitudeDegrees = models.FloatField(blank = False)
    LongitudeDegrees = models.FloatField(blank = False)
    