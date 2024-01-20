from django.db import models

# Create your models here.
from trajectory.models import AirlineAirport, AirlineRunWay, AirlineStandardDepartureArrivalRoute

from trajectory.Environment.RunWayFile import RunWay
from trajectory.Environment.Constants import NauticalMiles2Meter , Meter2NauticalMiles, ConstantClimbRampLengthNauticalMiles

from trajectory.Guidance.GeographicalPointFile import GeographicalPoint
from trajectory.Environment.Earth import EarthRadiusMeters
from trajectory.models import AirlineWayPoint

class Airline(models.Model):
    Name = models.CharField( max_length = 250 , unique=True)
    MinLongitudeDegrees = models.FloatField()
    MinLatitudeDegrees  = models.FloatField()
    MaxLongitudeDegrees = models.FloatField()
    MaxLatitudeDegrees  = models.FloatField()

    def __str__(self):
        return "{0}".format(self.Name)
    
    ''' used to compare objects '''
    def __eq__(self, other):
        return models.Model.__eq__(self, other)
    
    ''' 14 Juin 2023 '''
    ''' since Django 2.2 if eq is implemented, need to implement hash otherwise we get a type error object is unhashable '''
    def __hash__(self):
        return super().__hash__()

def get_default_airline():
    return Airline.objects.get_or_create(Name="AmericanWings")[0]


