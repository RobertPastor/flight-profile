'''
Created on 26 déc. 2022

@author: robert
'''
from airline.models import Airline, AirlineRoute, AirlineAircraft
from trajectory.models import  AirlineAirport, AirlineRunWay



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
        airlineAircraftsList.append({
            "airlineAircraftICAOcode" : airlineAircraft.aircraftICAOcode,
            "airlineAircraftFullName" : airlineAircraft.aircraftFullName
            })
    #print ("length of airline aircrafts list = {0}".format(len(airlineAircraftsList)))
    return airlineAircraftsList
