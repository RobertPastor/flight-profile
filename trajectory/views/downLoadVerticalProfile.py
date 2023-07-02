'''
Created on 26 déc. 2022

donwload vertical profile as an EXCEL file

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

def writeReadMe(workbook, request, airlineName):

    wsReadMe = workbook.add_worksheet("ReadMe")
    styleEntete = workbook.add_format({'bold': False, 'border':True})
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    row = 0
    wsReadMe.write(row, 0 , "Airline Services", styleLavender)
    wsReadMe.write(row, 1 , "Vertical Flight Profile", styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Airline", styleLavender)
    wsReadMe.write(row, 1 , airlineName, styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Aircraft ICAO code", styleLavender)
    wsReadMe.write(row, 1 , request.GET['ac'], styleEntete)
    
    aircraft = AirlineAircraft.objects.all().filter(aircraftICAOcode=request.GET['ac']).first()
    if ( aircraft ):
        row = row + 1
        wsReadMe.write(row, 0 , "Aircraft", styleLavender)
        wsReadMe.write(row, 1 , aircraft.getAircraftFullName(), styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Departure ICAO code", styleLavender)
    Adep = str(request.GET['route']).split("-")[0]
    wsReadMe.write(row, 1 , Adep, styleEntete)

    row = row + 1
    wsReadMe.write(row, 0 , "Destination ICAO code", styleLavender)
    Ades = str(request.GET['route']).split("-")[1]
    wsReadMe.write(row, 1 , Ades, styleEntete)

    row = row + 1
    wsReadMe.write(row, 0 , "Departure Runway", styleLavender)
    wsReadMe.write(row, 1 , request.GET['adepRwy'], styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Destination Runway", styleLavender)
    wsReadMe.write(row, 1 , request.GET['adesRwy'], styleEntete)
    
    ''' set width of each column '''
    wsReadMe.set_column(0 , 1 , len("Vertical Flight Profile"))
    

def createExcelWorkbook(memoryFile, request, airlineName):
    ''' create the EXCEL workbook '''
    ''' create the workbook '''
    wb = Workbook(memoryFile)
    ''' write the readme sheet '''
    writeReadMe(workbook=wb, request=request, airlineName=airlineName)
    return wb


@csrf_protect
def createExcelVerticalProfile(request, airlineName):
    
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
                        if ( acPerformance.read() ):
                            #logger.debug ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                            #logger.debug ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
            
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
                                memoryFile = io.BytesIO() # create a file-like object 
                        
                                # warning : we get strings from the URL query
                                wb = createExcelWorkbook(memoryFile, request, airlineName)
                                
                                ''' create State vector output sheet using an existing workbook '''
                                flightPath.createStateVectorOutputSheet(wb) 
                                wb.close()
                                
                                filename = 'VerticalProfile-{}.xlsx'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                                #print filename
                                
                                response = HttpResponse( memoryFile.getvalue() )
                                response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8'
                                #response['Content-Type'] = 'application/vnd.ms-excel'
                                response["Content-Transfer-Encoding"] = "binary"
                                response['Set-Cookie'] = 'fileDownload=true; path=/'
                                response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=filename)
                                response['Content-Length'] = memoryFile.tell()
                                return response    
                              
                            else:
                                response_data = {'errors' : 'Trajectory compute failed'}
                                return JsonResponse(response_data) 
                        else:
                            response_data = {'errors' : 'Aircraft Performance read failed - = {0}'.format(badaAircraft.getAircraftPerformanceFile())}
                            return JsonResponse(response_data) 
                        
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
