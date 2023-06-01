
# import Http Response from django

import json
import os
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse , Http404 
from wsgiref.util import FileWrapper
from django.http import JsonResponse
from datetime import datetime


from airline.models import Airline


def index(request):
    # create a function
    # create a dictionary to pass
    # data to the template
    ''' send the list of airlines to populate the dropdown list in the navigation bar '''
    airlineList = []
    for airline in Airline.objects.all():
        airlineDict = {}
        airlineDict["Name"] = airline.Name
        airlineDict["MinLongitudeDegrees"] = airline.MinLongitudeDegrees
        airlineDict["MinLatitudeDegrees"]  = airline.MinLatitudeDegrees
        airlineDict["MaxLongitudeDegrees"] = airline.MaxLongitudeDegrees
        airlineDict["MaxLatitudeDegrees"]  = airline.MaxLatitudeDegrees
       
        airlineList.append(airlineDict)
        
    context = {"airlines" : json.dumps(airlineList) }
    # return response with template and context
    return render(request, "index-og.html", context)
    #return render(request, "index-maplibre.html", context)
    
    
def doc(request):
    context = {"Author" : "Robert PASTOR"}
    return render(request, "index-doc.html", context)


@csrf_protect
def downloadPdfPresentation(request):
    pass
    if request.method == 'GET':
        
        fileName = 'AirlineServicesPresentation.pdf'
        #fileName = fileName + '-{0}.pdf'.format(datetime.now().strftime("%d-%b-%Y-%Hh%Mm%S"))
        filePath = os.path.join( os.path.dirname(__file__) , fileName)
        #print ( filePath )
        if os.path.exists(filePath):
            
            with open(filePath, 'rb') as fh:
                response = HttpResponse(fh.read(), content_type="application/pdf")
                response['Content-Disposition'] = 'attachment; filename=' + (fileName)
                return response
        
        else:
            raise Http404
    else:
        response_data = { 'errors' : 'expecting a GET - received something else = {0}'.format(request.method) }
        return JsonResponse(response_data)