class AirlineRoute(models.Model):
    
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE , default=None )

    DepartureAirport         = models.CharField(max_length = 500)
    DepartureAirportICAOCode = models.CharField(max_length = 50)
    ArrivalAirport           = models.CharField(max_length = 500)
    ArrivalAirportICAOCode   = models.CharField(max_length = 50)
    
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

    ''' used to compare objects '''
    def __eq__(self, other):
        return models.Model.__eq__(self, other)
    
    ''' 14 Juin 2023 '''
    ''' since Django 2.2 if eq is implemented, need to implement hash otherwise we get a type error object is unhashable '''
    def __hash__(self):
        return super().__hash__()
    
    def getAirportsList(self):
        airlineRoutes = AirlineRoute.objects.all()
        airportsICAOcodeList = []
        for airlineRoute in airlineRoutes:
            adep = airlineRoute.DepartureAirportICAOCode
            if ( adep in airportsICAOcodeList ) == False :
                airportsICAOcodeList.append(adep)
            ades = airlineRoute.ArrivalAirportICAOCode
            if ( ades in airportsICAOcodeList ) == False :
                airportsICAOcodeList.append(ades)
            
        return airportsICAOcodeList
    
    def extendRouteWithSID (self , Adep , AdepRunWayName , firstWayPointInRoute ):
        
        assert ( isinstance ( Adep , AirlineAirport ))
        assert ( isinstance ( firstWayPointInRoute , AirlineWayPoint ))

        AdepRunWay = AirlineRunWay.objects.filter  ( Name = AdepRunWayName , Airport = Adep ).first()
        if AdepRunWay:
            ''' searching for a SID '''
            isSID = True
            sidStar = AirlineStandardDepartureArrivalRoute.objects.filter ( isSID = isSID , 
                                                                            DepartureArrivalAirport = Adep,
                                                                            DepartureArrivalRunWay  = AdepRunWay ,
                                                                            FirstLastRouteWayPoint = firstWayPointInRoute).first()
            if sidStar:
                return sidStar.getWayPointsListAsString(isSID)
            
        return ""
    
    def extendRouteWithSTAR(self , Ades , AdesRunWayName , lastWayPointInRoute):
        
        assert ( isinstance ( Ades , AirlineAirport ))
        assert ( isinstance ( lastWayPointInRoute , AirlineWayPoint ))
        
        AdesRunWay = AirlineRunWay.objects.filter  ( Name = AdesRunWayName , Airport = Ades ).first()
        if AdesRunWay:
            ''' searching for a STAR '''
            isSID = False
            sidStar = AirlineStandardDepartureArrivalRoute.objects.filter ( isSID = isSID , 
                                                                            DepartureArrivalAirport = Ades,
                                                                            DepartureArrivalRunWay  = AdesRunWay ,
                                                                            FirstLastRouteWayPoint = lastWayPointInRoute).first()
            if sidStar:
                return sidStar.getWayPointsListAsString(isSID)
        
        return ""
    
    def getfirstRouteWayPoint(self):
        airlineRouteWayPoint = AirlineRouteWayPoints.objects.filter(Route=self).distinct().order_by("Order").first()
        if ( airlineRouteWayPoint ):
            airlineWayPoint = AirlineWayPoint.objects.filter ( WayPointName = airlineRouteWayPoint.getWayPointName() ).first()
            if ( airlineWayPoint ):
                return airlineWayPoint
        else:
            raise ValueError("first way point in Route not found ")
        return None
    
    def getLastRouteWayPoint(self):
        airlineRouteWayPoint = AirlineRouteWayPoints.objects.filter(Route=self).distinct().order_by("Order").last()
        if ( airlineRouteWayPoint ):
            airlineWayPoint = AirlineWayPoint.objects.filter ( WayPointName = airlineRouteWayPoint.getWayPointName() ).first()
            if ( airlineWayPoint ):
                return airlineWayPoint
        else:
            raise ValueError("first way point in Route not found ")
        return None
    
    def getAdepRouteAsString(self, AdepRunWayName = None):
        strRoute = "ADEP/" + self.DepartureAirportICAOCode 
        Adep = AirlineAirport.objects.filter(AirportICAOcode=self.DepartureAirportICAOCode).first()
        if ( Adep ):
            if (AdepRunWayName):
                strRoute += "/" + AdepRunWayName
                ''' 3th June 2023 - extend with SID when available '''
                strRoute += self.extendRouteWithSID( Adep , AdepRunWayName , self.getfirstRouteWayPoint() )
            else:
                #print ( "Best Departure Runway = {0}".format(self.computeBestDepartureRunWay()))
                AdepRunway = AirlineRunWay.objects.filter(Airport=Adep).first()
                if AdepRunway  and ( len ( AdepRunway.Name ) > 0):
                    strRoute += "/" + AdepRunway.Name
        return strRoute
    
    def getAdesRouteAsString(self, AdesRunWayName = None ):
        strRoute = ""
        Ades = AirlineAirport.objects.filter(AirportICAOcode=self.ArrivalAirportICAOCode).first()
        if ( Ades ):
            if (AdesRunWayName):
                ''' 6th June 2023 - extend with STAR when available '''
                strRoute += self.extendRouteWithSTAR(Ades, AdesRunWayName, self.getLastRouteWayPoint() )
                #print ( strRoute )
                strRoute += "-"
                strRoute += "ADES/" + self.ArrivalAirportICAOCode
                strRoute += "/" + AdesRunWayName
            else:
                AdesRunWay = AirlineRunWay.objects.filter(Airport=Ades).first()
                if AdesRunWay and ( len (AdesRunWay.Name ) > 0):
                    strRoute += "/" + AdesRunWay.Name 
        return strRoute
    
    def getWayPointsRouteAsString(self):
        strRoute = ""
        ''' 8th January 2023 - MySQL does not allow DISTINCT with field name '''
        airlineRouteWayPoints = AirlineRouteWayPoints.objects.filter(Route=self).distinct().order_by("Order")
        ''' 8th January 2023 - work around as DISTINCT with Order not allowed in MySQL - need to use an intermediate list '''
        wayPointsList = []
        for airlineRouteWayPoint in airlineRouteWayPoints:
            ''' avoid duplicates '''
            if airlineRouteWayPoint.WayPoint not in wayPointsList:
                wayPointsList.append(airlineRouteWayPoint.WayPoint)
                strRoute += airlineRouteWayPoint.WayPoint
                strRoute += "-"
        return strRoute
    
    def getDirectRouteAsString(self, AdepRunWayName = None, AdesRunWayName = None):
        strRoute = self.getAdepRouteAsString(AdepRunWayName = AdepRunWayName)
        strRoute += "-"
        strRoute += self.getfirstRouteWayPoint().getWayPointName()
        strRoute += "-"
        strRoute += self.getLastRouteWayPoint().getWayPointName()
        strRoute += "-"
        strRoute += self.getAdesRouteAsString(AdesRunWayName = AdesRunWayName)
        strRoute = str(strRoute).replace("--", "-")    
        return strRoute
    
    def getRouteAsString(self, AdepRunWayName = None, AdesRunWayName = None):
        strRoute = self.getAdepRouteAsString(AdepRunWayName = AdepRunWayName)
            
        strRoute += "-"
        strRoute += self.getWayPointsRouteAsString()
        
        strRoute += "-"
        strRoute += self.getAdesRouteAsString(AdesRunWayName = AdesRunWayName)
            
        # clean after duplicates suppression
        strRoute = str(strRoute).replace("--", "-")        
        return strRoute
  
    ''' best departure run-way is the one with minimal distance between end of 5 nautical climb ramp and first point of the route '''
    def computeBestDepartureRunWay(self):
        
        firstRouteWayPoint = AirlineRouteWayPoints.objects.all().filter(Route=self).distinct().order_by("Order").first()
        if ( firstRouteWayPoint ):
            wayPoint = AirlineWayPoint.objects.all().filter( WayPointName = firstRouteWayPoint.WayPoint ).first()
            if (wayPoint):
                firstRouteWayPoint = GeographicalPoint(wayPoint.Latitude , wayPoint.Longitude , EarthRadiusMeters)
                
                Adep = self.DepartureAirportICAOCode
                minimalDistanceMeters = 0.0
                bestRunWay = None
                first = True
                for rwy in AirlineRunWay.objects.all().filter(Airport=Adep):
                    runWay = RunWay(Name               = rwy.Name ,
                                    airportICAOcode    = Adep,
                                    LengthFeet         = rwy.LengthFeet,
                                    TrueHeadingDegrees = rwy.TrueHeadingDegrees,
                                    LatitudeDegrees    = rwy.LatitudeDegrees,
                                    LongitudeDegrees   = rwy.LongitudeDegrees)
                    rwyEnd = runWay.getEndOfRunWay()
                    ''' 5 Nm after end of run-way '''
                    latitudeDegrees , longitudeDegrees = rwyEnd.getGeoPointAtDistanceHeading( ConstantClimbRampLengthNauticalMiles * NauticalMiles2Meter, runWay.getTrueHeadingDegrees())
                    pathEnd = GeographicalPoint(latitudeDegrees , longitudeDegrees, EarthRadiusMeters)
        
                    distanceMeters = pathEnd.computeDistanceMetersTo(firstRouteWayPoint)
                    if first:
                        first = False
                        bestRunWay = rwy
                        minimalDistanceMeters = distanceMeters
                    else:
                        if ( distanceMeters < minimalDistanceMeters ):
                            bestRunWay = rwy
                            minimalDistanceMeters = distanceMeters
                        
                return bestRunWay.Name if (bestRunWay) else ""
            else:
                return "Error - computeBestDepartureRunWay"
        else:
            return "Error - computeBestDepartureRunWay"
  
  
    ''' best arrival run-way is the one with minimal distance between start of 5 nautic descent ramp and last point of the route '''
    def computeBestArrivalRunWay(self):
        
        lastRouteWayPoint = AirlineRouteWayPoints.objects.all().filter(Route=self).distinct().order_by("Order").last()
        if ( lastRouteWayPoint ):
            wayPoint = AirlineWayPoint.objects.all().filter( WayPointName = lastRouteWayPoint.WayPoint ).first()
            if ( wayPoint ):
        
                lastRouteWayPoint = GeographicalPoint(wayPoint.Latitude , wayPoint.Longitude , EarthRadiusMeters)
        
                Ades =  self.ArrivalAirportICAOCode
                minimalDistanceMeters = 0.0
                bestRunWay = None
                first = True
                for rwy in AirlineRunWay.objects.filter(Airport=Ades):
                    runWay = RunWay(Name               = rwy.Name ,
                                    airportICAOcode    = Ades,
                                    LengthFeet         = rwy.LengthFeet,
                                    TrueHeadingDegrees = rwy.TrueHeadingDegrees,
                                    LatitudeDegrees    = rwy.LatitudeDegrees,
                                    LongitudeDegrees   = rwy.LongitudeDegrees)
                    rwyEnd = runWay.getEndOfRunWay()
                    ''' 5 Nm after end of runway '''
                    latitudeDegrees , longitudeDegrees = rwyEnd.getGeoPointAtDistanceHeading(ConstantClimbRampLengthNauticalMiles * NauticalMiles2Meter, runWay.getTrueHeadingDegrees())
                    pathEnd = GeographicalPoint(latitudeDegrees , longitudeDegrees, EarthRadiusMeters)
                    
                    distanceMeters = pathEnd.computeDistanceMetersTo(lastRouteWayPoint)
        
                    if first:
                        first = False
                        bestRunWay = rwy
                        minimalDistanceMeters = distanceMeters
                    else:
                        if ( distanceMeters < minimalDistanceMeters ):
                            bestRunWay = rwy
                            minimalDistanceMeters = distanceMeters
                        
                return bestRunWay.Name if (bestRunWay) else ""
            else:
                return "Error - computeBestArrivalRunWay"
        else:
            return "Error - computeBestArrivalRunWay"
 
    
