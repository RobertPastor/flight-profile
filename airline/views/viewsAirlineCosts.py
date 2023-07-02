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

from pulp import LpProblem , LpMinimize ,  LpVariable, lpSum, LpStatus ,  PULP_CBC_CMD, value, LpBinary


from django.http import  JsonResponse
from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute

from trajectory.Environment.Constants import kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars
from airline.models import AirlineAircraftInstances
from airline.views.utils import compute_total_costs


''' 29th April 2023 add cruise level and adep . Ades runways '''
costsHeaders = ['airline' , 'aircraft'  , 'departureAirport' , 'adepRunway' , 'arrivalAirport' ,  'adesRunway' ,  'isAborted' , 'takeOffMassKg'  ,  'finalMassKg' , 'cruiseLevelFeet'  \
              , 'leg length NM' , 'Specific Range NM/kg' , 'flightDurationHours' , 'fuelCosts US$' , 'operationalCosts US$' , 'crewCosts US$' , 'totalCosts US$' ]       

costsMinimizationHeaders = [ 'airline' , 'Solver Status', 'aircraft' , 'departureAirport' , 'adepRunway' , 'arrivalAirport' , 'adesRunway' , 'totalCostsUSdollars' ]


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
    
    ''' Autofit the worksheet - adjust column width '''
    wsReadMe.autofit()
    return row, wsReadMe
    
    
def writeHeaders(worksheet, style, headers):
    row = 0
    col = 0
    for header in headers:
        worksheet.write(row, col , header , style)
        col = col + 1
   
    
