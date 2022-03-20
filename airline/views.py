from django.http import  JsonResponse

# Create your views here.
from .models import AirlineRoute, AirlineAircraft

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
    
    
def getAirlineFleetFromDB():
    airlineFleetList = []
    for airlineAircraft in AirlineAircraft.objects.all():
        #logger.debug ( str ( airlineAircraft ) )
        airlineFleetList.append({
            "AircraftICAOcode" : airlineAircraft.aircraftICAOcode,
            "AircraftFullName" : airlineAircraft.aircraftFullName,
            "NumberOfAircrafts" : airlineAircraft.numberOfAircraftsInService,
            "MaxNumberOfPassengers" : airlineAircraft.maximumOfPassengers,
            "CostsFlyingHoursDollars": airlineAircraft.costsFlyingPerHoursDollars})
    return airlineFleetList
    
    
def getAirlineFleet(request):
    logger.debug ("get Airline Fleet")
    if (request.method == 'GET'):
        logger.debug("get request received - Airline Fleet")
        airlineFleet = getAirlineFleetFromDB()
        response_data = {'airlineFleet': airlineFleet}
        return JsonResponse(response_data)