'''
Created on 16 janv. 2024

@author: robert
for each airline, for each aircraft, for each flight leg compute
1) flight leg duration in seconds
2) Take off Mass 
3) Final Mass Kg to compute Kerosene used
') fuel savings according to reduced climb power

'''

from time import time
from django.core.management.base import BaseCommand
from airline.models import Airline, AirlineAircraft, AirlineRoute, AirlineCosts
from trajectory.models import BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.Guidance.FlightPathFile import FlightPath

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    
    help = 'Compute the Airline costs'

    def handle(self, *args, **options):
        
        start_time = time()
        
        for airline in Airline.objects.all():
            logger.info ( airline )
            
            for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
                logger.info ( airlineAircraft )
                aircraftICAOcode = airlineAircraft.aircraftICAOcode
                badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
                if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):

                    logger.info ("selected aircraft = {0}".format( aircraftICAOcode ) )
                
                    for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                        
                        adepRunway = airlineRoute.computeBestDepartureRunWay()
                        adesRunway = airlineRoute.computeBestArrivalRunWay()
                        logger.info ( airlineRoute )
                        
                        ''' 30th April 2023 - compute route with best runways '''
                        routeAsString = airlineRoute.getRouteAsString(AdepRunWayName=adepRunway, AdesRunWayName=adesRunway, direct=False)
                        logger.info ( routeAsString )
                        
                        acPerformance = AircraftJsonPerformance(aircraftICAOcode, badaAircraft.getAircraftJsonPerformanceFile())
                        if ( acPerformance.read() ):
                            #print ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                            #print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )
                            
                            for reducedClimbPowerCoeff in range(16):
                            
                                flightPath = FlightPath(
                                        route = routeAsString, 
                                        aircraftICAOcode = aircraftICAOcode,
                                        RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet() / 100., 
                                        cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                        takeOffMassKilograms = acPerformance.getReferenceMassKilograms(),
                                        reducedClimbPowerCoeff = float(reducedClimbPowerCoeff))
        
                                abortedFlight = flightPath.computeFlight(deltaTimeSeconds = 1.0)
                                if ( abortedFlight == False ):
                                    raise ValueError( "flight did not go to a normal end")

        end_time = time()
        seconds_elapsed = end_time - start_time

        hours, rest = divmod(seconds_elapsed, 3600)
        minutes, seconds = divmod(rest, 60)
        print ( "hours = {0} - minutes = {1} - seconds = {2}".format( hours, minutes, seconds))