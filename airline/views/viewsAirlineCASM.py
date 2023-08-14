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

from pulp import LpProblem , LpMinimize ,  LpVariable, lpSum, LpStatus ,  PULP_CBC_CMD, value
from pulp.constants import LpBinary

from airline.models import Airline
from airline.models import AirlineCosts, AirlineAircraft, AirlineRoute
from airline.views.viewsAirlineCasmOptimization import computeAirlineCostsArray

from trajectory.Environment.Constants import Kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars
from trajectory.Environment.Constants import Meter2NauticalMiles

headersCASM = [ 'Airline' , 'Aircraft' , 'Departure', 'Arrival', 'Is Aborted', 'nb Seats' , 'leg length Nm' , 'total Costs US$' , 'Costs per Available Seat Mile US$' ]
headersCASMoptim = [ 'Airline' , 'Solver Status' , 'Aircraft' , 'Assigned' , 'Departure', 'Arrival', 'nb Seats' , 'leg length (nm)' , 'total Costs US$' , 'Costs per Available Seat Mile US$' ]


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
    
    # Autofit the worksheet.
    wsReadMe.autofit()
    return row, wsReadMe, styleLavender, styleEntete
    
    
def writeHeaders(worksheet, style, headers):
    row = 0
    col = 0
    for header in headers:
        worksheet.write(row, col , header , style)
        col = col + 1
    row = row + 1
    return row

    
def writeAirlineCasmResults(workbook , airlineName):
    
    worksheet = workbook.add_worksheet("Airline CASM Costs")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    row = writeHeaders(worksheet, styleLavender, headersCASM)
    
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
        
        for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
            nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                    
            for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                
                for airlineCosts in AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute):    
                            
                    massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                    fuelCostsUSdollars = massLossKg * Kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                
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
        logger.error ( " airline not found = {0}".format( airlineName ))
        ColumnIndex = 0
        worksheet.write(row, ColumnIndex, airlineName)
        

