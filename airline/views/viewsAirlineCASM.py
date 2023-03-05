'''
Created on 4 mars 2023

@author: robert
'''

import logging
logger = logging.getLogger(__name__)

from django.http import  JsonResponse

from airline.models import Airline
from airline.models import AirlineCosts, AirlineAircraft, AirlineRoute

from trajectory.Environment.Constants import kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars
from trajectory.Environment.Constants import Meter2NauticalMiles

def getAirlineCASM(request, airlineName):
    
    logger.setLevel(logging.INFO)
    logger.info ("views Airline CASM")
    
    airlineCostsList = []

    if (request.method == 'GET'):
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            pass
        
            for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
                nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                    
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                
                    for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):    
                            
                        massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                        fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                
                        operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                                
                        crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                        totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars     
                        
                        ''' 5th February 2023 - Costs per Available Seat Mile '''
                        miles = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                        seatsPerMiles = nbSeats * miles
                        casmUSdollars = totalCostsUSdollars / seatsPerMiles
                            
                        airlineCostsDict = {
                                'airline'                   : airlineName,
                                'airlineAircraft'           : airlineAircraft.aircraftFullName,
                                'departureAirport'          : airlineRoute.DepartureAirport,
                                'arrivalAirport'            : airlineRoute.ArrivalAirport,
                                'isAborted'                 : str(airlineCosts.isAborted) ,
                                'takeOffMassKg'             : round ( airlineCosts.initialTakeOffMassKg , 1),
                                'finalMassKg'               : round ( airlineCosts.finalMassKg , 1),
                                'flightDurationHours'        : round ( ( float(airlineCosts.flightDurationSeconds ) / 3600.0 ), 4 ),
                                'fuelCostsUSdollars'         : round ( fuelCostsUSdollars , 2),
                                'operationalCostsUSdollars'  : round ( operationalFlyingCostsUSdollars , 2),
                                'crewCostsUSdollars'         : round ( crewCostsUSdollars , 2),
                                'totalCostsUSdollars'        : round ( totalCostsUSdollars , 2),
                                'nbSeats'                    : round ( nbSeats , 2),
                                'miles'                      : round ( miles , 2),
                                'CasmUSdollars'              : round ( casmUSdollars , 4 )
                                            }
                        airlineCostsList.append(airlineCostsDict)
                            
            return JsonResponse({'airlineCasmList': airlineCostsList})
        else:
            return JsonResponse({'errors': "unknown airline {0}".format(airlineName)})
    else:
        return JsonResponse({'errors': "expecting GET method"})