'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse

from airline.models import Airline

import logging
logger = logging.getLogger(__name__)

from trajectory.views.utils import  getAirlineRoutesFromDB


def getAirlineRoutes(request , airlineName):
    logger.debug ("get Airline Routes for airline = {0}".format(airlineName) )
    if (request.method == 'GET'):
        logger.debug("get request received - Airline Routes")
        
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):

            response_data = { 'airlineRoutes' : getAirlineRoutesFromDB(airline) }
            return JsonResponse( response_data )
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})

    else:
        return JsonResponse({'errors': "expecting GET method"})
    
    