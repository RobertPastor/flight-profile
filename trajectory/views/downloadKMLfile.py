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

from xlsxwriter import Workbook
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse


from airline.models import Airline, AirlineRoute, AirlineAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.Guidance.FlightPathFile import FlightPath

from trajectory.models import BadaSynonymAircraft


@csrf_protect
def createKMLfile(request, airlineName):
    
    ''' this is the main view entry '''
    locale.setlocale(locale.LC_TIME, French_Locale)
    
    logger.setLevel(logging.DEBUG)
    logging.info ("compute Flight Profile - for airline = {0}".format(airlineName))
    
    if request.method == 'GET':
        
        aircraftICAOcode = request.GET['ac']
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            
            badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
            if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
                
                logger.debug ("selected aircraft = {0}".format( aircraftICAOcode ) )
            
                airlineRoute = request.GET['route']
                
                logger.debug(airlineRoute)
                
                logger.debug ( str(airlineRoute).split("-")[0] )
                logger.debug ( str(airlineRoute).split("-")[1] )
                
                departureAirportICAOcode = str(airlineRoute).split("-")[0]
                departureAirportRunWayName = request.GET['adepRwy']
                
                arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
                arrivalAirportRunWayName = request.GET['adesRwy']
                
                takeOffMassKg = request.GET['mass']
                logger.debug( "takeOff mass Kg = {0}".format( takeOffMassKg ) )
                cruiseFLfeet = request.GET['fl'] 
                logger.debug( "cruise FL feet = {0}".format( cruiseFLfeet ) )
                
                airlineRoute = AirlineRoute.objects.filter(airline = airline, DepartureAirportICAOCode = departureAirportICAOcode, ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
                if (airlineRoute):
                        logger.debug ( airlineRoute )
                        '''  use run-ways defined in the web page '''
                        routeAsString = airlineRoute.getRouteAsString(departureAirportRunWayName, arrivalAirportRunWayName)
                        logger.debug ( routeAsString )
                        acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
        
                        flightPath = FlightPath(
                                        route = routeAsString, 
                                        aircraftICAOcode = aircraftICAOcode,
                                        RequestedFlightLevel = float ( cruiseFLfeet ) / 100., 
                                        cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                        takeOffMassKilograms = float(takeOffMassKg)  )

                        ret = flightPath.computeFlight(deltaTimeSeconds = 1.0)
                        
                        if ret:
                            
                            logger.debug ( "=========== Flight Plan create output files  =========== " )
                
                            ''' Robert - python2 to python 3 '''
                            memoryFile = io.StringIO()
                            
                            ''' create State vector output sheet using an existing workbook '''
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
                        logger.debug ('airline route not found = {0}'.format(airlineRoute))
                        response_data = {
                            'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
                        return JsonResponse(response_data)                                                                   
            else:
                logger.debug ('bada aircraft not found = {0}'.format(airlineRoute))
                response_data = {
                            'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
                return JsonResponse(response_data)   
             
        else:
            logger.debug ('airline  not found = {0}'.format(airlineName))
            response_data = {
                        'errors' : 'Airline not found = {0}'.format(airlineName)}
            return JsonResponse(response_data)

    else:
            logger.debug ('expecting a GET - received something else = {0}'.format(request.method))
            response_data = {
                        'errors' : 'expecting a GET - received something else = {0}'.format(request.method)}
            return JsonResponse(response_data)