class AirlineRouteWayPoints(models.Model):
    #Airline = models.ForeignKey(Airline, on_delete=models.CASCADE)
    Route = models.ForeignKey(AirlineRoute, on_delete=models.CASCADE)
    Order = models.IntegerField()
    # linked to the WayPoint class in the trajectory
    WayPoint = models.CharField(max_length = 100)
    
    ''' used to compare objects '''
    def __eq__(self, other):
        return models.Model.__eq__(self, other)
    
    ''' 14 Juin 2023 '''
    ''' since Django 2.2 if eq is implemented, need to implement hash otherwise we get a type error object is unhashable '''
    def __hash__(self):
        return super().__hash__()
    
    def getWayPointsListAsString(self):
        routeAsString = ""
        first = True
        for wayPoint in AirlineRouteWayPoints.objects.filter(Route=self).order_by("Order"):
            if (first):
                routeAsString += str(wayPoint.WayPoint).strip()
                first = False
            else:
                routeAsString += "-" + str(wayPoint.WayPoint).strip()
        return routeAsString
    
    def getWayPointName(self):
        return self.WayPoint
        
class AirlineAircraftInstances(object):

    ''' compute a list of aircraft instances to reach the same number of aircraft instances as the number of flight legs '''
    def computeAirlineAircraftInstances(self, airlineName, nbFlightLegs):
        aircraftInstanceList = []
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            nbAircrafts = AirlineAircraft.objects.filter(airline=airline).count()
            if ( nbAircrafts >= nbFlightLegs ):
                index = 0
                for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                    aircraftInstanceList.append(airlineAircraft.aircraftICAOcode + "-" + str(index).zfill(3))
                    index = index + 1
                return aircraftInstanceList
            
            else:
                index = 0
                while index < nbFlightLegs:
                    for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                        aircraftInstanceList.append(airlineAircraft.aircraftICAOcode + "-" + str(index).zfill(3))
                        index = index + 1
                        if ( index >= nbFlightLegs ):
                            break
                        
                return aircraftInstanceList       
        else:
            return []
        
    ''' aircraft instance = ICAO code + "-" + instance as xxx 3 digits '''
    def getAircraftInstanceICAOcode(self, acInstance):
        return str(acInstance).split("-")[0]
    
