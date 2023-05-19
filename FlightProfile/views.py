
# import Http Response from django
from django.shortcuts import render
from airline.models import Airline
import json

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