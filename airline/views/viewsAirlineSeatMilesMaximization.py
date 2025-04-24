'''
Created on 6 mai 2023

@author: robert

Maximize Seats Miles for one airline fleet and a set of flight legs

'''


import logging
logger = logging.getLogger(__name__)
import io

from datetime import datetime 
from xlsxwriter import Workbook
from django.shortcuts import HttpResponse
from django.http import  JsonResponse

from pulp import LpProblem  ,  LpVariable, lpSum, LpStatus ,  PULP_CBC_CMD, value, LpBinary, LpMaximize

from airline.models import Airline, AirlineAircraft, AirlineRoute, AirlineCosts, AirlineAircraftInstances
from trajectory.Environment.Constants import Meter2NauticalMiles

from airline.views.utils import computeAirportNumberOfRunways

headersResults = [ 'Airline' , 'Aircraft ICAO' , 'Aircraft' , 'Is Aborted', 'Departure', 'Adep Turn Around Time Sec', 'Arrival', 'Ades Turn Around Time Sec' ,
                   'nb Seats' , 'Aircraft Turn Around Time Sec' ,'Reduced Climb Power Coeff' , 'Leg Duration Sec' , 
                  'Leg Distance Nm' , 'Nb Rotations in 20 hours', 'Seat Miles Flown 20 hours Nm']

headersMaximization = [ 'Airline' , 'Aircraft' , 'Solver Status', 'Assigned', 'Departure', 'Arrival',  'nb Seats' , 'Aircraft Turn Around Times Sec' ,'Reduced Climb Power Coeff', 
                       'Leg Duration Sec' , 'Leg Distance Nm' , 'Nb Rotations in 20 hours', 'Seat Miles Flown 20 hours Nm']

maxDailyHours= 20.0

def computeAirportTurnAroundTimeSeconds( airportICAOcode ):
    return ( computeAirportNumberOfRunways ( airportICAOcode ) * 60 )

def computeNumberOfRotations(flightDurationSeconds , turnAroundTimesSeconds , airlineRoute):
    
    assert ( isinstance(  airlineRoute , AirlineRoute)) and  not ( airlineRoute is None)
    
    departureAirportICAOcode = airlineRoute.getDepartureAirportICAOcode()
    arrivalAirportICAOcode   = airlineRoute.getArrivalAirportICAOcode()
    ''' the aircraft is ready after 
    1) one flight level duration to the destination airport
    2) plus 1 turn around time at the arrival airport 
    3) one flight leg duration to the departure air^port 
    4) plus 1 turn around time at the departure airport '''
    totalRotationDurationSeconds =  ( flightDurationSeconds + turnAroundTimesSeconds ) * 2 
    ''' coeff dependent upon the number of runways of each airport '''
    totalRotationDurationSeconds = totalRotationDurationSeconds + computeAirportTurnAroundTimeSeconds  ( departureAirportICAOcode )
    totalRotationDurationSeconds = totalRotationDurationSeconds + computeAirportTurnAroundTimeSeconds ( arrivalAirportICAOcode ) 
    
    return int ( ( maxDailyHours * 3600 ) / totalRotationDurationSeconds )


def computeSeatMilesResults(airline, airlineName):
    
    airlineSeatsMiles = []
    ''' need to define aircraft instances as the "costs" table must be squared between aircrafts instances and flight legs '''
            
    nbFligthtLegs = AirlineRoute.objects.filter(airline=airline).count()
    aircraftInstances = AirlineAircraftInstances()
    aircraftInstancesList = aircraftInstances.computeAirlineAircraftInstances(airlineName , nbFligthtLegs)
    #print ( aircraftInstancesList )
            
    for aircraftInstance in aircraftInstancesList:
                
                acICAOcode = aircraftInstances.getAircraftInstanceICAOcode(aircraftInstance)
                airlineAircraft = AirlineAircraft.objects.filter(airline=airline , aircraftICAOcode=acICAOcode).first()
                                
                nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                turnAroundTimesSeconds = airlineAircraft.getTurnAroundTimesMinutes() * 60
            
                #print ( "aircraft = {0} - number of seats = {1} - turnAround times Seconds = {2}".format( airlineAircraft , nbSeats , turnAroundTimesSeconds) )
                
                aircraftSeatMiles = []
                airlineFlightLegsList = []
                
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                    
                    airlineFlightLegsList.append(airlineRoute.getFlightLegAsString())
                    
                    airlineCosts = AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                    if airlineCosts:
                        
                        milesFlownPerLeg = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                        #print ("aircraft = {0} - flight leg = {1} - flight duration (Seconds) = {2} - distance flown (nautics) = {3}".format(airlineAircraft, airlineRoute.getFlightLegAsString() , airlineCosts.flightDurationSeconds, milesFlownPerLeg))
                        nbRotationsDay = computeNumberOfRotations ( airlineCosts.flightDurationSeconds ,  turnAroundTimesSeconds , airlineRoute )
                        #print ( "nb rotations = {0} - nb rotations = {1}".format( nbRotationsDay , int(nbRotationsDay) ) )
                        
                        totalSeatMilesFlownPerDay = nbSeats * int(nbRotationsDay) * 2 * milesFlownPerLeg
                        #print ( "total miles flown in 20 hours = {0}".format( totalSeatMilesFlownPerDay ))
                        
                        aircraftSeatMiles.append( totalSeatMilesFlownPerDay )
                        
                airlineSeatsMiles.append(aircraftSeatMiles)
                
    return airlineSeatsMiles , airlineFlightLegsList
                
                