class AirlineAircraft(models.Model):
    aircraftICAOcode = models.CharField(max_length = 50)
    aircraftFullName = models.CharField(max_length = 500)
    numberOfAircraftsInService = models.IntegerField(default = 0)
    maximumOfPassengers = models.IntegerField(default = 0)
    costsFlyingPerHoursDollars = models.FloatField(default = 0)
    crewCostsPerFlyingHoursDollars = models.FloatField(default = 0)
    
    ''' 3rd May 2023 - add turn around times '''
    turnAroundTimesMinutes = models.FloatField(default = 0)
    landingLengthMeters = models.FloatField(default = 0)
    ''' Max TakeOff Weight '''
    takeOffMTOWLengthMeters = models.FloatField(default = 0)
    
    airline = models.ForeignKey(Airline, on_delete=models.CASCADE  )

    ''' used to compare objects '''
    def __eq__(self, other):
        return models.Model.__eq__(self, other)
    
    ''' 14 Juin 2023 '''
    ''' since Django 2.2 if eq is implemented, need to implement hash otherwise we get a type error object is unhashable '''
    def __hash__(self):
        return super().__hash__()
    
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
    
    def getTurnAroundTimesMinutes(self):
        return self.turnAroundTimesMinutes
    
''' 29th April 2023 - add target cruise level - departure run-way and arrival run-way '''
class AirlineCosts(models.Model):
    airline               = models.ForeignKey( Airline, on_delete=models.CASCADE , default=None )
    airlineAircraft       = models.ForeignKey( AirlineAircraft, on_delete=models.CASCADE , default=None )
    airlineRoute          = models.ForeignKey( AirlineRoute, on_delete=models.CASCADE , default=None )
    isAborted             = models.BooleanField()
    flightDurationSeconds = models.FloatField()
    initialTakeOffMassKg  = models.FloatField()
    targetCruiseLevelFeet = models.FloatField( default = 0.0 )
    adepRunway            = models.CharField( max_length = 50 , default=None )
    adesRunway            = models.CharField( max_length = 50 , default=None )
    finalMassKg           = models.FloatField()
    finalLengthMeters     = models.FloatField( default = 0.0)
    reducedClimbPowerCoeff = models.FloatField( default = 0.0)
    
    def getTakeOffMassKg(self):
        return self.initialTakeOffMassKg
    
    def getFinalMassKg(self):
        return self.finalMassKg
    
    def getFlightLegDurationSeconds(self):
        return self.flightDurationSeconds
    
    def getFlightLegLengthMeters(self):
        return self.finalLengthMeters
    
    def getFlightLegLengthMiles(self):
        return self.finalLengthMeters * Meter2NauticalMiles
    
    def getFlightLegFuelBurnKg(self):
        return ( self.initialTakeOffMassKg - self.finalMassKg)
    
  
    
