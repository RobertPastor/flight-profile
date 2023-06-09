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


def getSidStarFromDB(airline):
    pass
    assert ( isinstance ( airline , Airline ))
    sidStarsList = []
    for sidStar in AirlineStandardDepartureArrivalRoute.objects.all():
        print ( sidStar )
        sidStarJson = {}
        sidStarJson["isSID"] = sidStar.getIsSID()
        sidStarJson["DepartureArrivalAirport"] = sidStar.getDepartureArrivalAirport().getICAOcode()
        sidStarsList.append( sidStarJson )
    return sidStarsList


def showSidStar(request , airlineName):
    #print  ("launch Flight Profile - with airline = {0}".format(airlineName))
    if (request.method == 'GET'):
        
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            
            print (airline)
            responseData = {}
            airportsList = getSidStarFromDB(airline)
            sidStarsList = getSidStarFromDB ( airline )
            responseData = {
                'airports' : airportsList,
                'SidStars' : sidStarsList}
            
            return JsonResponse(responseData)
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})
    else:
        return JsonResponse({'errors': "expecting GET method"})