'''
Created on 28 janv. 2023

@author: robert
'''

import logging
logger = logging.getLogger(__name__)

from django.http import  JsonResponse
from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute


def getAirlineCosts(request, airlineName):
    logger.setLevel(logging.INFO)
    logger.info ("views Airline Costs")
    
    airlineCostsList = []
    if (request.method == 'GET'):
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            
            for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
            
                    for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):            
            
                        airlineCostsDict = {
                            'airline'          : airlineName,
                            'airlineAircraft'  : airlineAircraft.aircraftFullName,
                            'departureAirport' : airlineRoute.DepartureAirport,
                            'arrivalAirport'   : airlineRoute.ArrivalAirport,
                            'isAborted'        : str(airlineCosts.isAborted) ,
                            'takeOffMassKg'    : round ( airlineCosts.initialTakeOffMassKg , 1),
                            'finalMassKg'      : round ( airlineCosts.finalMassKg , 1),
                            'flightDurationHours' : round ( ( float(airlineCosts.flightDurationSeconds ) / 3600.0 ), 4 )
                                        }
                        airlineCostsList.append(airlineCostsDict)
            return JsonResponse({'airlineCostsList': airlineCostsList})
        else:
            return JsonResponse({'errors': "unknown airline {0}".format(airlineName)})
    else:
        return JsonResponse({'errors': "expecting GET method"})
    