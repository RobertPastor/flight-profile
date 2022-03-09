from django.shortcuts import render
from django.http import HttpResponse , JsonResponse

# Create your views here.
from .models import AirlineRoute

import logging
logger = logging.getLogger(__name__)

def getAirlineRoutesFromDB():
    airlineRoutesList = []
    for airlineRoute in AirlineRoute.objects.all():
        logger.debug ( str ( airlineRoute ) )
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