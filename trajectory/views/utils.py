'''
Created on 26 déc. 2022

@author: robert PASTOR
'''

from airline.models import Airline,  AirlineAircraft, AirlineRoute, AirlineCosts

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


def getAirlineTripPerformanceFromDB( airline ):
    
    assert ( isinstance( airline , Airline ))
    airlineTripPerformanceList = []
    for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
        pass
        badaAircraft = BadaSynonymAircraft.objects.all().filter( AircraftICAOcode=airlineAircraft.aircraftICAOcode ).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
            if acPerformance:
                for airlineRoute in AirlineRoute.objects.filter(airline = airline):
                    pass
                    for airlineCosts in AirlineCosts.objects.filter( airline = airline, airlineAircraft = airlineAircraft, airlineRoute = airlineRoute):
                        OneHourReserveFuelKg =  ( airlineCosts.getFlightLegFuelBurnKg() / airlineCosts.getFlightLegDurationSeconds() ) * 3600.0 
                        airlineTripPerformanceList.append( {
                            "Airline"               : airlineRoute.airline.Name,
                            "Aircraft"              : airlineAircraft.getAircraftICAOcode(),
                            "Route"                 : airlineRoute.getFlightLegAsString(),
                            "TakeOffMassKg"         : airlineCosts.getTakeOffMassKg(),
                            "LegDurationSec"        : round ( airlineCosts.getFlightLegDurationSeconds() , 1 ) ,
                            "LegLengthMiles"        : round ( airlineCosts.getFlightLegLengthMiles() , 1 ) ,
                            "TripFuelBurnKg"        : round ( airlineCosts.getFlightLegFuelBurnKg() , 1 ) ,
                            "OneHourReserveFuelKg"      : round (  OneHourReserveFuelKg , 1 ), 
                            "OptimalTakeOffMassKg"      : round ( acPerformance.getMinimumMassKilograms() + ( ( 80.0 * acPerformance.getMaximumPayLoadMassKilograms() ) / 100.0 ) + airlineCosts.getFlightLegFuelBurnKg() + OneHourReserveFuelKg , 1 )
                            })
    return airlineTripPerformanceList



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
                acMaxPayLoadKg       = acPerformance.getMaximumPayLoadMassKilograms()
        airlineAircraftsList.append({
            "airlineAircraftICAOcode" : airlineAircraft.aircraftICAOcode,
            "airlineAircraftFullName" : airlineAircraft.aircraftFullName,
            "acMaxTakeOffWeightKg"    : acMaxTakeOffWeightKg,
            "acMinTakeOffWeightKg"    : acMinTakeOffWeightKg,
            "acMaxOpAltitudeFeet"     : acMaxOpAltitudeFeet,
            "acMaxPayLoadKg"          : acMaxPayLoadKg
            })
    #print ("length of airline aircrafts list = {0}".format(len(airlineAircraftsList)))
    return airlineAircraftsList
