'''
Created on 24 déc. 2023

@author: robert
https://en.wikipedia.org/wiki/Fuel_economy_in_aircraft 

'''

import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse

import io
from xlsxwriter import Workbook
from datetime import datetime 
from django.shortcuts import HttpResponse

from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute
from trajectory.Environment.Constants import KeroseneKilogram2Liter


Headers = ['airline' , 'aircraft' , 'nbPassengers' , 'departureAirport' , 'adepRunway' , 'arrivalAirport' ,  'adesRunway' ,  
                'isAborted' , 'takeOffMassKg'  ,  'finalMassKg' , 'massLossKg' , 'KeroseneLiter' , 'LegLenghtKiloMeters' , 'FuelEfficiencyLitersPerHundredKMPerPassenger']

def writeReadMe(workbook, airlineName):

    wsReadMe = workbook.add_worksheet("ReadMe")
    styleEntete = workbook.add_format({'bold': False, 'border':True})
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    row = 0
    wsReadMe.write(row, 0 , "Airline Services", styleLavender)
    wsReadMe.write(row, 1 , "Airline Fuel Efficiency", styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Airline", styleLavender)
    wsReadMe.write(row, 1 , airlineName, styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Date", styleLavender)
    wsReadMe.write(row, 1 , datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") , styleEntete)
    
    ''' Autofit the worksheet - adjust column width '''
    wsReadMe.autofit()
    return row, wsReadMe


def writeHeaders(worksheet, style, headers):
    row = 0
    col = 0
    for header in headers:
        worksheet.write(row, col , header , style)
        col = col + 1
        

def writeAirlineFuelEfficiency(workbook, airlineName):
    worksheet = workbook.add_worksheet("Airline Fuel Efficiency")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    writeHeaders(worksheet, styleLavender , Headers)
    
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
            
        row  = 1
        for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
            for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                
                for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):    
                    
                    ColumnIndex = 0
                    worksheet.write(row, ColumnIndex, airlineName)
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineAircraft.getAircraftFullName())
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineAircraft.getMaximumNumberOfPassengers())
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineRoute.getDepartureAirportICAOcode())
                    
                    ''' 29th April 2023 add cruise level and adep . Ades runways '''
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.adepRunway )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineRoute.getArrivalAirportICAOcode())
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.adesRunway )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, str(airlineCosts.isAborted) )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.initialTakeOffMassKg )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.finalMassKg )
                    
                    massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, massLossKg )
                    
                    keroseneLiters = massLossKg * KeroseneKilogram2Liter
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, keroseneLiters )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.getFlightLegLengthMeters() / 1000.0 )
                    
                    fuelEfficiencyLiterPer100KmPerPassenger = (( keroseneLiters / ( airlineCosts.getFlightLegLengthMeters() / 1000.0 ) ) / airlineAircraft.getMaximumNumberOfPassengers()) * 100.
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, fuelEfficiencyLiterPer100KmPerPassenger )
                    
                    row = row + 1
                    
        worksheet.autofit()
    else:
        logger.debug ("Error - airline = {0} not found".format( airlineName ) )


def createExcelWorkbook(memoryFile, request, airlineName):
    ''' create the EXCEL workbook '''
    wb = Workbook(memoryFile)
    ''' write the ReadMe sheet '''
    row , wsReadMe = writeReadMe(workbook=wb, airlineName=airlineName)
    
    ''' write the airline results '''
    writeAirlineFuelEfficiency(workbook=wb , airlineName=airlineName)
    
    return wb

def getAirlineFuelEfficiencyXlsx(request, airlineName):
    pass
    if (request.method == 'GET'):
    
        ''' Robert - python2 to python 3 '''
        memoryFile = io.BytesIO() # create a file-like object 
                    
        # warning : we get strings from the URL query
        wb = createExcelWorkbook(memoryFile, request, airlineName)
        wb.close()
                            
        filename = 'AirlineFuelEfficiency-{}.xlsx'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                            
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
    
    