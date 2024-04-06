'''
Created on 26 déc. 2022

donwload vertical profile as an EXCEL file

@author: robert
'''

import locale
import io

import logging
from trajectory.views.utils import getRouteFromRequest
logger = logging.getLogger(__name__)

French_Locale = ""
from datetime import datetime 

from xlsxwriter import Workbook
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_protect
from django.http import JsonResponse


from airline.models import Airline, AirlineRoute, AirlineAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.Guidance.FlightPathFile import FlightPath
from trajectory.models import AirlineAirport

from trajectory.models import BadaSynonymAircraft
from trajectory.views.utils import getAircraftFromRequest, getRouteFromRequest, getAdepRunwayFromRequest, getAdesRunwayFromRequest , getMassFromRequest, getFlightLevelFromRequest
from trajectory.views.utils import getReducedClimbPowerCoeffFromRequest , getDirectRouteFromRequest

def writeReadMeRow(worksheet, row, headerStr , styleHeader, dataStr,  styleData):
    worksheet.write(row, 0 , headerStr, styleHeader)
    worksheet.write(row, 1 , dataStr, styleData)
    

def writeReadMe(workbook, request, airlineName):

    wsReadMe = workbook.add_worksheet("ReadMe")
    styleEntete = workbook.add_format({'bold': False, 'border':True})
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    row = 0
    writeReadMeRow(wsReadMe, row, "Airline Services" , styleLavender , "Vertical Flight Profile", styleEntete)
    
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Airline" , styleLavender , airlineName, styleEntete)

    row = row + 1
    writeReadMeRow(wsReadMe, row, "Aircraft ICAO code" , styleLavender , getAircraftFromRequest(request) , styleEntete)
    
    aircraft = AirlineAircraft.objects.all().filter(aircraftICAOcode=getAircraftFromRequest(request) ).first()
    if ( aircraft ):
        row = row + 1
        writeReadMeRow(wsReadMe, row, "Aircraft" , styleLavender , aircraft.getAircraftFullName() , styleEntete)
    
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Departure Airport ICAO code" , styleLavender , str(getRouteFromRequest(request)).split("-")[0] , styleEntete)
    
    airport = AirlineAirport.objects.filter(AirportICAOcode = str(getRouteFromRequest(request)).split("-")[0]).first()
    if airport:
        row = row + 1
        writeReadMeRow(wsReadMe, row, "Departure Airport" , styleLavender , airport.getAirportName() , styleEntete)
        
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Departure Airport Runway" , styleLavender , getAdepRunwayFromRequest(request) , styleEntete)

    row = row + 1
    writeReadMeRow(wsReadMe, row, "Arrival Airport ICAO code" , styleLavender , str(getRouteFromRequest(request)).split("-")[1] , styleEntete)
    
    airport = AirlineAirport.objects.filter(AirportICAOcode = str(getRouteFromRequest(request)).split("-")[1]).first()
    if airport:
        row = row + 1
        writeReadMeRow(wsReadMe, row, "Arrival Airport" , styleLavender , airport.getAirportName() , styleEntete)
    
    row = row + 1
    writeReadMeRow(wsReadMe, row, "Arrival Airport Runway" , styleLavender , getAdesRunwayFromRequest(request) , styleEntete)

    row = row + 1
    writeReadMeRow(wsReadMe, row, "TakeOff Mass (kg)" , styleLavender , getMassFromRequest(request) , styleEntete)

    row = row + 1
    writeReadMeRow(wsReadMe, row, "Cruise Flight Level (feet)" , styleLavender , getFlightLevelFromRequest(request) , styleEntete)

    row = row + 1
    writeReadMeRow(wsReadMe, row, "Reduced Climb Power Coefficient (%)" , styleLavender , getReducedClimbPowerCoeffFromRequest(request) , styleEntete)

    wsReadMe.autofit()

def createExcelWorkbook(memoryFile, request, airlineName):
    ''' create the EXCEL workbook '''
    ''' create the workbook '''
    wb = Workbook(memoryFile)
    ''' write the readme sheet '''
    writeReadMe(workbook=wb, request=request, airlineName=airlineName)
    return wb

@csrf_protect
def createExcelVerticalProfile(request, airlineName):
    ''' @TODO same inputs as compute profile , compute costs and compute state vector  '''
    ''' this is the main view entry '''
    locale.setlocale(locale.LC_TIME, French_Locale)
    
    logger.setLevel(logging.DEBUG)
    logger.info ("compute Flight Profile - for airline = {0}".format(airlineName))
    
    if request.method == 'GET':
        
        aircraftICAOcode = getAircraftFromRequest(request)
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            
            badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
            if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
                            
                airlineRoute = getRouteFromRequest(request)
                
                departureAirportICAOcode = str(airlineRoute).split("-")[0]
                departureAirportRunWayName = getAdepRunwayFromRequest(request)
                
                arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
                arrivalAirportRunWayName = getAdesRunwayFromRequest(request)
                
                takeOffMassKg = getMassFromRequest(request)
                cruiseFLfeet = getFlightLevelFromRequest(request) 
                
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
                        #logger.debug ( routeAsString )
                        acPerformance = AircraftJsonPerformance(aircraftICAOcode, badaAircraft.getAircraftPerformanceFile())
                        if ( acPerformance.read() ):
            
                            flightPath = FlightPath(
                                            route = routeAsString, 
                                            aircraftICAOcode = aircraftICAOcode,
                                            RequestedFlightLevel = float ( cruiseFLfeet ) / 100., 
                                            cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                            takeOffMassKilograms = float(takeOffMassKg) ,
                                            reducedClimbPowerCoeff = float(reducedClimbPowerCoeff) )
            
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
                    response_data = {'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
                    return JsonResponse(response_data)                                                                   
            else:
                logger.debug ('Aircraft not found = {0}'.format(badaAircraft))
                response_data = {'errors' : 'Aircraft not found= {0}'.format(badaAircraft)}
                return JsonResponse(response_data)   
             
        else:
            logger.debug ('airline  not found = {0}'.format(airlineName))
            response_data = {'errors' : 'Airline not found = {0}'.format(airlineName)}
            return JsonResponse(response_data)

    else:
            logger.debug ('expecting a GET - received something else = {0}'.format(request.method))
            response_data = {'errors' : 'expecting a GET - received something else = {0}'.format(request.method)}
            return JsonResponse(response_data)
