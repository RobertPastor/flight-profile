'''
Created on 26 déc. 2022

@author: robert PASTOR
'''
from airline.models import  AirlineAircraft
from trajectory.models import  AirlineRunWay , BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance


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
