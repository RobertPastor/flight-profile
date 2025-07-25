'''
Created on 24 juin 2023

@author: robert

'''


import locale
#import StringIO
import io

import logging
logger = logging.getLogger(__name__)

French_Locale = ""
from datetime import datetime 

from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse


from airline.models import Airline, AirlineRoute
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.Guidance.FlightPathFile import FlightPath

from trajectory.models import BadaSynonymAircraft
from trajectory.views.utils import getAircraftFromRequest, getRouteFromRequest, getAdepRunwayFromRequest, getAdesRunwayFromRequest
from trajectory.views.utils import getMassFromRequest, getFlightLevelFromRequest, getReducedClimbPowerCoeffFromRequest, getDirectRouteFromRequest

from trajectory.Environment.Earth import Earth
from trajectory.Environment.Atmosphere import Atmosphere

from trajectory.GuidanceOpenap.FlightPathOpenapFile import FlightPathOpenap
from trajectory.Openap.AircraftMainFile import OpenapAircraft


def createBadaKMLfile( request, airline ):
            aircraftICAOcode = getAircraftFromRequest(request)
            badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
            if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
                            
                airlineRoute = getRouteFromRequest(request)
                                                
                departureAirportICAOcode = str(airlineRoute).split("-")[0]
                departureAirportRunWayName = getAdepRunwayFromRequest(request)
                
                arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
                arrivalAirportRunWayName = getAdesRunwayFromRequest(request)
                
                takeOffMassKg = getMassFromRequest(request)
                cruiseFLfeet = getFlightLevelFromRequest(request)
                ''' 10th August 2023 - Reduced Climb Power % '''
                reducedClimbPowerCoeff = 0.0
                try:
                    reducedClimbPowerCoeff = float(getReducedClimbPowerCoeffFromRequest(request))
                except:
                    reducedClimbPowerCoeff = 0.0
                    
                ''' 1st April 2024 - checkbox to fly direct route '''
                direct = getDirectRouteFromRequest(request)
                
                airlineRoute = AirlineRoute.objects.filter(airline = airline, DepartureAirportICAOCode = departureAirportICAOcode, ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
                if (airlineRoute):
                    '''  use run-ways defined in the web page '''
                    routeAsString = airlineRoute.getRouteAsString(AdepRunWayName=departureAirportRunWayName, AdesRunWayName=arrivalAirportRunWayName, direct=direct)
                    acPerformance = AircraftJsonPerformance(aircraftICAOcode, badaAircraft.getAircraftPerformanceFile())
                    if ( acPerformance.read() ):
                        flightPath = FlightPath(
                                            route = routeAsString, 
                                            aircraftICAOcode = aircraftICAOcode,
                                            RequestedFlightLevel = float ( cruiseFLfeet ) / 100., 
                                            cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                            takeOffMassKilograms = float(takeOffMassKg)  ,
                                            reducedClimbPowerCoeff = float(reducedClimbPowerCoeff) )
                        ret = flightPath.computeFlight(deltaTimeSeconds = 1.0)
                        if ret:
                            logger.debug ( "=========== Flight Plan create output files  =========== " )
                    
                            ''' Robert - python2 to python 3 '''
                            memoryFile = io.StringIO()
                                
                            ''' create KML byte like file '''
                            flightPath.createKMLfileLike(memoryFile)
                        
                            filename = 'KMLfile-{}.kml'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                            #print filename
                                
                            response = HttpResponse( memoryFile.getvalue() )
                            response['Content-Type'] = 'text/xml, application/xml; charset=utf-8'
                            #response['Content-Type'] = 'application/vnd.ms-excel'
                            response["Content-Transfer-Encoding"] = "binary"
                            response['Set-Cookie'] = 'fileDownload=true; path=/'
                            response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=filename)
                            response['Content-Length'] = memoryFile.tell()
                            return response
                        else:
                            response_data = {'errors' : 'Trajectory computation failed '}
                            return JsonResponse(response_data)
                    else:
                        response_data = {
                            'errors' : 'Aircraft Performance read failed = {0}'.format(badaAircraft.getAircraftPerformanceFile())}
                        return JsonResponse(response_data)   
                else:
                    logger.error('airline route not found = {0}'.format(airlineRoute))
                    response_data = {'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
                    return JsonResponse(response_data)                                                                   
            else:
                logger.debug ('bada aircraft not found = {0}'.format(airlineRoute))
                response_data = { 'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
                return JsonResponse(response_data)   

def createWrapKMLfile( request , airline ):
    pass

    aircraftICAOcode = getAircraftFromRequest(request).lower()
    logging.info( aircraftICAOcode )
    
    earth = Earth()
    atmosphere = Atmosphere()

    ac = OpenapAircraft( aircraftICAOcode , earth , atmosphere , initialMassKilograms = None)
    logging.info( ac.getAircraftName())
    
    airlineRoute = getRouteFromRequest(request)
    logging.info( airlineRoute )
                                    
    departureAirportICAOcode = str(airlineRoute).split("-")[0]
    departureAirportRunWayName = getAdepRunwayFromRequest(request)
            
    arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
    arrivalAirportRunWayName = getAdesRunwayFromRequest(request)
            
    takeOffMassKg = getMassFromRequest(request)
    cruiseFlightLevel = float ( getFlightLevelFromRequest(request) ) / 100.0
    
    targetCruiseMach = ac.getMaximumSpeedMmoMach()
    logging.info( "target cruise mach = {0:.2f} ".format( targetCruiseMach ) )
    
    airlineRoute = AirlineRoute.objects.filter(airline = airline, DepartureAirportICAOCode = departureAirportICAOcode, ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
    if (airlineRoute):
        logger.debug( airlineRoute )
        
        ''' 1st April 2024 - checkbox to fly direct route '''
        direct = getDirectRouteFromRequest(request)
        
        '''  use run-ways defined in the page '''
        routeAsString = airlineRoute.getRouteAsString(AdepRunWayName = departureAirportRunWayName, AdesRunWayName = arrivalAirportRunWayName, direct=direct)

        ''' try with direct route '''
        logging.info ( "Trajectory Compute Wrap - " + routeAsString )
                    
        flightPath = FlightPathOpenap(
                        route                = routeAsString, 
                        aircraftICAOcode     = aircraftICAOcode.lower(),
                        RequestedFlightLevel = float(cruiseFlightLevel), 
                        cruiseMach           = float(targetCruiseMach), 
                        takeOffMassKilograms = float(takeOffMassKg) )
        try:
            ret = flightPath.computeFlight(deltaTimeSeconds = 1.0)
            if ret:
                    ''' Robert - python2 to python 3 '''
                    memoryFile = io.StringIO()
                    
                    ''' create KML byte like file '''
                    flightPath.createKMLfileLike(memoryFile)
                    
                    filename = 'KMLfile-{}.kml'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                    #print filename
                                
                    response = HttpResponse( memoryFile.getvalue() )
                    response['Content-Type'] = 'text/xml, application/xml; charset=utf-8'
                    #response['Content-Type'] = 'application/vnd.ms-excel'
                    response["Content-Transfer-Encoding"] = "binary"
                    response['Set-Cookie'] = 'fileDownload=true; path=/'
                    response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=filename)
                    response['Content-Length'] = memoryFile.tell()
                    return response
            else:
                response_data = {'errors' : 'Trajectory computation failed '}
                return JsonResponse(response_data)
        
        except Exception as e:
            logging.error("Trajectory Compute Wrap - Exception = {0}".format( str(e ) ) )
            response_data = {'errors' : 'Trajectory computation failed '}
            return JsonResponse(response_data)

                
    else:
        logger.error('airline route not found = {0}'.format(airlineRoute))
        response_data = {'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
        return JsonResponse(response_data)       


@csrf_protect
def createKMLfile(request, airlineName , BadaWrap ):
    ''' @TODO same inputs as compute profile , compute costs and compute state vector  '''
    ''' this is the main view entry '''
    locale.setlocale(locale.LC_TIME, French_Locale)
    
    logger.setLevel(logging.DEBUG)
    logging.info ("Download KML - compute KML Profile - for airline = {0}".format(airlineName))
    
    if request.method == 'GET':
        
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            
            if BadaWrap == "BADA":
                return createBadaKMLfile( request, airline )
            else:
                return createWrapKMLfile( request , airline )
 
        else:
            logger.debug ('airline not found = {0}'.format(airlineName))
            response_data = { 'errors' : 'Airline not found = {0}'.format(airlineName)}
            return JsonResponse(response_data)
    else:
        logger.debug ('expecting a GET - received something else = {0}'.format(request.method))
        response_data = {'errors' : 'expecting a GET - received something else = {0}'.format(request.method)}
        return JsonResponse(response_data)
