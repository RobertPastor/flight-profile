from django.shortcuts import render
from django.template import loader
from django.core import serializers
from django.http import HttpResponse , JsonResponse

import json
import logging
logger = logging.getLogger(__name__)

#from trajectory.models import SiteMessage
from trajectory.models import Airport

# Create your views here.
def indexTrajectory(request):
    # return HttpResponse('Hello from Python!')
    template = loader.get_template('./index.html')

    siteMessages = []
    '''    for siteMessage in SiteMessage.objects.all().order_by("event_date"):
        if siteMessage.active == True:
            siteMessages.append(siteMessage)
    '''            
    siteMessages = serializers.serialize('json', siteMessages)
    
    context = {'siteMessages' : siteMessages}
    return HttpResponse(template.render(context, request))

def index(request):
    # create a function
    # create a dictionary to pass
    # data to the template
    context ={}
    # return response with template and context
    return render(request, "index.html", context)

def getAirportsFromDB():
    
    airportsList = []
    for airport in Airport.objects.all():
        logger.debug (airport.AirportICAOcode)
        if str(airport.AirportICAOcode).startswith("K") and str(airport.AirportName).endswith("Intl"):
            airportsList.append({
                "AirportICAOcode" : airport.AirportICAOcode ,
                "AirportName": airport.AirportName,
                "Longitude": airport.Longitude,
                "Latitude": airport.Latitude
                } )
    return airportsList

def getAirports(request):
    logger.debug ("get Airports")
    if (request.method == 'GET'):
        logger.debug("get request received - airports")
        airports = getAirportsFromDB()
        response_data = {'airports': airports}
        return JsonResponse(response_data)
    
def getFlightProfile(request):
    logger.debug ("get Flight Profile")
    if (request.method == 'GET'):
        fileName = "A319-KATL-PANC-Atlanta-Hartsfield-Jackson-Atlanta-Intl-Rwy-08L-Anchorage-Ted-Stevens-Anchorage-Intl-rwy-07L-16-Jan-2022-11h28m27.kml"
        response_data = {'kmlURL': "/static/trajectory/kml/" + fileName}
        return JsonResponse(response_data)
