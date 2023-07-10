
# import Http Response from django

import json
from django.utils import timezone

from django.shortcuts import render
from airline.models import Airline, User


def get_ip(request):
    address = request.META.get('HTTP_X_FORWARDED_FOR')
    if address:
        ip = address
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def save_user(request):
    userIp = get_ip(request)
    ''' count number of users '''
    userCount = User.objects.filter(userIp=userIp).count()
    #print ( userCount )
    if userCount == 0:
        ''' user does not exists '''
        #now().date() may be different from current date, since it uses UTC
        user = User(userIp=userIp)
        user.save()
        if user:
            user.setConnexions(1)
            user.save()
    else:
        #print ( "user is existing ")
        user = User.objects.filter(userIp=userIp).first()
        if user:
            cnxCount = user.getNbConnexions()
            #print ( cnxCount )
            cnxCount = cnxCount + 1
            #print ( cnxCount )
            #print ( "user has several connexions = {0}".format(cnxCount) )
            user.setConnexions(cnxCount)
            user.setLastCnxDateTime(timezone.now())
            user.save()

def index(request):
    # create a function
    # create a dictionary to pass
    # data to the template
    
    ''' save anonymous user's IP address '''
    save_user(request)
    
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


