
from xml.dom import minidom
import logging
logger = logging.getLogger(__name__)
import xmltodict

from django.template import loader
from django.core import serializers
from django.http import HttpResponse , JsonResponse

from airline.models import AirlineRoute, AirlineAircraft, Airline,    AirlineRouteWayPoints
from trajectory.models import AirlineWayPoint, AirlineAirport
from trajectory.models import BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.Guidance.FlightPathFile import FlightPath

from trajectory.views.utils import  getAirlineAircraftsFromDB, getAirlineRoutesFromDB,\
    getRouteFromRequest, getAircraftFromRequest


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

    
def getPlaceMarks(XmlDocument):
    placeMarksList = []
    #print ( BASE_DIR )
    #filePath = os.path.join ( BASE_DIR , os.path.join ( "trajectory/static/kml"  , fileName ) )
    
    parseXml = minidom.parseString(XmlDocument)
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
   
    logging.info ( "length place marks = {0}".format(len ( placeMarksList )) )
    return placeMarksList
    

    
def getWayPointsFromDB(viewExtent, airlineName):
    wayPointsList = []
    airline = Airline.objects.filter(Name=airlineName).first()
    if (airline):
        for airlineRoute in AirlineRoute.objects.filter(airline=airline):
            
            #print ( "best departure runway = {0}".format( airlineRoute.computeBestDepartureRunWay() ) )
            #print ( "best arrival runway = {0}".format( airlineRoute.computeBestArrivalRunWay() ) )
            
            for airlineRouteWayPoints in AirlineRouteWayPoints.objects.filter(Route = airlineRoute):
                wayPointName = airlineRouteWayPoints.WayPoint
                #print ( wayPointName )
                wayPoint = AirlineWayPoint.objects.filter(WayPointName = wayPointName).first()
                if wayPoint:
                    #print (wayPoint.WayPointName)
                    '''
                    if waypoint.Latitude >= viewExtent["minlatitude"] and \
                        waypoint.Latitude <= viewExtent["maxlatitude"] and \
                        waypoint.Longitude >= viewExtent["minlongitude"] and \
                        waypoint.Longitude <= viewExtent["maxlongitude"] :
                    '''
                    wayPointsList.append({
                            "name" : wayPoint.WayPointName ,
                            "Longitude": wayPoint.Longitude,
                            "Latitude": wayPoint.Latitude
                            } )
    #print ( "length of waypoints list = {0}".format(len(wayPointsList)))
    return wayPointsList
    

def getWayPoints(request, airlineName):
    logger.debug ("get WayPoints")
    if (request.method == 'GET'):
        logger.debug("get request received - WayPoints")
        try:
            viewExtent = {
               "minlatitude" : int(request.GET['minlatitude']),
               "maxlatitude" : int(request.GET['maxlatitude']),
               "minlongitude" : int(request.GET['minlongitude']),
               "maxlongitude" : int(request.GET['maxlongitude'])
            }
            logger.debug(viewExtent)
            #print ( viewExtent )
            waypoints = getWayPointsFromDB(viewExtent, airlineName)
            response_data = {'waypoints': waypoints}
            return JsonResponse(response_data)
        except:
            response_data = { "errors" : "Expecting a GET - min max latitude & longitude = {0}".format(request.method)}
            return JsonResponse(response_data)
    
    else:
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
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
    ''' purpose is only to fill the window with the selection to be made '''
    logger.debug ("launch Flight Profile")
    if (request.method == 'GET'):
        airlineAircraftsList = getAirlineAircraftsFromDB()
        airlineRoutesList = getAirlineRoutesFromDB()
        response_data = {
            'airlineAircrafts': airlineAircraftsList,
            'airlineRoutes': airlineRoutesList}
        return JsonResponse(response_data)
    
    
def getAirport(airportICAOcode):
    for airport in AirlineAirport.objects.all():
        if (airport.AirportICAOcode == airportICAOcode ):
            return { "AirportICAOcode" : airport.AirportICAOcode ,
                     "AirportName"     : airport.AirportName,
                     "Longitude"       : airport.Longitude,
                     "Latitude"        : airport.Latitude         }
    return {}
    
    
def computeFlightProfile(request):
    
    logger.setLevel(logging.DEBUG)
    logger.debug ("compute Flight Profile")
    
    #routeWayPointsList = []
    if (request.method == 'GET'):
        aircraftICAOcode = getAircraftFromRequest(request)
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):

            logger.debug ("selected aircraft = {0}".format( aircraftICAOcode ) )
            
            airlineRoute = getRouteFromRequest(request)
                        
            logger.debug ( "airport = {0}".format( str(airlineRoute).split("-")[0] ) )
            logger.debug ( str(airlineRoute).split("-")[1] )
            
            departureAirportICAOcode = str(airlineRoute).split("-")[0]
            arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
            airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode = departureAirportICAOcode, ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
            
            if (airlineRoute):
                #print ( airlineRoute )
                routeAsString = airlineRoute.getRouteAsString(AdepRunWayName = None, AdesRunWayName = None, direct = False)
                logger.debug ( routeAsString )
                acPerformance = AircraftJsonPerformance(badaAircraft.getAircraftPerformanceFile())
                if acPerformance.read():
                    logger.debug ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                    logger.debug ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
    
                    flightPath = FlightPath(
                                    route = routeAsString, 
                                    aircraftICAOcode = aircraftICAOcode,
                                    RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet() / 100., 
                                    cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                    takeOffMassKilograms = acPerformance.getMaximumMassKilograms())
    
                    flightPath.computeFlight(deltaTimeSeconds = 1.0)
        
                    logger.debug ( "=========== Flight Plan create output files  =========== " )
                    csvAltitudeMSLTimeGroundTrack = flightPath.createCsvAltitudeTimeProfile()
        
                    kmlXmlDocument = flightPath.createKmlXmlDocument()
                    if ( kmlXmlDocument and csvAltitudeMSLTimeGroundTrack):
                        logger.debug ( "=========== Flight Plan end  =========== "  )
                                            
                        response_data = {
                                    'kmlXMLjson': xmltodict.parse( kmlXmlDocument ),
                                    'placeMarks' : getPlaceMarks(kmlXmlDocument) ,
                                    'csvAltitudeMSLtime' : csvAltitudeMSLTimeGroundTrack
                                    }
                        return JsonResponse(response_data)
                    else:
                        logger.debug ('Error while retrieving the KML document')
                        response_data = {
                        'errors' : 'Error while retrieving the KML document'}
                        return JsonResponse(response_data)
                else:
                        logger.debug ('Error while reading Aircraft Performance file = {0}'.format(badaAircraft.getAircraftPerformanceFile()))
                        response_data = {
                        'errors' : 'Error while reading Aircraft Performance file = {0}'.format(badaAircraft.getAircraftPerformanceFile())}
                        return JsonResponse(response_data)

            else:
                logger.debug ('airline route not found = {0}'.format(airlineRoute))
                response_data = {
                'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
                return JsonResponse(response_data)
                
        else:
            logger.debug ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
            logger.debug ("or aircraft performance file = {0} not found".format(badaAircraft))
            response_data = {
                'errors' : 'Aircraft performance file {0} not found - please select another aircraft'.format(aircraftICAOcode)}
            return JsonResponse(response_data)
            
    else:
        return JsonResponse({'errors': "expecting GET method"})
