'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse

# Create your views here.
from airline.models import Airline, AirlineRoute, AirlineAircraft, AirlineRouteWayPoints
from trajectory.models import AirlineWayPoint

import logging
logger = logging.getLogger(__name__)

    
def getWayPointsOfRoute(routeWayPoints):
    wayPointsList = []
    for waypoint in AirlineWayPoint.objects.all():
        for routeWayPoint in routeWayPoints:
            if ( waypoint.WayPointName == routeWayPoint.WayPoint):
                logger.debug (waypoint.WayPointName)
                '''
                if waypoint.Latitude >= viewExtent["minlatitude"] and \
                    waypoint.Latitude <= viewExtent["maxlatitude"] and \
                    waypoint.Longitude >= viewExtent["minlongitude"] and \
                    waypoint.Longitude <= viewExtent["maxlongitude"] :
                '''
                wayPointsList.append({
                        "name" : waypoint.WayPointName ,
                        "Longitude": waypoint.Longitude,
                        "Latitude": waypoint.Latitude
                        } )
    #print ( "length of waypoints list = {0}".format(len(wayPointsList)))
    return wayPointsList
    
    
def getRouteWayPoints(request, Adep, Ades):
    logger.debug ( "URL WayPoints for Route")
    if (request.method == 'GET'):
        logger.debug( "Received Get for Route WayPoints")
        logger.debug ( Adep )
        logger.debug  ( Ades )
        route = AirlineRoute.objects.filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
        if route :
            print ( str(route) )
            routeWayPoints = AirlineRouteWayPoints.objects.filter(Route=route)
            response_data = {'airlineRouteWayPoints': getWayPointsOfRoute(routeWayPoints)}
            return JsonResponse(response_data)
             
        else:
            response_data = { "errors" : "route not found = Adep= {0] - Ades= {1}".format(Adep,Ades) }
            return JsonResponse(response_data)
            
    else:
        #raise ValueError("Expecting a GET - received something else")
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)
        
        
        