def writeReadMe(workbook, airlineName):

    wsReadMe = workbook.add_worksheet("ReadMe")
    styleEntete = workbook.add_format({'bold': False, 'border': True})
    styleLavender = workbook.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
    
    row = 0
    wsReadMe.write(row, 0 , "Airline Services", styleLavender)
    wsReadMe.write(row, 1 , "Airline Seats Miles Maximization", styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Airline", styleLavender)
    wsReadMe.write(row, 1 , airlineName, styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Purpose", styleLavender)
    wsReadMe.write(row, 1 , "Seat Miles Flown in 20 Hours", styleEntete)
    
    row = row + 1
    wsReadMe.write(row, 0 , "Date", styleLavender)
    wsReadMe.write(row, 1 , datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") , styleEntete)
    
    ''' set width of each column '''
    wsReadMe.set_column(0 , 1 , len("Airline Services"))
    
    # Autofit the worksheet.
    wsReadMe.autofit()
    return wsReadMe, row
    

def writeHeaders(worksheet, style, headers):
    row = 0
    col = 0
    for header in headers:
        worksheet.write(row, col , header , style)
        col = col + 1
    
def writeAirlineSeatMilesResults(workbook, airlineName):
    
    worksheet = workbook.add_worksheet("Airline Seat Miles Results")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    writeHeaders(worksheet, styleLavender , headersResults)
    
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
        
        row  = 1
        for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                                                
                nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                turnAroundTimesSeconds = airlineAircraft.getTurnAroundTimesMinutes() * 60
                            
                airlineFlightLegsList = []
                
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                    
                    airlineFlightLegsList.append(airlineRoute.getFlightLegAsString())
                    
                    airlineCosts = AirlineCosts.objects.filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                    if airlineCosts:
                        
                        milesFlownPerLeg = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                        #print ("aircraft = {0} - flight leg = {1} - flight duration (Seconds) = {2} - distance flown (nautics) = {3}".format(airlineAircraft, airlineRoute.getFlightLegAsString() , airlineCosts.flightDurationSeconds, milesFlownPerLeg))
                        nbRotationsDay = computeNumberOfRotations ( airlineCosts.flightDurationSeconds , turnAroundTimesSeconds , airlineRoute)
                        #print ( "nb rotations = {0} - nb rotations = {1}".format( nbRotationsDay , int(nbRotationsDay) ) )
                        
                        totalSeatMilesFlownPerDay = nbSeats * int(nbRotationsDay) * 2 * milesFlownPerLeg
                        #print ( "total miles flown in 20 hours = {0}".format( totalSeatMilesFlownPerDay ))
                        
                        ColumnIndex = 0
                        worksheet.write(row, ColumnIndex, airlineName)   
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, airlineAircraft.getAircraftICAOcode())   
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, airlineAircraft.getAircraftFullName())   
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, str(airlineCosts.isAborted) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, airlineRoute.getDepartureAirportICAOcode())
    
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, computeAirportTurnAroundTimeSeconds ( airlineRoute.getDepartureAirportICAOcode() ) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, airlineRoute.getArrivalAirportICAOcode())
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, computeAirportTurnAroundTimeSeconds ( airlineRoute.getArrivalAirportICAOcode() ) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, (nbSeats) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, (turnAroundTimesSeconds) )
                        
                        ''' 20th January 2024 - add Reduced Climb Power Coeff '''
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, (airlineCosts.reducedClimbPowerCoeff) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, (airlineCosts.flightDurationSeconds) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, (milesFlownPerLeg) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, (int(nbRotationsDay)) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, (totalSeatMilesFlownPerDay) )
                        
                        row = row + 1
        
    worksheet.autofit()
        
        
