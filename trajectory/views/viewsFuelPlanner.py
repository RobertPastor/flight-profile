'''
Created on 13 mai 2023

@author: robert
'''

import logging
logger = logging.getLogger(__name__)
from django.http import  JsonResponse

from airline.models import Airline
from trajectory.views.utils import  getAirlineAircraftsFromDB, getAirlineRoutesFromDB, getAirlineTripPerformanceFromDB


def launchFuelPlanner(request , airlineName):
    #print  ("launch Flight Profile - with airline = {0}".format(airlineName))
    if (request.method == 'GET'):
        
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            
            airlineAircraftsList    = getAirlineAircraftsFromDB( airline )     
            airlineRoutesList       = getAirlineRoutesFromDB( airline )
            aircraftPerformanceList = getAirlineTripPerformanceFromDB( airline )

            response_data = {
                'airlineAircrafts'    : airlineAircraftsList,
                'airlineRoutes'       : airlineRoutesList,
                'aircraftPerformance' : aircraftPerformanceList
                
                }
            
            return JsonResponse(response_data)
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})
    else:
        return JsonResponse({'errors': "expecting GET method"})