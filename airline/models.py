from django.db import models
import logging
# Create your models here.
from trajectory.models import AirlineAirport, AirlineRunWay

class Airline(models.Model):
    Name = models.CharField( max_length = 250 , unique=True)
    MinLongitudeDegrees = models.FloatField()
    MinLatitudeDegrees  = models.FloatField()
    MaxLongitudeDegrees = models.FloatField()
    MaxLatitudeDegrees  = models.FloatField()

    def __str__(self):
        return "{0}".format(self.Name)


def get_default_airline():
    return Airline.objects.get_or_create(Name="AmericanWings")[0]



class AirlineRoute(models.Model):
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE , default=None )

    DepartureAirport = models.CharField(max_length = 500)
    DepartureAirportICAOCode = models.CharField(max_length = 50)
    ArrivalAirport = models.CharField(max_length = 500)
    ArrivalAirportICAOCode = models.CharField(max_length = 50)
    
    class Meta:
        unique_together = (('DepartureAirportICAOCode', 'ArrivalAirportICAOCode'),)

    def getDepartureAirportICAOcode(self):
        return self.DepartureAirportICAOCode
    
    def getArrivalAirportICAOcode(self):
        return self.ArrivalAirportICAOCode
    
    def getFlightLegAsString (self):
        return self.DepartureAirportICAOCode + "-" + self.ArrivalAirportICAOCode
    
    def __str__(self):
        return "departure airport= {0} - arrival airport= {1}".format(self.DepartureAirportICAOCode, self.ArrivalAirportICAOCode)

    def getAirportsList(self):
        airlineRoutes = AirlineRoute.objects.all()
        airportsICAOcodeList = []
        for airlineRoute in airlineRoutes:
            adep = airlineRoute.DepartureAirportICAOCode
            if ( adep in airportsICAOcodeList ) == False :
                logging.info ( adep )
                airportsICAOcodeList.append(adep)
            ades = airlineRoute.ArrivalAirportICAOCode
            if ( ades in airportsICAOcodeList ) == False :
                logging.info ( ades )
                airportsICAOcodeList.append(ades)
            
        return airportsICAOcodeList
    
    
    def getRouteAsString(self, AdepRunWayName = None, AdesRunWayName = None):
        strRoute = "ADEP/" + self.DepartureAirportICAOCode 
        Adep = AirlineAirport.objects.all().filter(AirportICAOcode=self.DepartureAirportICAOCode).first()
        if ( Adep ):
            if (AdepRunWayName):
                strRoute += "/" + AdepRunWayName
            else:
                AdepRunway = AirlineRunWay.objects.all().filter(Airport=Adep).first()
                if AdepRunway  and ( len ( AdepRunway.Name ) > 0):
                    strRoute += "/" + AdepRunway.Name
            
        strRoute += "-"
        airlineRouteWayPoints = AirlineRouteWayPoints.objects.all().filter(Route=self).distinct("Order").order_by("Order")
        for airlineRouteWayPoint in airlineRouteWayPoints:
            strRoute += airlineRouteWayPoint.WayPoint
            strRoute += "-"
        
        strRoute += "ADES/" + self.ArrivalAirportICAOCode
        Ades = AirlineAirport.objects.all().filter(AirportICAOcode=self.ArrivalAirportICAOCode).first()
        if ( Ades ):
            if (AdesRunWayName):
                strRoute += "/" + AdesRunWayName
            else:
                AdesRunWay = AirlineRunWay.objects.all().filter(Airport=Ades).first()
                if AdesRunWay and ( len (AdesRunWay.Name ) > 0):
                    strRoute += "/" + AdesRunWay.Name 
            
        logging.info ( strRoute )
        return strRoute
  
  
class AirlineRouteWayPoints(models.Model):
    #Airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    Route = models.ForeignKey(AirlineRoute, on_delete=models.CASCADE)
    Order = models.IntegerField()
    # linked to the WayPoint class in the trajectory
    WayPoint = models.CharField(max_length = 100)
            
    def getWayPointsListAsString(self):
        routeAsString = ""
        first = True
        for wayPoint in AirlineRouteWayPoints.objects.all().filter(Route=self).order_by("Order"):
            if (first):
                routeAsString += str(wayPoint.WayPoint).strip()
                first = False
            else:
                routeAsString += "-" + str(wayPoint.WayPoint).strip()
        logging.info ( routeAsString )
        return routeAsString
        


class AirlineAircraft(models.Model):
    aircraftICAOcode = models.CharField(max_length = 50)
    aircraftFullName = models.CharField(max_length = 500)
    numberOfAircraftsInService = models.IntegerField(default = 0)
    maximumOfPassengers = models.IntegerField(default = 0)
    costsFlyingPerHoursDollars = models.FloatField(default = 0)
    crewCostsPerFlyingHoursDollars = models.FloatField(default = 0)
    
    landingLengthMeters = models.FloatField(default = 0)
    takeOffMTOWLengthMeters = models.FloatField(default = 0)
    
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE  )

        
    def __str__(self):
        return "{0}-{1}".format(self.aircraftFullName, self.aircraftICAOcode)
        
    def hasICAOcode(self):
        return ( len ( self.aircraftICAOcode ) > 0 )
        
    def getAircraftFullName(self):
        return self.aircraftFullName
    
    def getNumberOfAircraftInstances(self):
        return self.numberOfAircraftsInService
    
    def getMaximumNumberOfPassengers(self):
        return self.maximumOfPassengers
    
    def getCostsFlyingPerHoursDollars(self):
        return self.costsFlyingPerHoursDollars
    
    def getCrewCostsPerFlyingHoursDollars(self):
        return self.crewCostsPerFlyingHoursDollars
    
    ''' added as an extension from other databases '''
    def setAircraftICAOcode(self, acICAOcode):
        self.aircraftICAOcode = acICAOcode
    
    def getAircraftICAOcode(self):
        return self.aircraftICAOcode
    
    def setLandingLengthMeters(self, lengthMeters):
        self.landingLengthMeters = lengthMeters
    
    def setTakeOffMTOWLengthMeters(self, lenghtMeters):
        self.takeOffMTOWLengthMeters = lenghtMeters
    
    def getLandingLengthMeters(self):
        return self.landingLengthMeters
    
    def getTakeOffMTOWLengthMeters(self):
        return self.takeOffMTOWLengthMeters
    

