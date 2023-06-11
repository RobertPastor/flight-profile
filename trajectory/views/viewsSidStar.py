'''
Created on 8 juin 2023

@author: robert
'''

import logging
logger = logging.getLogger(__name__)
from django.http import  JsonResponse

from trajectory.models import AirlineStandardDepartureArrivalRoute, AirlineAirport, AirlineRunWay, AirlineWayPoint


def getSidStarFromDB( SidOrStar , airport , runway, waypoint ):
    
    #print ( airport )
    ''' Sid Star Id is used to loop through the existing Sid Star '''
    
    assert ( isinstance ( airport , str ))
    
    airport = AirlineAirport.objects.filter ( AirportICAOcode = airport ).first()
    assert ( isinstance ( airport , AirlineAirport ))
    #print ( airport )
    
    runway = AirlineRunWay.objects.filter( Name = runway , Airport = airport ).first()
    assert ( isinstance ( runway , AirlineRunWay ))

    #print ( runway )
    
    waypoint = AirlineWayPoint.objects.filter ( WayPointName = waypoint).first()
    assert ( isinstance ( waypoint , AirlineWayPoint ))

    #print ( waypoint )
    
    isSID = True if ( SidOrStar.lower() == "sid" ) else False
    
    sidStarJson = {}
    
    if ( airport and runway and waypoint ):
        sidStar = AirlineStandardDepartureArrivalRoute.objects.filter( isSID = isSID ,
                                                                       DepartureArrivalAirport = airport ,
                                                                       DepartureArrivalRunWay = runway ,
                                                                       FirstLastRouteWayPoint = waypoint).first()
        
        if ( sidStar ):
            
                        #print ( sidStar )
                        sidStarJson = {}
                        sidStarJson["isSID"]                     = sidStar.getIsSID()
                        sidStarJson["DepartureArrivalAirport"]   = sidStar.getDepartureArrivalAirport().getAsJson()
                        sidStarJson["DepartureArrivalRunWay"]    = sidStar.getDepartureArrivalRunWay().getAsJson()
                        sidStarJson["SidStarWayPoints"]          = sidStar.getWayPointsAsGeoPointsList()
                
        
    return sidStarJson


def showSidStar(request , SidOrStar , airport , runway, waypoint ):
    #print  ("launch Flight Profile - with airline = {0}".format(airlineName))
    
    if (request.method == 'GET'):
        
            #print (airline)
            responseData = {}
            sidStarsJson = getSidStarFromDB ( SidOrStar , airport , runway, waypoint )
            responseData = {
                'SidStar'  : sidStarsJson}
            
            return JsonResponse(responseData)
        
    else:
        return JsonResponse({'errors': "expecting GET method"})