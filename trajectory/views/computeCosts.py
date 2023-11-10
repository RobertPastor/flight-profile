'''
Created on 30 juil. 2022

@author: robert
'''

import logging
logger = logging.getLogger(__name__)
from django.http import  JsonResponse

from trajectory.models import BadaSynonymAircraft
from airline.models import Airline, AirlineRoute, AirlineAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.Guidance.FlightPathFile import FlightPath

from trajectory.Environment.Constants import Kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars


def computeDurationHours( durationSeconds ):
    durationMinutes = 0.0
    durationHours = 0.0
    if ( durationSeconds > 60.0 ):
        durationMinutes = durationSeconds / 60.0
        if ( durationMinutes > 60.0 ):
            durationHours = durationMinutes / 60.0
        else:
            durationHours = durationMinutes / 60.0
    else:
        durationHours = durationSeconds / 3600.0
    return durationHours
        

def computeCosts(request, airlineName):
    ''' @TODO same inputs as compute profile , compute costs and comput state vector  '''
    logger.setLevel(logging.DEBUG)
    logger.debug ("computeCosts - compute Flight leg related costs")
    
    #routeWayPointsList = []
    if (request.method == 'GET'):
        aircraftICAOcode = request.GET['aircraft']
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
        
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):

            logger.debug ("computeCosts è selected aircraft = {0}".format( aircraftICAOcode ) )
            
            # route as string
            airlineRoute = request.GET['route']
            
            logger.debug("computeCosts - " + airlineRoute)
            
            logger.debug ( str(airlineRoute).split("-")[0] )
            logger.debug ( str(airlineRoute).split("-")[1] )
            
            departureAirportICAOcode = str(airlineRoute).split("-")[0]
            departureAirportRunWayName = request.GET['AdepRwy']
            
            arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
            arrivalAirportRunWayName = request.GET['AdesRwy']
            
            takeOffMassKg = request.GET['mass']
            logger.debug( "takeOff mass Kg = {0}".format( takeOffMassKg ) )
            cruiseFLfeet = request.GET['fl'] 
            logger.debug( "cruise FL feet = {0}".format( cruiseFLfeet ) )
            
            reducedClimbPowerCoeff = 0.0
            try:
                reducedClimbPowerCoeff = request.GET['reduc']
                reducedClimbPowerCoeff = float(reducedClimbPowerCoeff)
            except:
                reducedClimbPowerCoeff = 0.0
            
            airline = Airline.objects.filter(Name=airlineName).first()
            if (airline):

                airlineRoute = AirlineRoute.objects.filter(airline = airline, DepartureAirportICAOCode = departureAirportICAOcode, ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
            
                if (airlineRoute):
                    #print ( airlineRoute )
                    '''  use runways defined in the web page '''
                    routeAsString = airlineRoute.getRouteAsString(departureAirportRunWayName, arrivalAirportRunWayName)
                    logger.debug ( routeAsString )
                    
                    acPerformance = AircraftJsonPerformance(aircraftICAOcode, badaAircraft.getAircraftPerformanceFile())
                    if ( acPerformance.read() ):
                        #logger.info ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                        #logger.info ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
        
                        flightPath = FlightPath(
                                        route = routeAsString, 
                                        aircraftICAOcode = aircraftICAOcode,
                                        RequestedFlightLevel = float ( cruiseFLfeet )  / 100.0 , 
                                        cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                        takeOffMassKilograms =  float(takeOffMassKg) ,
                                        reducedClimbPowerCoeff = float(reducedClimbPowerCoeff) )
        
                        flightPath.computeFlight(deltaTimeSeconds = 1.0)
            
                        logger.debug ( "=========== Flight Plan computation is done  =========== " )
                        
                        fuelCostsUSdollars =  ( flightPath.aircraft.getAircraftInitialMassKilograms() - flightPath.aircraft.getAircraftCurrentMassKilograms() )  * Kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars 
        
                        airlineAircraft = AirlineAircraft.objects.filter(aircraftICAOcode=aircraftICAOcode).first()
                        operationalFlyingCostsUSdollars = ( flightPath.getFlightDurationSeconds() / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                        #print ( airlineAircraft.getCostsFlyingPerHoursDollars() )
                        #print ( flightPath.getFlightDurationSeconds() / 3600.0  )
                        ''' 21st September 2022 - Crew Costs '''
                        crewCostsUSdollars = ( flightPath.getFlightDurationSeconds() / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                           
                        response_data = {
                                        'seats' : airlineAircraft.getMaximumNumberOfPassengers(),
                                        'isAborted': flightPath.abortedFlight ,
                                        'initialMassKilograms'   : flightPath.aircraft.getAircraftInitialMassKilograms(),
                                        'takeOffMassKilograms'   : flightPath.aircraft.getAircraftInitialMassKilograms(),
                                        'cruiseLevelFeet'        : cruiseFLfeet,
                                        'reducedClimbPowerCoeff' : reducedClimbPowerCoeff,
                                        'finalMassKilograms'     : round ( flightPath.aircraft.getAircraftCurrentMassKilograms() , 1),
                                        'massLossFilograms'      : round ( flightPath.aircraft.getAircraftInitialMassKilograms()-flightPath.aircraft.getAircraftCurrentMassKilograms() , 1 ),
                                        'fuelCostsDollars'       : round( fuelCostsUSdollars , 0),
                                        'flightDurationHours'    : round ( ( float(flightPath.getFlightDurationSeconds() ) / 3600.0 ), 4 ),
                                        'operationalFlyingCostsDollars' : round ( operationalFlyingCostsUSdollars , 0),
                                        'crewFlyingCostsDollars'        : round( crewCostsUSdollars , 0 ),
                                        'totalCostsDollars'             : round ( fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars , 0 )
                                        }
                        return JsonResponse(response_data)
                    else:
                        logger.info ('Error - acPerformance read failed = {0}'.format(badaAircraft.getAircraftJsonPerformanceFile()))
                        response_data = { 'errors' : 'acPerformance read failed = {0}'.format(badaAircraft.getAircraftJsonPerformanceFile()) }
                        return JsonResponse(response_data)
                    
                else:
                    logger.info ('airline route not found = {0}'.format(airlineRoute))
                    response_data = { 'errors' : 'Airline route not found = {0}'.format(airlineRoute) }
                    return JsonResponse(response_data)
                
            else:
                logger.info ('airline not found = {0}'.format(airlineName))
                response_data = {'errors' : 'Airline not found = {0}'.format(airlineName)}
                return JsonResponse(response_data)
                
        else:
            logger.info ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
            logger.info ("or aircraft performance file = {0} not found".format(badaAircraft))
            response_data = {
                'errors' : 'Aircraft performance file {0} not found - please select another aircraft'.format(aircraftICAOcode)}
            return JsonResponse(response_data)
            
    else:
        return JsonResponse({'errors': "expecting GET method"})