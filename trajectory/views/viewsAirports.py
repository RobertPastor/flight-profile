
import logging
logger = logging.getLogger(__name__)

from django.template import loader
from django.core import serializers
from django.http import HttpResponse , JsonResponse

from airline.models import AirlineRoute
from trajectory.models import  AirlineAirport

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



def getAirportsFromDB():
    airportsList = []
    for airport in AirlineAirport.objects.all():
        logger.debug (airport.AirportICAOcode)
        for airlineRoute in AirlineRoute.objects.all():
            
            if (airport.AirportICAOcode == airlineRoute.getDepartureAirportICAOcode()) or (airport.AirportICAOcode == airlineRoute.getArrivalAirportICAOcode() ):
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
    
    
