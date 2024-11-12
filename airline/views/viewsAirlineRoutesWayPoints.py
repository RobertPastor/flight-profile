'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse

# Create your views here.
from airline.models import  AirlineRoute,  AirlineRouteWayPoints
from trajectory.models import AirlineWayPoint, AirlineAirport, AirlineRunWay

import logging
logger = logging.getLogger(__name__)

    
def getWayPointsOfRoute(routeWayPoints , adepRunWayObject, adesRunWayObject):
    
    assert (isinstance(adepRunWayObject, AirlineRunWay)) 
    assert not(adepRunWayObject is None)
    
    assert (isinstance(adesRunWayObject, AirlineRunWay)) 
    assert not(adesRunWayObject is None) 
    
    wayPointsList = []
    ''' 4th May 2023 - insert best departure runway '''
    runwayObj = { "name"      : adepRunWayObject.Name ,
                  "Longitude" : adepRunWayObject.getLongitudeDegrees(),
                  "Latitude"  : adepRunWayObject.getLatitudeDegrees()
                }
    #print ( runwayObj )
    wayPointsList.append( runwayObj )
    # list to avoid duplicates
    wayPointNames = []
    
    for waypoint in AirlineWayPoint.objects.all():
        for routeWayPoint in routeWayPoints:
            if ( waypoint.WayPointName == routeWayPoint.WayPoint):
                
                if ( waypoint.WayPointName not in wayPointNames):
                    wayPointNames.append(waypoint.WayPointName)
                    wayPointsList.append({
                        "name"      : waypoint.WayPointName ,
                        "Longitude" : waypoint.Longitude,
                        "Latitude"  : waypoint.Latitude
                        } )
                
    ''' 4th May 2023 - insert best arrival runway '''
    runwayObj = {
                    "name"      : adesRunWayObject.Name ,
                    "Longitude" : adesRunWayObject.getLongitudeDegrees(),
                    "Latitude"  : adesRunWayObject.getLatitudeDegrees()
                }
    #print ( runwayObj )
    wayPointsList.append( runwayObj )
     
    #print ( "length of waypoints list = {0}".format(len(wayPointsList)))
    return wayPointsList
    
    
def getRouteWayPoints(request, Adep, Ades):

    if (request.method == 'GET'):
        
        airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
        if airlineRoute :
            
            departureAirport = AirlineAirport.objects.filter(AirportICAOcode=Adep).first()
            arrivalAirport   = AirlineAirport.objects.filter(AirportICAOcode=Ades).first()
            
            ''' May 2023 - runways here are only strings '''
            adepRunWayStr = airlineRoute.computeBestDepartureRunWay()
            adepRunWayObject = AirlineRunWay.objects.filter( Name = adepRunWayStr , Airport = departureAirport ).first()
            
            #print ( "best departure runway = {0}".format( AdepRunWay ) )
            adesRunWayStr = airlineRoute.computeBestArrivalRunWay()
            adesRunWayObject = AirlineRunWay.objects.filter( Name = adesRunWayStr , Airport = arrivalAirport ).first()
            
            if adepRunWayObject and adesRunWayObject:

                routeWayPoints = AirlineRouteWayPoints.objects.filter(Route=airlineRoute)
                response_data = {
                    'departureAirport'      : Adep,
                    'arrivalAirport'        : Ades,
                    'airlineRouteWayPoints' : getWayPointsOfRoute(routeWayPoints , adepRunWayObject , adesRunWayObject),
                    'bestAdepRunway'        : adepRunWayStr,
                    'bestAdesRunway'        : adesRunWayStr
                    }
                return JsonResponse(response_data)
            else:
                response_data = { "errors" : "runway not found = AdepRwy= {0} - AdesRwy= {1}".format(adepRunWayStr,adesRunWayStr) }
                return JsonResponse(response_data)
        else:
            response_data = { "errors" : "route not found = Adep= {0} - Ades= {1}".format(Adep,Ades) }
            return JsonResponse(response_data)
    else:
        #raise ValueError("Expecting a GET - received something else")
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)
        
        
        