def writeAirlineSeatMilesMaximization(workbook, airlineName):
    
    worksheet = workbook.add_worksheet("Airline Seat Miles Maximization")
    styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
    
    writeHeaders(worksheet, styleLavender , headersMaximization)
    row  = 1
    airline = Airline.objects.all().filter(Name=airlineName).first()
    if airline:
        
        airlineSeatsMiles , airlineFlightLegsList = computeSeatMilesResults(airline, airlineName)
        
        prob = LpProblem("Seat-Miles-Problem", LpMaximize)
        
        nbFligthtLegs = AirlineRoute.objects.filter(airline=airline).count()
        aircraftInstances = AirlineAircraftInstances()
        aircraftInstancesList = aircraftInstances.computeAirlineAircraftInstances(airlineName , nbFligthtLegs)
                
        num_aircraft_instances = len(aircraftInstancesList)
        num_flight_legs = len( AirlineRoute.objects.filter(airline=airline) )

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
        prob += lpSum( [ airlineSeatsMiles[i][j] * x_vars[i,j] for i in range(num_aircraft_instances) for j in range(num_flight_legs) ])

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
                
        prob.solve(PULP_CBC_CMD(msg=0))
        logger.debug ("Status: {0}".format( str( LpStatus[prob.status] ) ) )
        
        #print ( "Seat Miles Max - objective function value   = {0}".format( value(prob.objective) ) )
            
        for v in prob.variables():
                
                acICAOcode = str(v.name).split("_")[0]
                
                if ( v.varValue > 0.0 ):
                    ''' this aircraft is assigned to a leg '''
                    logger.debug ( "var name = {0} - var value = {1}".format( v.name, v.varValue ) )
                
                    ColumnIndex = 0
                    worksheet.write(row, ColumnIndex, airlineName)   
                            
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, acICAOcode)
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, str(LpStatus[prob.status]))
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, "yes")
                    
                    ''' between index 0 which is the aircraft ICAO code and the flight leg there is the aircraft instance '''
                    Adep = str(v.name).split("_")[2]
                    Ades = str(v.name).split("_")[3]
                            
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, Adep)
        
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, Ades)
                    
                    airlineAircraft = AirlineAircraft.objects.filter(airline=airline , aircraftICAOcode=acICAOcode).first()
                    nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                    turnAroundTimesSeconds = airlineAircraft.getTurnAroundTimesMinutes() * 60
                
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, nbSeats)
                    
                    ColumnIndex += 1
                    worksheet.write(row, ColumnIndex, turnAroundTimesSeconds)
                    
                    airlineRoute = AirlineRoute.objects.filter(airline=airline, DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
                    airlineCosts = AirlineCosts.objects.filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                    if airlineCosts:
                        
                        ''' 20th January 2024 - add Reduced Climb Power Coeff '''
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, airlineCosts.reducedClimbPowerCoeff)
                        
                        milesFlownPerLeg = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                        #print ("aircraft = {0} - flight leg = {1} - flight duration (Seconds) = {2} - distance flown (nautics) = {3}".format(airlineAircraft, airlineRoute.getFlightLegAsString() , airlineCosts.flightDurationSeconds, milesFlownPerLeg))
                        nbRotationsDay = computeNumberOfRotations ( airlineCosts.flightDurationSeconds , turnAroundTimesSeconds , airlineRoute )
                        #print ( "nb rotations = {0} - nb rotations = {1}".format( nbRotationsDay , int(nbRotationsDay) ) )
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, airlineCosts.flightDurationSeconds)
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, milesFlownPerLeg)
                        
                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, int(nbRotationsDay))
                        
                        totalSeatMilesFlownPerDay = nbSeats * int(nbRotationsDay) * 2 * milesFlownPerLeg

                        ColumnIndex += 1
                        worksheet.write(row, ColumnIndex, totalSeatMilesFlownPerDay)
                    
                    row = row + 1
                    
        worksheet.autofit()
        return value(prob.objective)
    else:
        row = 1
        ColumnIndex = 0
        worksheet.write(row, ColumnIndex, "airline not found - {0}".format(airlineName))
        return 0.0
    
    
def createExcelWorkbook(memoryFile, airlineName):
    
    ''' create the EXCEL workbook '''
    wb = Workbook(memoryFile)
    
    ''' write the readme sheet '''
    wsReadMe, row = writeReadMe(workbook=wb, airlineName=airlineName)
    ''' write the seat miles results '''
    writeAirlineSeatMilesResults(workbook=wb , airlineName=airlineName)
    ''' write the maximisation results '''
    #maxSumSeatMiles = writeAirlineSeatMilesMaximization(workbook=wb , airlineName=airlineName)
    maxSumSeatMiles = 0.0
    row = row + 1
    
    styleBoldYellow = wb.add_format({'bold': True, 'border': True, 'bg_color': 'yellow'})
    styleEntete = wb.add_format({'bold': False, 'border': True})
    
    wsReadMe.write(row, 0 , "Objective function - max Sum Seat Miles" , styleBoldYellow )
    wsReadMe.write(row, 1 , maxSumSeatMiles, styleEntete)
    wsReadMe.autofit()
    return wb

    
def getAirlineSeatsMilesMaxXlsx(request, airlineName):

    logger.setLevel(logging.INFO)
    logger.debug ("retrieve Airline CASM as Xlsx file")        
            
    if (request.method == 'GET'):
            
        ''' Robert - python2 to python 3 '''
        memoryFile = io.BytesIO() # create a file-like object 
                        
        # warning : we get strings from the URL query
        wb = createExcelWorkbook(memoryFile, airlineName)
        wb.close()
                                
        filename = 'AirlineSeatMilesMaximization-{}.xlsx'.format( datetime.now().strftime("%d-%B-%Y-%Hh%Mm%S") )
                                
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