''' add user to track IP address of the anonymous guests '''
class User(models.Model):
    userIp = models.CharField( max_length = 150 , default=None , primary_key = True)
    firstCnxDateTime = models.DateTimeField( auto_now_add=True )
    lastCnxDateTime = models.DateTimeField( auto_now_add=True )
    connexions = models.IntegerField(default=0)
    
    def __str__(self):
        return str(self.userIp)
    
    ''' used to compare objects '''
    def __eq__(self, other):
        return models.Model.__eq__(self, other)
    
    ''' 14 Juin 2023 '''
    ''' since Django 2.2 if eq is implemented, need to implement hash otherwise we get a type error object is unhashable '''
    def __hash__(self):
        return super().__hash__()
    
    def getUserIpAddress(self):
        return self.userIp
    
    def getNbConnexions(self):
        return self.connexions
    
    def setConnexions(self, nbCnx):
        self.connexions = nbCnx
        
    def getFirstCnxDateTime(self):
        return self.firstCnxDateTime
    
    def setFirstCnxDateTime(self, dateTimeNow):
        self.firstCnxDateTime = dateTimeNow
        
    def getLastCnxDateTime(self):
        return self.lastCnxDateTime
        
    def setLastCnxDateTime(self, dateTimeNow):
        self.lastCnxDateTime = dateTimeNow
    