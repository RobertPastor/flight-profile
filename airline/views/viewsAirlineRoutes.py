'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse

from airline.models import Airline, AirlineRoute, AirlineAircraft, AirlineRouteWayPoints

import logging
logger = logging.getLogger(__name__)


def getAirlineRoutesFromDB():
    airlineRoutesList = []
    for airlineRoute in AirlineRoute.objects.all():
        #logger.debug ( str ( airlineRoute ) )
        airlineRoutesList.append({
                "DepartureAirport" : airlineRoute.DepartureAirport ,
                "DepartureAirportICAOCode": airlineRoute.DepartureAirportICAOCode,
                "ArrivalAirport": airlineRoute.ArrivalAirport,
                "ArrivalAirportICAOCode": airlineRoute.ArrivalAirportICAOCode
                } )
    return airlineRoutesList


def getAirlineRoutes(request):
    logger.debug ("get Airline Routes")
    if (request.method == 'GET'):
        logger.debug("get request received - Airline Routes")
        airlineRoutes = getAirlineRoutesFromDB()
        response_data = {'airlineRoutes': airlineRoutes}
        return JsonResponse(response_data)
    else:
        return JsonResponse({'errors': "expecting GET method"})
    
    