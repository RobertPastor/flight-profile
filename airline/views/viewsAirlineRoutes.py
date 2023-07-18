'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse
from airline.models import Airline
from trajectory.views.utils import getAirlineRoutesFromDB

def getAirlineRoutes(request , airlineName):
    
    if (request.method == 'GET'):
        
        airline = Airline.objects.filter(Name=airlineName).first()
        if airline:
            
            response_data = { 'airlineRoutes' : getAirlineRoutesFromDB(airline) }
            return JsonResponse( response_data )
        else:
            response_data = {'errors': "airline with name {0} not found".format(airlineName)}
            return JsonResponse(response_data)

    else:
        response_data = {'errors': "expecting GET method - received = {0}".format(request.method)}
        return JsonResponse(response_data)