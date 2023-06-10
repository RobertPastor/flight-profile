'''
Created on 8 juin 2023

@author: robert
'''

import logging
logger = logging.getLogger(__name__)
from django.http import  JsonResponse

from airline.models import Airline
from trajectory.views.utils import getAirportsFromDB
from trajectory.models import AirlineStandardDepartureArrivalRoute


def retrieveSidStarId( request ):
    ''' Sid Star Id to retrieve is based upon a session data '''
    
    SidStarId = request.session.get('SidStarId', default=0)
    SidStarCount = AirlineStandardDepartureArrivalRoute.objects.count()
    if SidStarId < SidStarCount :
        pass
    else:
        SidStarId = 0
    #print ( "Sid Star Id = {0}".format(SidStarId))
    return SidStarId


def setNextSidStarId( request ):
        
    SidStarId = request.session.get('SidStarId', default=0)
    SidStarCount = AirlineStandardDepartureArrivalRoute.objects.count()
    if SidStarId < SidStarCount :
        SidStarId = SidStarId + 1
    else:
        SidStarId = 0
        
    request.session['SidStarId'] = SidStarId
    #print ( "Sid Star Id = {0}".format(SidStarId))


def getSidStarFromDB(airline , request ):
    ''' Sid Star Id is used to loop through the existing Sid Star '''
    
    assert ( isinstance ( airline , Airline ))

    SidStarId = retrieveSidStarId ( request )
    index = 0
    
    sidStars = AirlineStandardDepartureArrivalRoute.objects.all()
    sidStarJson = {}
    for sidStar in sidStars:
        #print ( sidStar )
        if ( sidStar and index == SidStarId):
            
            #print ( sidStar )
            sidStarJson = {}
            sidStarJson["isSID"]                     = sidStar.getIsSID()
            sidStarJson["DepartureArrivalAirport"]   = sidStar.getDepartureArrivalAirport().getAsJson()
            sidStarJson["DepartureArrivalRunWay"]    = sidStar.getDepartureArrivalRunWay().getAsJson()
            sidStarJson["SidStarWayPoints"]          = sidStar.getWayPointsAsGeoPointsList()
        index = index + 1
        
    setNextSidStarId( request )
    return sidStarJson


def showSidStar(request , airlineName):
    #print  ("launch Flight Profile - with airline = {0}".format(airlineName))
    
    if (request.method == 'GET'):
        
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            
            #print (airline)
            responseData = {}
            airportsList = getAirportsFromDB( airline )
            sidStarsJson = getSidStarFromDB ( airline , request )
            responseData = {
                'airports' : airportsList,
                'SidStar'  : sidStarsJson}
            
            return JsonResponse(responseData)
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})
    else:
        return JsonResponse({'errors': "expecting GET method"})