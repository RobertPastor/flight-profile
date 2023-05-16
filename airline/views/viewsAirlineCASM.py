'''
Created on 4 mars 2023

@author: robert
'''

import logging
logger = logging.getLogger(__name__)

from django.http import  JsonResponse

import io
from xlsxwriter import Workbook
from datetime import datetime 
from django.shortcuts import HttpResponse

from airline.models import Airline
from airline.models import AirlineCosts, AirlineAircraft, AirlineRoute

from trajectory.Environment.Constants import kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars
from trajectory.Environment.Constants import Meter2NauticalMiles


headers = [ 'Airline' , 'Aircraft' , 'Departure', 'Arrival', 'Is Aborted', 'nb Seats' , 'leg length miles' , 'totalCostsUS$' , 'Costs per Available Seat Mile US$' ]

def writeReadMe(workbook, request, airlineName):

    wsReadMe = workbook.add_worksheet("ReadMe")
    styleEntete = workbook.add_format({'bold': False, 'border':True})
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    row = 0
    wsReadMe.write(row, 0 , "Airline Services", styleLavender)
    wsReadMe.write(row, 1 , "Airline CASM costs", styleEntete)
    
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
    
    
def writeAirlineCasmResults(workbook , airlineName):
    
    worksheet = workbook.add_worksheet("Airline CASM Costs")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    writeHeaders(worksheet, styleLavender)
    
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
        
        row  = 1
        for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
            nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                    
            for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                
                for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):    
                            
                    massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                    fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                
                    operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                                
                    crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                    totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars     
                        
                    ''' 5th February 2023 - Costs per Available Seat Mile '''
                    miles = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                    seatsPerMiles = nbSeats * miles
                    casmUSdollars = totalCostsUSdollars / seatsPerMiles
                    
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
                    worksheet.write(row, ColumnIndex, (nbSeats) )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, (miles) )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, (totalCostsUSdollars) )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, (casmUSdollars) )
                    
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
    writeAirlineCasmResults(workbook=wb , airlineName=airlineName)
    return wb


def getAirlineCasmXlsx(request, airlineName):

    logger.setLevel(logging.INFO)
    logger.info ("retrieve Airline CASM as Xlsx file")        
        
    if (request.method == 'GET'):
        
        ''' Robert - python2 to python 3 '''
        memoryFile = io.BytesIO() # create a file-like object 
                    
        # warning : we get strings from the URL query
        wb = createExcelWorkbook(memoryFile, request, airlineName)
        wb.close()
                            
        filename = 'AirlineCasmCosts-{}.xlsx'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                            
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
    

def getAirlineCASM(request, airlineName):
    
    logger.setLevel(logging.INFO)
    logger.info ("views Airline CASM")
    
    airlineCostsList = []

    if (request.method == 'GET'):
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            pass
        
            for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
                nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                    
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                
                    for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):    
                            
                        massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                        fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                
                        operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                                
                        crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                        totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars     
                        
                        ''' 5th February 2023 - Costs per Available Seat Mile '''
                        miles = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                        seatsPerMiles = nbSeats * miles
                        casmUSdollars = totalCostsUSdollars / seatsPerMiles
                            
                        airlineCostsDict = {
                                'airline'                   : airlineName,
                                'airlineAircraft'           : airlineAircraft.aircraftFullName,
                                'departureAirport'          : airlineRoute.DepartureAirport,
                                'arrivalAirport'            : airlineRoute.ArrivalAirport,
                                'isAborted'                 : str(airlineCosts.isAborted) ,
                                'takeOffMassKg'             : round ( airlineCosts.initialTakeOffMassKg , 1),
                                'finalMassKg'               : round ( airlineCosts.finalMassKg , 1),
                                'flightDurationHours'        : round ( ( float(airlineCosts.flightDurationSeconds ) / 3600.0 ), 4 ),
                                'fuelCostsUSdollars'         : round ( fuelCostsUSdollars , 2),
                                'operationalCostsUSdollars'  : round ( operationalFlyingCostsUSdollars , 2),
                                'crewCostsUSdollars'         : round ( crewCostsUSdollars , 2),
                                'totalCostsUSdollars'        : round ( totalCostsUSdollars , 2),
                                'nbSeats'                    : round ( nbSeats , 2),
                                'miles'                      : round ( miles , 2),
                                'CasmUSdollars'              : round ( casmUSdollars , 4 )
                                            }
                        airlineCostsList.append(airlineCostsDict)
                            
            return JsonResponse({'airlineCasmList': airlineCostsList})
        else:
            return JsonResponse({'errors': "unknown airline {0}".format(airlineName)})
    else:
        return JsonResponse({'errors': "expecting GET method"})