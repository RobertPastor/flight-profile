'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse

from airline.models import Airline, AirlineRoute

import logging
logger = logging.getLogger(__name__)


def getAirlineRoutesFromDB(airline):
    airlineRoutesList = []
    for airlineRoute in AirlineRoute.objects.filter(airline = airline):
        #logger.debug ( str ( airlineRoute ) )
        airlineRoutesList.append({
                "Airline": airlineRoute.airline.Name,
                "DepartureAirport" : airlineRoute.DepartureAirport ,
                "DepartureAirportICAOCode": airlineRoute.DepartureAirportICAOCode,
                "ArrivalAirport": airlineRoute.ArrivalAirport,
                "ArrivalAirportICAOCode": airlineRoute.ArrivalAirportICAOCode
                } )
    return airlineRoutesList


def getAirlineRoutes(request , airlineName):
    logger.debug ("get Airline Routes for airline = {0}".format(airlineName) )
    if (request.method == 'GET'):
        logger.debug("get request received - Airline Routes")
        
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):

            airlineRoutes = getAirlineRoutesFromDB(airline)
            response_data = {'airlineRoutes': airlineRoutes}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})

    else:
        return JsonResponse({'errors': "expecting GET method"})
    
    