def writeAirlineCostsResults(workbook , airlineName):
    
    worksheet = workbook.add_worksheet("Airline Costs")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    writeHeaders(worksheet, styleLavender, costsHeaders)
    
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
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.targetCruiseLevelFeet )
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.getFlightLegLengthMiles() )
                    
                    ''' 23rd May 2023 - specific range Nautical miles per Kg '''
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, airlineCosts.getFlightLegLengthMiles() / ( airlineCosts.getTakeOffMassKg() - airlineCosts.getFinalMassKg() ) )
                   
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
        
        
def writeAirlineCostsMinimization( workbook , airlineName ):
    pass
    worksheet = workbook.add_worksheet("Airline Costs Minimization")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    writeHeaders(worksheet, styleLavender , costsMinimizationHeaders)
    
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
            pass
            nbFligthtLegs = AirlineRoute.objects.filter(airline=airline).count()
            aircraftInstances = AirlineAircraftInstances()
            aircraftInstancesList = aircraftInstances.computeAirlineAircraftInstances(airlineName , nbFligthtLegs)
            #print ( aircraftInstancesList )
            
            #logger.debug ( "length of flight legs = {0}".format( AirlineRoute.objects.filter(airline=airline).count() ) )
            
            airlineCostsArray = []
            airlineAircraftICAOcodeList = []
            airlineAircraftFullNameList = []
            
            #for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
            for aircraftInstance in aircraftInstancesList:
                
                acICAOcode = aircraftInstances.getAircraftInstanceICAOcode(aircraftInstance)
                airlineAircraft = AirlineAircraft.objects.filter(airline=airline , aircraftICAOcode=acICAOcode).first()
                
                #print ( airlineAircraft.aircraftFullName )
                airlineAircraftICAOcodeList.append(airlineAircraft.aircraftICAOcode)
                airlineAircraftFullNameList.append(airlineAircraft.aircraftFullName)
                
                aircraftCostsArray = []
                airlineFlightLegsList = []
                
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                    
                    #print ( airlineRoute.getFlightLegAsString() )
                    airlineFlightLegsList.append(airlineRoute.getFlightLegAsString())
                    
                    airlineCosts = AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                    if airlineCosts:
                        
                        totalCostsUSdollars = compute_total_costs( airlineCosts, airlineAircraft )
                        
                        #print ( "{0} - {1} - {2}".format(airlineAircraft.aircraftICAOcode, airlineRoute.getFlightLegAsString() , type(totalCostsUSdollars) ))
                            
                        aircraftCostsArray.append( float(totalCostsUSdollars) )
                        
                airlineCostsArray.append(aircraftCostsArray)
                
            logger.debug ( airlineCostsArray )
            #print ( "number of aircrafts = {0}".format( len( AirlineAircraft.objects.filter(airline=airline) ) ) )
            #print ( "number of routes = {0}".format( len( AirlineRoute.objects.filter(airline=airline) ) ) )
            
            '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
            '''  if worker i is assigned to task j. '''
            #num_aircrafts = len( AirlineAircraft.objects.filter(airline=airline) )
            num_flight_legs = len( AirlineRoute.objects.filter(airline=airline) )
            
            #num_aircrafts = len(airlineCostsArray)
            num_aircraft_instances = len(aircraftInstancesList)
            
            logger.debug ( "number of aircraft instances = {0}".format( num_aircraft_instances ))
            num_flight_legs = len(airlineCostsArray[0])
            #print ( num_flight_legs )
            
            ''' Create the MIP solver with the SCIP back-end '''
            #solver = pywraplp.Solver.CreateSolver('SCIP')
            prob = LpProblem("AssignmentProblem", LpMinimize)
            
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
                    
            
            ''' --------- objective function --------------'''
            for i in range(num_aircraft_instances):
                for j in range(num_flight_legs):
                    pass
                    #objective_terms.append(float(airlineCostsArray[i][j]) * x[i, j])
            prob += lpSum( [ airlineCostsArray[i][j] * x_vars[i,j] for i in range(num_aircraft_instances) for j in range(num_flight_legs) ])
                    
            logger.debug ("--- add constraints ----")
            '''  Each aircraft is assigned to at most 1 flight leg. '''
            for i in range(num_aircraft_instances):
                pass
                #solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
                prob += lpSum( [ x_vars[i,j] for j in range(num_flight_legs) ] ) <= 1
                #c_list = lpSum ( [x_vars[i,j] for j in range(num_flight_legs)] ) <= 1
                #check_constraints(prob, c_list)
                
            ''' Each flight leg is assigned to exactly one aircraft '''
            for j in range(num_flight_legs):
                pass
                prob += lpSum ( [ x_vars[i,j] for i in range(num_aircraft_instances) ] ) == 1
                #check_constraints(prob, c_list)

                #solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) <= 1)
                
            ''' minimize the costs '''
            #solver.Minimize(solver.Sum(objective_terms))
            prob.solve(PULP_CBC_CMD(msg=0))
            logger.debug ("Status: {0}".format( str( LpStatus[prob.status] ) ) )
            
            #for name, c in list(prob.constraints.items()):
            #    print(name, ":", c, "\t", c.pi, "\t\t", c.slack)
            
            #prob.writeLP("pulp_problem.lp", writeSOS=1, mip=1 )
            
            row = 1
            for v in prob.variables():
                pass
            
                if ( v.varValue > 0.0 ):
                
                    ColumnIndex = 0
                    worksheet.write(row, ColumnIndex, airlineName)   
                    
                    ColumnIndex = ColumnIndex + 1
                    worksheet.write(row, ColumnIndex, str(LpStatus[prob.status]))  
                    
                    acICAOcode = str(v.name).split("_")[0]
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex,  str(acICAOcode) )
                    
                    Adep = str(v.name).split("_")[2]
                    Ades = str(v.name).split("_")[3]
                    
                    airlineRoute = AirlineRoute.objects.filter(airline=airline , DepartureAirportICAOCode=Adep  , ArrivalAirportICAOCode=Ades).first()
                    if ( airlineRoute ):
                        
                        airlineAircraft = AirlineAircraft.objects.filter(airline=airline, aircraftICAOcode=acICAOcode).first()
                        if airlineAircraft:
                            airlineCosts = AirlineCosts.objects.filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                            if airlineCosts:
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex,  str(Adep) )
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex,  str(airlineCosts.adepRunway) )
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex,  str(Ades) )
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex,  str(airlineCosts.adesRunway) )
                                
                                totalCostsUSdollars = compute_total_costs(airlineCosts, airlineAircraft )
                                
                                ColumnIndex += 1
                                worksheet.write(row, ColumnIndex,  (round ( totalCostsUSdollars , 2 )) )
                
                    
                                 
                    row = row + 1
                    
            worksheet.autofit()
            return value(prob.objective)
    else:
        return "Error : airline not found"
    
    
def createExcelWorkbook(memoryFile, request, airlineName):
    ''' create the EXCEL workbook '''
    wb = Workbook(memoryFile)
    ''' write the readme sheet '''
    row , wsReadMe = writeReadMe(workbook=wb, request=request, airlineName=airlineName)
    ''' write the costs results '''
    writeAirlineCostsResults(workbook=wb , airlineName=airlineName)
    ''' write costs minimization '''
    valueProblemObjective = writeAirlineCostsMinimization(workbook=wb , airlineName=airlineName)
    
    row = row + 1
    
    wsReadMe.write(row, 0 , "Objective function - Minimize Sum of Costs -US$")
    wsReadMe.write(row, 1 ,  ( valueProblemObjective ) )
    wsReadMe.autofit()
    
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
    logger.debug ("views Airline Costs")
    
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
    