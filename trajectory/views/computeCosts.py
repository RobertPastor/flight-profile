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
from trajectory.views.utils import getAircraftFromRequest, getRouteFromRequest , getReducedClimbPowerCoeffFromRequest
from trajectory.views.utils import getAdepRunwayFromRequest, getAdesRunwayFromRequest, getMassFromRequest , getFlightLevelFromRequest
from trajectory.views.utils import getDirectRouteFromRequest

from trajectory.Openap.AircraftMainFile import OpenapAircraft
from trajectory.Environment.Earth import Earth
from trajectory.Environment.Atmosphere import Atmosphere
from openap import prop
from trajectory.GuidanceOpenap.FlightPathOpenapFile import FlightPathOpenap


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
        
        
def computeWrapCosts ( request , airlineName , aircraftICAOcode ):
    
    earth = Earth()
    atmosphere = Atmosphere()

    #print("Wrap mode")
    ac = None
    available_acs = prop.available_aircraft(use_synonym=True)
    for WrapAcCode in available_acs:
        if str(WrapAcCode).upper() == aircraftICAOcode:
            ac = OpenapAircraft( aircraftICAOcode , earth , atmosphere , initialMassKilograms = None)
            logging.info( ac.getAircraftName())
            
            ''' 1st April 2024 - checkbox to fly direct route '''
            direct = getDirectRouteFromRequest(request)
                
            airline = Airline.objects.filter(Name=airlineName).first()
            if (airline):
    
                airlineRoute = getRouteFromRequest(request)
                if (airlineRoute):
                    
                    departureAirportICAOcode = str(airlineRoute).split("-")[0]
                    departureAirportRunWayName = getAdepRunwayFromRequest(request)
                
                    arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
                    arrivalAirportRunWayName = getAdesRunwayFromRequest(request)
                    
                    airlineRoute = AirlineRoute.objects.filter(airline = airline, 
                                                               DepartureAirportICAOCode = departureAirportICAOcode, 
                                                               ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
                    if (airlineRoute):
                        routeAsString = airlineRoute.getRouteAsString(AdepRunWayName=departureAirportRunWayName, 
                                                                      AdesRunWayName=arrivalAirportRunWayName, 
                                                                      direct=direct)
                        
                        takeOffMassKg = float( getMassFromRequest(request) )
                        cruiseFlightLevel = float( getFlightLevelFromRequest(request) ) / 100.0

                        flightPath = FlightPathOpenap(
                            route                = routeAsString, 
                            aircraftICAOcode     = aircraftICAOcode,
                            RequestedFlightLevel = cruiseFlightLevel, 
                            cruiseMach           = ac.getMaximumSpeedMmoMach(), 
                            takeOffMassKilograms = takeOffMassKg)
                        try:
                            flightPath.computeFlight(deltaTimeSeconds = 1.0)
                        
                            airlineAircraft = AirlineAircraft.objects.filter(aircraftICAOcode=aircraftICAOcode).first()

                            fuelCostsUSdollars =  ( takeOffMassKg - ac.getCurrentMassKilograms() )  * Kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars 
                            operationalFlyingCostsUSdollars = ( flightPath.getFlightDurationSeconds() / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                            crewCostsUSdollars = ( flightPath.getFlightDurationSeconds() / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()

                            response_data = {
                                            'seats'                  : ac.getMaximumNumberOfPassengers(),
                                            'isAborted'              : flightPath.abortedFlight ,
                                            'initialMassKilograms'   : takeOffMassKg,
                                            'takeOffMassKilograms'   : takeOffMassKg,
                                            'cruiseLevelFeet'        : round ( float ( getFlightLevelFromRequest(request) ) , 0 ),
                                            'reducedClimbPowerCoeff' : 0.0,
                                            'direct'                 : direct,
                                            'finalMassKilograms'     : round ( flightPath.getAircraft().getCurrentMassKilograms() , 1),
                                            'massLossFilograms'      : round ( takeOffMassKg - flightPath.getAircraft().getCurrentMassKilograms() , 1 ),
                                            'fuelCostsDollars'       : round( fuelCostsUSdollars , 0),
                                            'flightDurationHours'    : round ( ( float(flightPath.getFlightDurationSeconds() ) / 3600.0 ), 4 ),
                                            'operationalFlyingCostsDollars' : round ( operationalFlyingCostsUSdollars , 0),
                                            'crewFlyingCostsDollars'        : round( crewCostsUSdollars , 0 ),
                                            'totalCostsDollars'             : round ( fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars , 0 )
                                            }
                            return JsonResponse(response_data)
                        
                        except Exception as e:
                            logging.error("Trajectory Compute Wrap - Exception = {0}".format( str(e ) ) )

    if ac == None:
        logger.info ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
        response_data = {
                'errors' : 'Aircraft performance file {0} not found - please select another aircraft'.format(aircraftICAOcode)}
        return JsonResponse(response_data)

        
def computeBadaCosts ( request , airline , aircraftICAOcode):
    pass

    badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
            
    if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
    
                logger.debug ("computeCosts for selected aircraft = {0}".format( aircraftICAOcode ) )
                
                # route as string
                airlineRoute = getRouteFromRequest(request)
                
                logger.debug("computeCosts - " + airlineRoute)
                
                logger.debug ( str(airlineRoute).split("-")[0] )
                logger.debug ( str(airlineRoute).split("-")[1] )
                
                departureAirportICAOcode = str(airlineRoute).split("-")[0]
                departureAirportRunWayName = getAdepRunwayFromRequest(request)
                
                arrivalAirportICAOcode = str(airlineRoute).split("-")[1]
                arrivalAirportRunWayName = getAdesRunwayFromRequest(request)
                
                takeOffMassKg = getMassFromRequest(request)
                logger.debug( "takeOff mass Kg = {0}".format( takeOffMassKg ) )
                cruiseFLfeet = getFlightLevelFromRequest(request)
                logger.debug( "cruise FL feet = {0}".format( cruiseFLfeet ) )
                
                reducedClimbPowerCoeff = 0.0
                try:
                    reducedClimbPowerCoeff = getReducedClimbPowerCoeffFromRequest(request)
                    reducedClimbPowerCoeff = float(reducedClimbPowerCoeff)
                except:
                    reducedClimbPowerCoeff = 0.0
                    
                ''' 1st April 2024 - checkbox to fly direct route '''
                direct = getDirectRouteFromRequest(request)
                
                airlineRoute = AirlineRoute.objects.filter(airline = airline, 
                                                           DepartureAirportICAOCode = departureAirportICAOcode, 
                                                           ArrivalAirportICAOCode=arrivalAirportICAOcode).first()
                
                if (airlineRoute):
                    #print ( airlineRoute )
                    '''  use runways defined in the web page '''
                    routeAsString = airlineRoute.getRouteAsString(AdepRunWayName = departureAirportRunWayName, 
                                                                      AdesRunWayName = arrivalAirportRunWayName, 
                                                                      direct         = direct)
                    logger.debug ( routeAsString )
                        
                    acPerformance = AircraftJsonPerformance(aircraftICAOcode, badaAircraft.getAircraftPerformanceFile())
                    if ( acPerformance.read() ):
                            #logger.info ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                            #logger.info ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
                            
                            flightPath = FlightPath(
                                            route                 = routeAsString, 
                                            aircraftICAOcode      = aircraftICAOcode,
                                            RequestedFlightLevel  = float ( cruiseFLfeet )  / 100.0 , 
                                            cruiseMach            = acPerformance.getMaxOpMachNumber(), 
                                            takeOffMassKilograms  =  float(takeOffMassKg) ,
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
                            ''' 6th April 204 add direct route '''
                            response_data = {
                                            'seats'                  : airlineAircraft.getMaximumNumberOfPassengers(),
                                            'isAborted'              : flightPath.abortedFlight ,
                                            'initialMassKilograms'   : flightPath.aircraft.getAircraftInitialMassKilograms(),
                                            'takeOffMassKilograms'   : flightPath.aircraft.getAircraftInitialMassKilograms(),
                                            'cruiseLevelFeet'        : cruiseFLfeet,
                                            'reducedClimbPowerCoeff' : reducedClimbPowerCoeff,
                                            'direct'                 : direct,
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
        logger.info ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
        logger.info ("or aircraft performance file = {0} not found".format(badaAircraft))
        response_data = {
                'errors' : 'Aircraft performance file {0} not found - please select another aircraft'.format(aircraftICAOcode)}
        return JsonResponse(response_data)
        

def computeCosts(request, airlineName , BadaWrap ):
    ''' @TODO same inputs as compute profile , compute costs and compute state vector  '''
    logger.setLevel(logging.DEBUG)
    logger.debug ("computeCosts - compute Flight leg related costs")
    
    #routeWayPointsList = []
    if (request.method == 'GET'):
        
        aircraftICAOcode = getAircraftFromRequest( request )
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):

            if BadaWrap ==  "BADA":
                return computeBadaCosts ( request , airline , aircraftICAOcode )
                
            else:
                return computeWrapCosts( request , airline , aircraftICAOcode )
            
        else:
            logger.info ('airline not found = {0}'.format(airlineName))
            response_data = {'errors' : 'Airline not found = {0}'.format(airlineName)}
            return JsonResponse(response_data)
        
    else:
        return JsonResponse({'errors': "expecting GET method"})