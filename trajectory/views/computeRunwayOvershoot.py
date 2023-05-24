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
        
    print ( '================ get aircraft =================' )
    atmosphere = Atmosphere()
    earth = Earth()
    acBd = BadaAircraftDatabase()
    assert acBd.read()
        
    if ( acBd.aircraftExists( aircraftICAOcode ) and
        acBd.aircraftPerformanceFileExists( aircraftICAOcode)):
            
        print ( 'performance file= {0}'.format(acBd.getAircraftPerformanceFile(aircraftICAOcode)) )
        aircraft = BadaAircraft(ICAOcode = aircraftICAOcode, 
                                        aircraftFullName = acBd.getAircraftFullName(aircraftICAOcode),
                                        badaPerformanceFilePath = acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                        atmosphere = atmosphere,
                                        earth = earth)
        aircraft.dump()
        return aircraft
    else:
        raise ValueError( 'aircraft not found= ' + aircraftICAOcode)
    
    
def buildGroungRun(departureRunway , aircraft , departureAirport):
    ''' 
        this function manages the departure phases with a ground run 
    '''
        
    print (  ' ============== build the departure ground run =========== '  )
    finalRoute = GroundRunLeg(runway = departureRunway, aircraft = aircraft, airport = departureAirport)
        
    distanceToLastFixMeters = 10000.0
    distanceStillToFlyMeters = 10000.0
    flightLengthMeters = 10000.0

    elapsedTimeSeconds = 0.0
    deltaTimeSeconds = 1.0
    
    finalRoute.buildDepartureGroundRun(deltaTimeSeconds  = deltaTimeSeconds,
                                                elapsedTimeSeconds = elapsedTimeSeconds,
                                                distanceStillToFlyMeters = distanceStillToFlyMeters,
                                                distanceToLastFixMeters = distanceToLastFixMeters)
    
    distanceStillToFlyMeters = flightLengthMeters - finalRoute.getLengthMeters()

    #logging.info '==================== end of ground run ==================== '
    initialWayPoint = finalRoute.getLastVertex().getWeight()
    print ( initialWayPoint )
    return finalRoute.getTotalLegDistanceMeters()


def computeRunwayOvershoot(request, aircraft , airport, runway , mass):
    pass
    print ( "aircraft = {0} - airport = {1} - runway name = {2} - mass ={3} tons".format( aircraft , airport , runway , mass) )
    
    logger.setLevel(logging.DEBUG)

    if request.method == 'GET':

        airline = Airline.objects.first()
        if ( airline ):
            print ( airline )
                
            badaSynonymAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraft).first()
            if ( badaSynonymAircraft and badaSynonymAircraft.aircraftPerformanceFileExists()):
                
                acPerformance = AircraftPerformance(badaSynonymAircraft.getAircraftPerformanceFile()) 

                print ("selected aircraft = {0}".format( badaSynonymAircraft ) )
                
                airportObj = AirlineAirport.objects.filter(AirportICAOcode = airport).first()
                if ( airportObj ):
                    print (airportObj)
                    
                    badaAircraft = getBadaAircraft ( aircraft )
                    if ( badaAircraft ):
                        
                        runwayObj = AirlineRunWay.objects.filter( Airport = airportObj, Name = runway ).first()
                        print ( "Airline runway = {0}".format ( runway ) )
                        
                        if ( runwayObj ):
                            ''' convert to environment runway '''
                            runwayObj = runwayObj.convertToEnvRunway()
                        
                            #print ( "Trajectory Environment RunWay = {0}".format ( runwayObj ) )
                            
                            maxTakeOffMassKg = acPerformance.getMaximumMassKilograms()
                            minTakeOffMassKg = acPerformance.getMinimumMassKilograms()
                            #print ( "takeoff maximum mass kg = {0}".format ( maxTakeOffMassKg ) )
                            
                            if ( ( float ( mass ) * 1000.0 ) >= minTakeOffMassKg ) and  ( ( float ( mass ) * 1000.0 ) <= maxTakeOffMassKg ):
                                
                                badaAircraft.setAircraftMassKilograms( float ( mass ) * 1000.0 )
                                badaAircraft.setDepartureGroundRunConfiguration( 0.0 )
                                
                                takeOffStallSpeedCasKnots = badaAircraft.computeStallSpeedCasKnots()
                                print ( "TakeOff Stall speed = {0} Kcas Knots".format( badaAircraft.computeStallSpeedCasKnots() ) )
                                
                                airportObj = airportObj.convertToEnvAirport()
                                
                                ''' build the ground run '''
                                totalGrounLegLengthMeters = buildGroungRun( runwayObj , badaAircraft , airportObj )
                                
                                response_data = {
                                                'aircraft'                : '{0}'.format( badaSynonymAircraft ), 
                                                'aircraftReferenceMassKg' : '{0}'.format( acPerformance.getReferenceMassTons() * 1000.0 ),
                                                'aircraftInitialMassKg'   : '{0}'.format( badaAircraft.getAircraftInitialMassKilograms() ),
                                                'airport'                 : '{0}'.format( airportObj ) , 
                                                'runway'                  : '{0}'.format( runwayObj ) , 
                                                'runwayLengthMeters'      : '{0}'.format( round ( runwayObj.getLengthMeters() , 2 ) ),
                                                'TakeOffStallSpeedCasKnots'      : '{0}'.format( round ( takeOffStallSpeedCasKnots , 2 ) ),
                                                'groundRunLengthMeters'   : '{0}'.format( round ( totalGrounLegLengthMeters , 2 ) )
                                                }
                                return JsonResponse(response_data)
                            
                            else:
                                print ('TakeOff mass must be greaterOrEqual to = {0} and lowerOrEqual to = {1}'.format(minTakeOffMassKg , maxTakeOffMassKg))
                                response_data = {'errors' : 'TakeOff mass must be greaterOrEqual to = {0} and lowerOrEqual to = {1}'.format(minTakeOffMassKg , maxTakeOffMassKg)}
                                return JsonResponse(response_data)
                            
                        else:
                            print ('Runway  not found = {0}'.format(runway))
                            response_data = {'errors' : 'Runway not found = {0}'.format(runway)}
                            return JsonResponse(response_data)
                        
                    else:
                        print ('Aircraft  not found = {0}'.format(aircraft))
                        response_data = {'errors' : 'Aircraft not found = {0}'.format(aircraft)}
                        return JsonResponse(response_data)
                    
                else:
                    print ('Airport  not found = {0}'.format(airport))
                    response_data = {'errors' : 'Airport not found = {0}'.format(airport)}
                    return JsonResponse(response_data)
            
            else:
                print ('Aircraft  not found = {0}'.format(aircraft))
                response_data = {'errors' : 'Aircraft not found = {0}'.format(aircraft)}
                return JsonResponse(response_data)
                
        else:
            print ('airline  not found = {0}'.format(airline))
            response_data = {'errors' : 'Airline not found = {0}'.format(airline)}
            return JsonResponse(response_data)
            
    else:
        logger.info ('expecting a GET - received something else = {0}'.format(request.method))
        response_data = {
                        'errors' : 'expecting a GET - received something else = {0}'.format(request.method)}
        return JsonResponse(response_data)
