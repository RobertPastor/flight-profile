'''
Created on 11 févr. 2023

@author: robert

'''

from airline.models import  AirlineCosts, AirlineAircraft
from trajectory.models import AirlineAirport, AirlineRunWay
from trajectory.Environment.Constants import Kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars


def compute_total_costs( airlineCosts, airlineAircraft ):

    assert (isinstance(airlineCosts, AirlineCosts)) and not(airlineCosts is None)
    assert (isinstance(airlineAircraft, AirlineAircraft)) and not(airlineAircraft is None)

    massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
    fuelCostsUSdollars = massLossKg * Kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                            
    operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                            
    crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
    totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars
    return totalCostsUSdollars

def computeAirportNumberOfRunways( airportICAOcode ):
    
    airport = AirlineAirport.objects.filter( AirportICAOcode = airportICAOcode).first()
    assert ( isinstance( airport, AirlineAirport )) and not(airport is None)
    #print ( "utils in airline/views/utils - airport = {0}".format( airport ) )
    #for runWay in AirlineRunWay.objects.filter(Airport=airport):
    #    print ( runWay )
    #print ( "{0} - number of runways = {1}".format( airport.getICAOcode() , AirlineRunWay.objects.filter(Airport=airport).count() ))
    return  AirlineRunWay.objects.filter(Airport=airport).count()
    