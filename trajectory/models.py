import os
import logging
from django.db import models

from trajectory.Environment.RunWayFile import RunWay
from trajectory.Guidance.WayPointFile import Airport

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
    
    def __str__(self):
        return "wayPoint name = {0} - Latitude {1:.2f} - Longitude = {2:.2f}".format(self.WayPointName , self.Latitude , self.Longitude ) 

    def getWayPointName(self):
        return self.WayPointName
    

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
    
    def getICAOcode(self):
        return self.AirportICAOcode
    
    def getLatitudeDegrees(self):
        return self.Latitude
    
    def getLongitudeDegrees(self):
        return self.Longitude
    
    def convertToEnvAirport(self):
        return Airport ( Name = self.AirportName, 
                         LatitudeDegrees = self.Latitude , 
                         LongitudeDegrees = self.Longitude ,
                         fieldElevationAboveSeaLevelMeters = self.FieldElevationAboveSeaLevelMeters, 
                         isDeparture = True, 
                         isArrival = False,
                         ICAOcode = self.AirportICAOcode,
                         Country = 'unknown')
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
    ''' warning the runway name is not unique as the same name can be used in different airports '''
    ''' however for one airport , the runway names are unique '''
    Name = models.CharField(max_length = 10)
    ''' foreign key on the related airport '''
    Airport = models.ForeignKey(AirlineAirport, on_delete=models.CASCADE)
    LengthFeet = models.FloatField(blank = False)
    TrueHeadingDegrees = models.FloatField(blank = False)
    LatitudeDegrees = models.FloatField(blank = False)
    LongitudeDegrees = models.FloatField(blank = False)
    
    def __str__(self):
        return "{0}/{1}".format(self.Airport.AirportICAOcode, self.Name)
    
    def getLatitudeDegrees(self):
        return self.LatitudeDegrees
    
    def getLongitudeDegrees(self):
        return self.LongitudeDegrees
    
    def convertToEnvRunway(self):
        return RunWay(Name = self.Name, 
                airportICAOcode = self.Airport.getICAOcode(), 
                LengthFeet      = self.LengthFeet, 
                TrueHeadingDegrees = self.TrueHeadingDegrees, 
                LatitudeDegrees    = self.LatitudeDegrees, 
                LongitudeDegrees   = self.LongitudeDegrees)
    
    
class AirlineStandardDepartureArrivalRoute(models.Model):
    ''' 3rd June 2023 '''
    isSID                      = models.BooleanField(default=True)
    DepartureArrivalAirport    = models.ForeignKey(AirlineAirport, on_delete=models.CASCADE)
    DepartureArrivalRunWay     = models.ForeignKey(AirlineRunWay, on_delete=models.CASCADE)
    FirstLastRouteWayPoint     = models.ForeignKey(AirlineWayPoint, on_delete=models.CASCADE)
    
    
    def getWayPointsListAsString(self , isSID):
        assert ( isinstance ( isSID, bool ))
        routeAsString = ""
        first = True
        sidStarWayPointsRoute = AirlineSidStarWayPointsRoute.objects.filter( Route = self ).order_by("Order")
        for wayPoint in sidStarWayPointsRoute:
            if (first):
                if ( isSID ):
                    if ( ( ("/") in str(wayPoint.WayPointName) ) == False ):
                        routeAsString += str(wayPoint.WayPointName).strip()
                    first = False
                else:
                    if ( ( ("/") in str(wayPoint.WayPointName) ) == False ):
                        routeAsString += str(wayPoint.WayPointName).strip()
                    first = False
            else:
                if ( isSID ):
                    routeAsString += "-" + str(wayPoint.WayPointName).strip()
                else:
                    if ( ( ("/") in str(wayPoint.WayPointName) ) == False ):
                        routeAsString += "-" + str(wayPoint.WayPointName).strip()
        
        logging.info ( routeAsString )
        print ( routeAsString )
        return routeAsString

    
class AirlineSidStarWayPointsRoute(models.Model):
    ''' 3rd June 2023 '''
    Route = models.ForeignKey(AirlineStandardDepartureArrivalRoute, on_delete=models.CASCADE)
    ''' warning - in the SID order = 0 is the departure runway '''
    Order = models.IntegerField()
    # linked to the WayPoint class in the trajectory
    WayPointName     = models.CharField(max_length = 100, blank = False)
    LatitudeDegrees  = models.FloatField(blank = False)
    LongitudeDegrees = models.FloatField(blank = False)
    
    def getWayPointsListAsString(self):
        routeAsString = ""
        first = True
        for wayPoint in AirlineSidStarWayPointsRoute.objects.filter(Route=self).order_by("Order"):
            if (first):
                routeAsString += str(wayPoint.WayPoint).strip()
                first = False
            else:
                routeAsString += "-" + str(wayPoint.WayPoint).strip()
        logging.info ( routeAsString )
        return routeAsString
    
    
    