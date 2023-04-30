'''
Created on 28 janv. 2023

@author: robert
'''

import logging
logger = logging.getLogger(__name__)

import io
from xlsxwriter import Workbook
from datetime import datetime 
from django.shortcuts import HttpResponse

from django.http import  JsonResponse
from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute

from trajectory.Environment.Constants import kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars

''' 29th April 2023 add cruise level and adep . Ades runways '''
headers = ['airline' , 'aircraft'  , 'departureAirport' , 'arrivalAirport' , 'isAborted' , 'takeOffMassKg'  , 'cruiseLevelFeet' , 'adepRunway' , 'adesRunway' , 'finalMassKg' \
              , 'flightDurationHours' , 'fuelCostsUSdollars' , 'operationalCostsUSdollars' , 'crewCostsUSdollars' , 'totalCostsUSdollars' ]       

def writeReadMe(workbook, request, airlineName):

    wsReadMe = workbook.add_worksheet("ReadMe")
    styleEntete = workbook.add_format({'bold': False, 'border':True})
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    row = 0
    wsReadMe.write(row, 0 , "Airline Services", styleLavender)
    wsReadMe.write(row, 1 , "Airline Costs", styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Airline", styleLavender)
    wsReadMe.write(row, 1 , airlineName, styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Date", styleLavender)
    wsReadMe.write(row, 1 , datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") , styleEntete)
    
    ''' set width of each column '''
    wsReadMe.set_column(0 , 1 , len("Airline Services"))
    
    # Autofit the worksheet.
    wsReadMe.autofit()
    
    
def writeHeaders(worksheet, style):
    row = 0
    col = 0
    for header in headers:
        worksheet.write(row, col , header , style)
        col = col + 1
   
    
def writeAirlineCostsResults(workbook , airlineName):
    
    worksheet = workbook.add_worksheet("AirlineCosts")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    writeHeaders(worksheet, styleLavender)
    
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
            
        row  = 1
        for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
            for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                
                for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):    
                        
                    massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                    fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                            
                    operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                            
                    crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                    totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars    
                    
                    ColumnIndex = 0
                    worksheet.write(row, ColumnIndex, airlineName)   
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineAircraft.getAircraftFullName())
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineRoute.getDepartureAirportICAOcode())
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineRoute.getArrivalAirportICAOcode())
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, str(airlineCosts.isAborted) )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.initialTakeOffMassKg )
                    
                    ''' 29th April 2023 add cruise level and adep . Ades runways '''
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.targetCruiseLevelFeet )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.adepRunway )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.adesRunway )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.finalMassKg )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.flightDurationSeconds / 3600.0 )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, fuelCostsUSdollars )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, operationalFlyingCostsUSdollars )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, crewCostsUSdollars )
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, totalCostsUSdollars )
                    
                    row = row + 1
                    
        worksheet.autofit()
    else:
        print ( "airline not found")
    
def createExcelWorkbook(memoryFile, request, airlineName):
    ''' create the EXCEL workbook '''
    wb = Workbook(memoryFile)
    ''' write the readme sheet '''
    writeReadMe(workbook=wb, request=request, airlineName=airlineName)
    ''' write the costs results '''
    writeAirlineCostsResults(workbook=wb , airlineName=airlineName)
    return wb


def getAirlineCostsAsXlsx(request, airlineName):
    
    if (request.method == 'GET'):
        
        ''' Robert - python2 to python 3 '''
        memoryFile = io.BytesIO() # create a file-like object 
                    
        # warning : we get strings from the URL query
        wb = createExcelWorkbook(memoryFile, request, airlineName)
        wb.close()
                            
        filename = 'AirlineCosts-{}.xlsx'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                            
        response = HttpResponse( memoryFile.getvalue() )
        response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet; charset=utf-8'
        #response['Content-Type'] = 'application/vnd.ms-excel'
        response["Content-Transfer-Encoding"] = "binary"
        response['Set-Cookie'] = 'fileDownload=true; path=/'
        response['Content-Disposition'] = 'attachment; filename={filename}'.format(filename=filename)
        response['Content-Length'] = memoryFile.tell()
        return response         
        
    else:
        return JsonResponse({'errors': "expecting GET method"})
        

def getAirlineCosts(request, airlineName):
    logger.setLevel(logging.INFO)
    logger.info ("views Airline Costs")
    
    airlineCostsList = []
    if (request.method == 'GET'):
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            
            for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
            
                    for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):    
                        
                        massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                        fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                            
                        operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                            
                        crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                        totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars            
                        
                        airlineCostsDict = {
                            'airline'          : airlineName,
                            'airlineAircraft'  : airlineAircraft.aircraftFullName,
                            'departureAirport' : airlineRoute.DepartureAirport,
                            'arrivalAirport'   : airlineRoute.ArrivalAirport,
                            'isAborted'        : str(airlineCosts.isAborted) ,
                            'takeOffMassKg'    : round ( airlineCosts.initialTakeOffMassKg , 1),
                            'finalMassKg'      : round ( airlineCosts.finalMassKg , 1),
                            'flightDurationHours'        : round ( ( float(airlineCosts.flightDurationSeconds ) / 3600.0 ), 4 ),
                            'fuelCostsUSdollars'         : round ( fuelCostsUSdollars , 2),
                            'operationalCostsUSdollars'  : round ( operationalFlyingCostsUSdollars , 2),
                            'crewCostsUSdollars'         : round ( crewCostsUSdollars , 2),
                            'totalCostsUSdollars'        : round ( totalCostsUSdollars , 2)
                                        }
                        airlineCostsList.append(airlineCostsDict)
                        
            return JsonResponse({'airlineCostsList': airlineCostsList})
        else:
            return JsonResponse({'errors': "unknown airline {0}".format(airlineName)})
    else:
        return JsonResponse({'errors': "expecting GET method"})
    