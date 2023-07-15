'''
Created on 23 mai 2023

@author: robert
'''

from airline.models import Airline
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.models import BadaSynonymAircraft
from trajectory.models import  AirlineAirport, AirlineRunWay

import logging
logger = logging.getLogger(__name__)
from django.http import  JsonResponse

from trajectory.Environment.Atmosphere import Atmosphere
from trajectory.Environment.Earth import Earth

from trajectory.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from trajectory.Guidance.GroundRunLegFile import GroundRunLeg


def getBadaAircraft(aircraftICAOcode):
        
    logger.info ( '================ get aircraft =================' )
    atmosphere = Atmosphere()
    earth = Earth()
    acBd = BadaAircraftDatabase()
    assert acBd.read()
        
    if ( acBd.aircraftExists( aircraftICAOcode ) and
        acBd.aircraftPerformanceFileExists( aircraftICAOcode)):
            
        logger.info ( 'performance file= {0}'.format(acBd.getAircraftPerformanceFile(aircraftICAOcode)) )
        aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                        badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                        atmosphere = atmosphere,
                                        earth = earth)
        aircraft.dump()
        return aircraft
    else:
        raise ValueError( 'aircraft not found= ' + aircraftICAOcode)
    
    
def buildDepartureGroungRun(departureRunway , aircraft , departureAirport):
    ''' 
        this function manages the departure phases with a ground run 
    '''
    
    logger.info ( '================ build Departure Ground Run =================' )

    groundRun = GroundRunLeg(runway = departureRunway, aircraft = aircraft, airport = departureAirport)
    # default values not used here
    distanceToLastFixMeters = 10000.0
    distanceStillToFlyMeters = 10000.0
    flightLengthMeters = 10000.0

    elapsedTimeSeconds = 0.0
    deltaTimeSeconds = 1.0
    
    groundRun.buildDepartureGroundRun(deltaTimeSeconds  = deltaTimeSeconds,
                                        elapsedTimeSeconds = elapsedTimeSeconds,
                                        distanceStillToFlyMeters = distanceStillToFlyMeters,
                                        distanceToLastFixMeters = distanceToLastFixMeters)
    
    distanceStillToFlyMeters = flightLengthMeters - groundRun.getLengthMeters()

    initialWayPoint = groundRun.getLastVertex().getWeight()
    logger.info ( initialWayPoint )
    return groundRun.getTotalLegDistanceMeters() , groundRun.getLastTrueAirSpeedMetersSecond()


