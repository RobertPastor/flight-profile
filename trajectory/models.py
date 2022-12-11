import os
import logging
from django.db import models


BADA_381_DATA_FILES = 'Bada381DataFiles'
OPFfileExtension = '.OPF'
# Create your models here.

class BadaSynonymAircraft(models.Model):
    
    AircraftICAOcode = models.CharField(max_length = 100, primary_key = True)
    Manufacturer = models.CharField(max_length = 100)
    AircraftModel = models.CharField(max_length = 100)
    AircraftFile = models.CharField(max_length = 100)
    useSynonym = models.BooleanField(default = False)
    
    def __str__(self):
        return "{0}-{1}-{2}".format(self.AircraftICAOcode, self.Manufacturer, self.AircraftModel)
    
    def getAircraftPerformanceFile(self):
        OPFfilePrefix = self.AircraftFile    
        filePath = os.path.join ( os.path.dirname(__file__) , BADA_381_DATA_FILES , OPFfilePrefix + OPFfileExtension )
        logging.info ( filePath )
        return filePath
        
    def aircraftPerformanceFileExists(self):
        filePath = self.getAircraftPerformanceFile()
        return os.path.exists(filePath) and os.path.isfile(filePath)
    
    def getICAOcode(self):
        return self.AircraftICAOcode
    
    def getAircraftFullName(self):
        return self.AircraftModel
    
    def getAircraftOPFfilePrefix(self):
        return self.AircraftFile


class AirlineWayPoint(models.Model):
    WayPointName = models.CharField(max_length = 100, primary_key = True)
    Type = models.CharField(max_length = 100)
    Continent = models.CharField(max_length = 100)
    Latitude = models.FloatField(blank = False)
    Longitude = models.FloatField(blank = False)
    
    '''
    def getDistanceMetersTo(self, nextWayPoint):
        if isinstance(nextWayPoint, WayPoint)==True:
            return points2distanceMeters([self.LatitudeDegrees,self.LongitudeDegrees],
                                         [nextWayPoint.LatitudeDegrees, nextWayPoint.LongitudeDegrees])
        return 0.0
    '''
    
    def __str(self):
        print ( self.WayPointName , str(self.Latitude) , str(self.Longitude) )


''' an airport is not related to an airline '''
class AirlineAirport(models.Model):
    AirportICAOcode = models.CharField(max_length = 100, primary_key = True)
    AirportName = models.CharField(max_length = 100, unique = True)
    Latitude = models.FloatField()
    Longitude = models.FloatField()
    FieldElevationAboveSeaLevelMeters = models.FloatField(blank = False)
    Continent = models.CharField(max_length = 100)
    
    def __str__(self):
        return "{0}-{1}".format(self.AirportICAOcode, self.AirportName)
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
class AirlineRunWay(models.Model):
    ''' example : 08R/26L and 09L/27R '''
    Name = models.CharField(max_length = 10)
    ''' foreign key on the related airport '''
    Airport = models.ForeignKey(AirlineAirport, on_delete=models.CASCADE)
    LengthFeet = models.FloatField(blank = False)
    TrueHeadingDegrees = models.FloatField(blank = False)
    LatitudeDegrees = models.FloatField(blank = False)
    LongitudeDegrees = models.FloatField(blank = False)
    
    def __str__(self):
        return "{0}/{1}".format(self.Airport.AirportICAOcode, self.Name)
    
    

    