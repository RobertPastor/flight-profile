
import logging
logger = logging.getLogger(__name__)

from django.template import loader
from django.core import serializers
from django.http import HttpResponse , JsonResponse

from airline.models import Airline
from trajectory.views.utils import getAirportsFromDB

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

