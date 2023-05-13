'''
Created on 26 déc. 2022

@author: robert PASTOR
'''
from airline.models import  AirlineAircraft, AirlineRoute
from trajectory.models import  AirlineRunWay , BadaSynonymAircraft, AirlineAirport
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance

from trajectory.Environment.Earth import EarthRadiusMeters
from trajectory.Environment.Constants import Meter2NauticalMiles
from trajectory.Guidance.GeographicalPointFile import GeographicalPoint



def computeRouteLengthMiles( AdepICAOcode, AdesICAOcode ):
    adepAirport = AirlineAirport.objects.filter( AirportICAOcode = AdepICAOcode ).first()
    adesAirport = AirlineAirport.objects.filter( AirportICAOcode = AdesICAOcode ).first()
    
    adepGeo = GeographicalPoint(adepAirport.getLatitudeDegrees() , adepAirport.getLongitudeDegrees(), EarthRadiusMeters)
    adesGeo = GeographicalPoint(adesAirport.getLatitudeDegrees() , adesAirport.getLongitudeDegrees(), EarthRadiusMeters)
            #print ( "end of runway extended path = {0}".format(pathEnd) )

    return adepGeo.computeDistanceMetersTo(adesGeo) * Meter2NauticalMiles


def getAirlineRoutesFromDB(airline):
    airlineRoutesList = []
    for airlineRoute in AirlineRoute.objects.filter(airline = airline):
        #logger.debug ( str ( airlineRoute ) )
        airlineRoutesList.append({
                "Airline"                  : airlineRoute.airline.Name,
                "DepartureAirport"         : airlineRoute.DepartureAirport ,
                "DepartureAirportICAOCode" : airlineRoute.DepartureAirportICAOCode,
                "ArrivalAirport"           : airlineRoute.ArrivalAirport,
                "ArrivalAirportICAOCode"   : airlineRoute.ArrivalAirportICAOCode,
                "RouteLengthMiles"         : round ( computeRouteLengthMiles(airlineRoute.DepartureAirportICAOCode , airlineRoute.ArrivalAirportICAOCode) , 2 )
                } )
    return airlineRoutesList



def getAirlineRunWaysFromDB():
    airlineRunWaysList = []
    for airlineRunWay in AirlineRunWay.objects.all():
        airlineRunWaysList.append( {
            'airlineAirport': airlineRunWay.Airport.AirportICAOcode,
            'airlineRunWayName' : airlineRunWay.Name,
            'airlineRunWayTrueHeadindDegrees': airlineRunWay.TrueHeadingDegrees})
    #print ( "Size of RunWays list = {0}".format(len(airlineRunWaysList)))
    return airlineRunWaysList



def getAirlineAircraftsFromDB(airline):
    airlineAircraftsList = []
    for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
        #print (str(airlineAircraft))
        acMaxTakeOffWeightKg = 0.0
        acMinTakeOffWeightKg = 0.0
        acMaxOpAltitudeFeet  = 0.0 
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=airlineAircraft.aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
            if acPerformance:
                acMaxTakeOffWeightKg = acPerformance.getMaximumMassKilograms()
                acMinTakeOffWeightKg = acPerformance.getMinimumMassKilograms()
                acMaxOpAltitudeFeet  = acPerformance.getMaxOpAltitudeFeet()
        airlineAircraftsList.append({
            "airlineAircraftICAOcode" : airlineAircraft.aircraftICAOcode,
            "airlineAircraftFullName" : airlineAircraft.aircraftFullName,
            "acMaxTakeOffWeightKg"    : acMaxTakeOffWeightKg,
            "acMinTakeOffWeightKg"    : acMinTakeOffWeightKg,
            "acMaxOpAltitudeFeet"     : acMaxOpAltitudeFeet
            })
    #print ("length of airline aircrafts list = {0}".format(len(airlineAircraftsList)))
    return airlineAircraftsList
