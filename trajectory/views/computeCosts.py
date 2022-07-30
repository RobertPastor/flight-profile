'''
Created on 30 juil. 2022

@author: robert
'''

import logging
logger = logging.getLogger(__name__)
from django.http import  JsonResponse
from trajectory.models import BadaSynonymAircraft
from airline.models import AirlineRoute, AirlineAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.Guidance.FlightPathFile import FlightPath

from trajectory.Environment.Constants import kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars


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
        

def computeCosts(request):
    logger.setLevel(logging.INFO)
    logger.info ("compute Flight Profile")
    
    #routeWayPointsList = []
    if (request.method == 'GET'):
        aircraftICAOcode = request.GET['aircraft']
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
        
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):

            logger.info ("selected aircraft = {0}".format( aircraftICAOcode ) )
            
            airlineRoute = request.GET['route']
            
            logger.info(airlineRoute)
            
            logger.info ( str(airlineRoute).split("-")[0] )
            logger.info ( str(airlineRoute).split("-")[1] )
            
            departureAirportICAOcode = str(airlineRoute).split("-")[0]
            departureAirportRunWayName = request.GET['AdepRwy']
            
            arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
            arrivalAirportRunWayName = request.GET['AdesRwy']

            airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode = departureAirportICAOcode, ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
            
            if (airlineRoute):
                #print ( airlineRoute )
                '''  use runways defined in the web page '''
                routeAsString = airlineRoute.getRouteAsString(departureAirportRunWayName, arrivalAirportRunWayName)
                logger.info ( routeAsString )
                acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
                logger.info ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                logger.info ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   

                flightPath = FlightPath(
                                route = routeAsString, 
                                aircraftICAOcode = aircraftICAOcode,
                                RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet() / 100., 
                                cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                takeOffMassKilograms = acPerformance.getMaximumMassKilograms())

                flightPath.computeFlight(deltaTimeSeconds = 1.0)
    
                logger.info ( "=========== Flight Plan computation is over  =========== " )
                
                fuelCostsUSdollars =  ( flightPath.aircraft.getAircraftInitialMassKilograms() - flightPath.aircraft.getAircraftCurrentMassKilograms() )  * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars 

                airlineAircraft = AirlineAircraft.objects.filter(aircraftICAOcode=aircraftICAOcode).first()
                operationalCostsUSdollars = ( flightPath.getFlightDurationSeconds() / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                   
                response_data = {
                                'isAborted': flightPath.abortedFlight ,
                                'initialMassKilograms' : flightPath.aircraft.getAircraftInitialMassKilograms(),
                                'finalMassKilograms' : round ( flightPath.aircraft.getAircraftCurrentMassKilograms() , 1),
                                'massLossFilograms' : round ( flightPath.aircraft.getAircraftInitialMassKilograms()-flightPath.aircraft.getAircraftCurrentMassKilograms() , 1 ),
                                'fuelCostsDollars' : round( fuelCostsUSdollars , 2),
                                'flightDurationHours' : round ( computeDurationHours ( flightPath.getFlightDurationSeconds() ) , 2 ),
                                'operationalflightCostsDollars' : round ( operationalCostsUSdollars , 2)
                                }
                return JsonResponse(response_data)
                

            else:
                logger.info ('airline route not found = {0}'.format(airlineRoute))
                response_data = {
                    'errors' : 'Airline route not found = {0}'.format(airlineRoute)}
                return JsonResponse(response_data)
                
        else:
            logger.info ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
            logger.info ("or aircraft performance file = {0} not found".format(badaAircraft))
            response_data = {
                'errors' : 'Aircraft performance file {0} not found - please select another aircraft'.format(aircraftICAOcode)}
            return JsonResponse(response_data)
            
    else:
        return JsonResponse({'errors': "expecting GET method"})