def computeRunwayOvershoot(request, aircraft , airport, runway , mass):

    if request.method == 'GET':

        airline = Airline.objects.first()
        if ( airline ):
                
            badaSynonymAircraft = BadaSynonymAircraft.objects.filter(AircraftICAOcode=aircraft).first()
            if ( badaSynonymAircraft and badaSynonymAircraft.aircraftPerformanceFileExists()):
                
                acPerformance = AircraftPerformance(badaSynonymAircraft.getAircraftPerformanceFile()) 
                if ( acPerformance.read() ):
                    
                    airportObj = AirlineAirport.objects.filter(AirportICAOcode = airport).first()
                    if ( airportObj ):
                        
                        badaAircraft = getBadaAircraft ( aircraft )
                        if ( badaAircraft ):
                            
                            runwayObj = AirlineRunWay.objects.filter( Airport = airportObj, Name = runway ).first()
                            
                            if ( runwayObj ):
                                ''' convert to environment runway '''
                                runwayObj = runwayObj.convertToEnvRunway()
                                                            
                                maxTakeOffMassKg = acPerformance.getMaximumMassKilograms()
                                minTakeOffMassKg = acPerformance.getMinimumMassKilograms()
                                
                                if ( ( float ( mass ) * 1000.0 ) >= minTakeOffMassKg ) and  ( ( float ( mass ) * 1000.0 ) <= maxTakeOffMassKg ):
                                    
                                    badaAircraft.setAircraftMassKilograms( float ( mass ) * 1000.0 )
                                    badaAircraft.setDepartureGroundRunConfiguration( 0.0 )
                                    
                                    takeOffStallSpeedCasKnots = badaAircraft.computeStallSpeedCasKnots()
                                    logger.info ( "TakeOff Stall speed = {0} Kcas Knots".format( badaAircraft.computeStallSpeedCasKnots() ) )
                                    
                                    airportObj = airportObj.convertToEnvAirport()
                                    
                                    ''' build the ground run '''
                                    totalGroundLegLengthMeters , trueAirSpeedMetersSecond = buildDepartureGroungRun( runwayObj , badaAircraft , airportObj )
                                    overshoot = ( totalGroundLegLengthMeters > runwayObj.getLengthMeters() )
                                    
                                    response_data = {
                                                    'aircraft ICAO'           : '{0}'.format( badaSynonymAircraft.getICAOcode() ), 
                                                    'aircraft'                : '{0}'.format( badaSynonymAircraft.getAircraftFullName() ), 
                                                    'aircraft TakeOff Mass Kg'   : '{0}'.format( badaAircraft.getAircraftInitialMassKilograms() ),
                                                    'airport'                    : '{0}'.format( airportObj ) , 
                                                    'runway'                     : '{0}'.format( runwayObj ) , 
                                                    'runway Length Meters'                  : '{0:.2f}'.format( runwayObj.getLengthMeters() ) ,
                                                    'TakeOff Stall Speed Cas Knots'         : '{0:.2f}'.format( takeOffStallSpeedCasKnots ),
                                                    'TakeOff True AirSpeed MetersPerSecond' : '{0:.2f}'.format( trueAirSpeedMetersSecond ) ,
                                                    'ground Run Length Meters'              : '{0:.2f}'.format( totalGroundLegLengthMeters ) ,
                                                    'overshoot'                  : str(overshoot)
                                                    }
                                    return JsonResponse(response_data)
                                
                                else:
                                    logger.info ('TakeOff mass must be greaterOrEqual to = {0} and lowerOrEqual to = {1}'.format(minTakeOffMassKg , maxTakeOffMassKg))
                                    response_data = {'errors' : 'TakeOff mass must be greaterOrEqual to = {0} and lowerOrEqual to = {1}'.format(minTakeOffMassKg , maxTakeOffMassKg)}
                                    return JsonResponse(response_data)
                                
                            else:
                                logger.info ('Runway  not found = {0}'.format(runway))
                                response_data = {'errors' : 'Runway not found = {0}'.format(runway)}
                                return JsonResponse(response_data)
                            
                        else:
                            logger.info ('Aircraft  not found = {0}'.format(aircraft))
                            response_data = {'errors' : 'Aircraft not found = {0}'.format(aircraft)}
                            return JsonResponse(response_data)
                        
                    else:
                        logger.info ('Airport  not found = {0}'.format(airport))
                        response_data = {'errors' : 'Airport not found = {0}'.format(airport)}
                        return JsonResponse(response_data)
                else:
                    logger.info("Ac Performance read failed = {0}".format(badaSynonymAircraft.getAircraftPerformanceFile()))
                    response_data = { 'errors' : "Ac Performance read failed = {0}".format(badaSynonymAircraft.getAircraftPerformanceFile())}
                    return JsonResponse(response_data)
                                                                                           
            else:
                logger.info ('Aircraft  not found = {0}'.format(aircraft))
                response_data = {'errors' : 'Aircraft not found = {0}'.format(aircraft)}
                return JsonResponse(response_data)
                
        else:
            logger.info ('airline  not found = {0}'.format(airline))
            response_data = {'errors' : 'Airline not found = {0}'.format(airline)}
            return JsonResponse(response_data)
            
    else:
        logger.debug ('expecting a GET - received something else = {0}'.format(request.method))
        response_data = { 'errors' : 'expecting a GET - received something else = {0}'.format(request.method) }
        return JsonResponse(response_data)
