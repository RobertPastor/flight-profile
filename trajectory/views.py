import os
from FlightProfile.settings import BASE_DIR
from django.shortcuts import render
from django.template import loader
from django.core import serializers
from django.http import HttpResponse , JsonResponse

from xml.dom import minidom
from django.core.files import File

import logging
logger = logging.getLogger(__name__)

#from trajectory.models import SiteMessage
from trajectory.models import Airport, WayPoint
from airline.models import AirlineRoute, AirlineAircraft, AirlineRouteWayPoints
from airline.views import getAirlineRoutesFromDB

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
    
    
def getPlaceMarks(fileName):
    placeMarksList = []
    print ( BASE_DIR )
    filePath = os.path.join ( BASE_DIR , os.path.join ( "trajectory/static/kml"  , fileName ) )
    print ( filePath )
    if (os.path.isfile(filePath)):
        print ( "file = {0} does exist".format(filePath))
        f = open(filePath)
        file = File(f)
        parseXml = minidom.parse(file)
        #use getElementsByTagName() to get tag
        placeMarks = parseXml.getElementsByTagName('Placemark')
        for placeMark in placeMarks:
            name = ""
            try:
                name = placeMark.getElementsByTagName("name")[0].childNodes[0].data
                #print ( name )
            except Exception:
                name = ""
            point = placeMark.getElementsByTagName("Point")[0]
            coordinates = point.getElementsByTagName("coordinates")[0].childNodes[0].data
            #print ( coordinates )
            placeMarksList.append({ 
                "name": name,
                "longitude": str(coordinates).split(",")[0],
                "latitude": str(coordinates).split(",")[1],
                "height": str(coordinates).split(",")[2]
            })
    else:
        print ( "file = {0} does not exist".format(filePath))
    print ( "length place marks = {0}".format(len ( placeMarksList )) )
    return placeMarksList
    
    
def showFlightProfile(request):
    print ("show Flight Profile")
    if (request.method == 'GET'):
        fileName = "A319-KATL-PANC-Atlanta-Hartsfield-Jackson-Atlanta-Intl-Rwy-08L-Anchorage-Ted-Stevens-Anchorage-Intl-rwy-07L-16-Jan-2022-11h28m27.kml"
        response_data = {
            'kmlURL': "/static/kml/" + fileName,
            'placeMarks' : getPlaceMarks(fileName)}
        return JsonResponse(response_data)
    
    
def getWayPointsFromDB(viewExtent):
    wayPointsList = []
    for waypoint in WayPoint.objects.all():
        logger.debug (waypoint.WayPointName)
        '''
        if waypoint.Latitude >= viewExtent["minlatitude"] and \
            waypoint.Latitude <= viewExtent["maxlatitude"] and \
            waypoint.Longitude >= viewExtent["minlongitude"] and \
            waypoint.Longitude <= viewExtent["maxlongitude"] :
        '''
        wayPointsList.append({
                "name" : waypoint.WayPointName ,
                "Longitude": waypoint.Longitude,
                "Latitude": waypoint.Latitude
                } )
    print ( "length of waypoints list = {0}".format(len(wayPointsList)))
    return wayPointsList
    

def getWayPoints(request):
    logger.debug ("get WayPoints")
    if (request.method == 'GET'):
        logger.debug("get request received - WayPoints")
        
        viewExtent = {
           "minlatitude" : int(request.GET['minlatitude']),
           "maxlatitude" : int(request.GET['maxlatitude']),
           "minlongitude" : int(request.GET['minlongitude']),
           "maxlongitude" : int(request.GET['maxlongitude'])
        }
        logger.debug(viewExtent)
        print ( viewExtent )
        waypoints = getWayPointsFromDB(viewExtent)
        response_data = {'waypoints': waypoints}
        return JsonResponse(response_data)
  
    
def getAirlineAircraftsFromDB():
    airlineAircraftsList = []
    for airlineAircraft in AirlineAircraft.objects.all():
        #print (str(airlineAircraft))
        airlineAircraftsList.append({
            "airlineAircraftICAOcode" : airlineAircraft.aircraftICAOcode,
            "airlineAircraftFullName" : airlineAircraft.aircraftFullName
            })
    #print ("length of airline aircrafts list = {0}".format(len(airlineAircraftsList)))
    return airlineAircraftsList


def launchFlightProfile(request):
    logger.debug ("launch Flight Profile")
    if (request.method == 'GET'):
        airlineAircraftsList = getAirlineAircraftsFromDB()
        airlineRoutesList = getAirlineRoutesFromDB()
        response_data = {
            'airlineAircrafts': airlineAircraftsList,
            'airlineRoutes': airlineRoutesList}
        return JsonResponse(response_data)
    
def getAirport(airportICAOcode):
    for airport in Airport.objects.all():
        if (airport.AirportICAOcode == airportICAOcode ):
            return { "AirportICAOcode" : airport.AirportICAOcode ,
                     "AirportName"     : airport.AirportName,
                     "Longitude"       : airport.Longitude,
                     "Latitude"        : airport.Latitude         }
    return {}
    
def computeFlightProfile(request):
    logger.debug ("compute Flight Profile")
    routeWayPointsList = []
    if (request.method == 'GET'):
        aircraftICAOcode = request.GET['aircraft']
        #print ( aircraftICAOcode )
        airlineRoute = request.GET['route']
        #print ( airlineRoute )
        #print ( str(airlineRoute).split("-")[0] )
        #print ( str(airlineRoute).split("-")[1] )
        departureAirportICAOcode = str(airlineRoute).split("-")[0]
        arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
        airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode = departureAirportICAOcode, ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
        if (airlineRoute):
            #print ( airlineRoute )
            airlineRouteWayPoints = AirlineRouteWayPoints.objects.filter(Route=airlineRoute).order_by('Order')
            for airlineRouteWayPoint in airlineRouteWayPoints:
                wayPoint = WayPoint.objects.filter(WayPointName = airlineRouteWayPoint.WayPoint).first()
                if wayPoint:
                    routeWayPointsList.append({
                            "name" : wayPoint.WayPointName ,
                            "Longitude": wayPoint.Longitude,
                            "Latitude": wayPoint.Latitude
                            })

    return JsonResponse({'departureAirport': getAirport(departureAirportICAOcode),
                         'arrivalAirport': getAirport(arrivalAirportICAOcode),
                         'waypoints': routeWayPointsList})