def writeAirlineCasmOptimizationResults(workbook , airlineName):
    
    worksheet = workbook.add_worksheet("Airline CASM Optimization")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    row = writeHeaders(worksheet, styleLavender, headersCASMoptim)
    
    value_prob_objective = 0.0
    
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
    
            ''' 27th May 2023 - unique function used by get EXCEL file and get JSON for display in an html table '''
            aircraftInstancesList , airlineFlightLegsList , airlineCasmArray = computeAirlineCostsArray(airline, airlineName)
            
            num_flight_legs = len( AirlineRoute.objects.filter(airline=airline) )
            logger.debug ( "num flight legs = {0}".format(num_flight_legs) )
            num_aircraft_instances = len(aircraftInstancesList)
            
            logger.debug ( "number of aircraft instances = {0}".format( num_aircraft_instances ) )
            num_flight_legs = len(airlineCasmArray[0])
            logger.debug ( "num flight legs = {0}".format(num_flight_legs) )

            ''' minimization problem '''
            prob = LpProblem("CASM-Problem", LpMinimize)
            
            ''' define the variables '''
            x_vars = {}
            #print ( range(num_aircrafts) )
            for i in range(num_aircraft_instances):
                #print ( "---> {0} - {1}".format( i , airlineAircraftICAOcodeList[i] ) )
                for j in range(num_flight_legs):
                    #print ( "------> {0} - {1}".format ( j , airlineFlightLegsList[j] ) )
                    #print ( '{0}-{1}'.format(airlineAircraftICAOcodeList[i], airlineFlightLegsList[j]) )
                    #x[i, j] = solver.IntVar(0, 1, '{0}-{1}'.format("A320", airlineFlightLegsList[j]))
                    pass
                    #x_vars = LpVariable("x_vars", lowBound=0, upBound=1, cat='Integer', e=None)
                    x_vars[i,j] = LpVariable(name="{0}-{1}".format(aircraftInstancesList[i], airlineFlightLegsList[j]), lowBound=0, upBound=1, cat=LpBinary)


            ''' define the objective function '''
            prob += lpSum( [ airlineCasmArray[i][j] * x_vars[i,j] for i in range(num_aircraft_instances) for j in range(num_flight_legs) ])

            logger.debug ( "--- add constraints ----")
            
            '''  Each aircraft is assigned to at most 1 flight leg. '''
            for i in range(num_aircraft_instances):
                pass
                #solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
                prob += lpSum( [ x_vars[i,j] for j in range(num_flight_legs) ] ) <= 1
                
            ''' Each flight leg is assigned to exactly one aircraft '''
            for j in range(num_flight_legs):
                pass
                prob += lpSum ( [ x_vars[i,j] for i in range(num_aircraft_instances) ] ) == 1
                #check_constraints(prob, c_list)
                
            ''' minimize the costs '''
            #solver.Minimize(solver.Sum(objective_terms))
            prob.solve(PULP_CBC_CMD(msg=0))
            logger.debug ("Status: {0}".format( str( LpStatus[prob.status] ) ) )
            
            for v in prob.variables():
                
                assigned = "no"
                if ( v.varValue > 0.0 ):
                    
                    ColumnIndex = 0
                    worksheet.write(row, ColumnIndex, airlineName)  
                
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, str(LpStatus[prob.status]))
                    
                    acICAOcode = str(v.name).split("_")[0]
    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, acICAOcode )
                
                    logger.debug ( "var name = {0} - var value = {1}".format( v.name, v.varValue ) )
                    assigned  = "yes"
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, assigned )
                    
                    ''' between index 0 which is the aircraft ICAO code and the flight leg there is the aircraft instance '''
                    Adep = str(v.name).split("_")[2]
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, Adep )    
                                
                    Ades = str(v.name).split("_")[3]
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, Ades )      
                               
                    airlineRoute = AirlineRoute.objects.filter(airline=airline , DepartureAirportICAOCode=Adep  , ArrivalAirportICAOCode=Ades).first()
                    if ( airlineRoute ):
                        
                        airlineAircraft = AirlineAircraft.objects.filter(airline=airline, aircraftICAOcode=acICAOcode).first()
                        if airlineAircraft:
                            
                            nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                            ColumnIndex += 1
                            worksheet.write(row, ColumnIndex, nbSeats ) 
                            
                            airlineCosts = AirlineCosts.objects.filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                            if airlineCosts:
                                
                                massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                                fuelCostsUSdollars = massLossKg * Kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                        
                                operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                                        
                                crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                                totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars     
                                
                                ''' 5th February 2023 - Costs per Available Seat Mile '''
                                miles = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex, miles )
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex, totalCostsUSdollars ) 
                                
                                seatsPerMiles = nbSeats * miles
                                casmUSdollars = totalCostsUSdollars / seatsPerMiles
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex, casmUSdollars ) 
                                
                                row = row + 1
                            
                            else:
                                print ("Airline costs not found")
                        
                        else:
                            print ("Aircraft not found = {0}".format(airlineAircraft))
                            
                    else:
                        print ("Error - route not found = {0}".format( airlineRoute ))
        
            logger.debug ( "Total CASM Objective  = {0}".format( value(prob.objective) ) )
            value_prob_objective = value(prob.objective)

            worksheet.autofit()     
            return value_prob_objective               

    else:
        ''' worksheet will contain only the headers '''
        print ( "airline not found = {}".format( airlineName ))
        return value_prob_objective
        

def createExcelWorkbook(memoryFile, request, airlineName):
    ''' create the EXCEL workbook '''
    wb = Workbook(memoryFile)
    ''' write the readme sheet '''
    row, wsReadMe, styleLavender, styleEntete = writeReadMe(workbook=wb, request=request, airlineName=airlineName)
    ''' write the costs results '''
    writeAirlineCasmResults(workbook=wb , airlineName=airlineName)
    ''' 27th May 2023 - add CASM minimization results '''
    value_prob_objective = writeAirlineCasmOptimizationResults(workbook=wb, airlineName=airlineName)
    
    row = row + 1
    wsReadMe.write(row, 0 , "CASM Objective function", styleLavender)
    wsReadMe.write(row, 1 , value_prob_objective , styleEntete)
    
    wsReadMe.autofit()  
    
    return wb


def getAirlineCasmXlsx(request, airlineName):
    ''' function retrieves a file to download '''
    logger.setLevel(logging.INFO)
    logger.debug ("retrieve Airline CASM as Xlsx file")        
        
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
    logger.debug ("views Airline CASM")
    
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
                        fuelCostsUSdollars = massLossKg * Kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                
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