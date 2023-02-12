'''
Created on 11 févr. 2023

@author: robert

'''

from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute
from trajectory.Environment.Constants import kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars


def compute_total_costs( airlineCosts, airlineAircraft ):

    assert (isinstance(airlineCosts, AirlineCosts))
    assert (isinstance(airlineAircraft, AirlineAircraft))

    massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
    fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                            
    operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                            
    crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
    totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars
    return totalCostsUSdollars