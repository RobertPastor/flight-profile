
import logging
logger = logging.getLogger(__name__)

from django.template import loader
from django.core import serializers
from django.http import HttpResponse , JsonResponse

from airline.models import AirlineRoute, Airline
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



def getAirportsFromDB(airline):
    ICAOlist = []
    airportsList = []
    ''' airports are not related to airlines '''
    for airport in AirlineAirport.objects.all():
        ''' routes are related to airlines '''
        for airlineRoute in AirlineRoute.objects.filter(airline = airline):
            #print ( airlineRoute )
            if (airport.AirportICAOcode == airlineRoute.getDepartureAirportICAOcode()) or (airport.AirportICAOcode == airlineRoute.getArrivalAirportICAOcode() ):
                if ( airport.AirportICAOcode not in ICAOlist):
                    logger.debug (airport.AirportICAOcode)
                    # add airport only once
                    ICAOlist.append(airport.AirportICAOcode)
                    airportsList.append({
                        "AirportICAOcode" : airport.AirportICAOcode ,
                        "AirportName": airport.AirportName,
                        "Longitude": airport.Longitude,
                        "Latitude": airport.Latitude
                        } )
    return airportsList


def getAirports(request, airlineName):
    logger.debug ("get Airports")
    if (request.method == 'GET'):
        logger.debug ("get request received - airports")
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            logger.debug ( airline )
            airports = getAirportsFromDB(airline)
            response_data = {'airports': airports}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})
    
    else:
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)

