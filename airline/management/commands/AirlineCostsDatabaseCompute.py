'''
Created on 26 janv. 2023

@author: robert

for each airline, for each aircraft, for each flight leg compute
1) flight leg duration in seconds
2) Take off Mass 
3) Final Mass Kg to compute Kerosene used

'''
from django.core.management.base import BaseCommand
from airline.models import Airline, AirlineAircraft, AirlineRoute, AirlineCosts
from trajectory.models import BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.Guidance.FlightPathFile import FlightPath

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Compute the Airline costs'

    def handle(self, *args, **options):
        
        AirlineCosts.objects.all().delete()
        
        for airline in Airline.objects.all():
            logger.info ( airline )
            
            for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
                logger.info ( airlineAircraft )
                aircraftICAOcode = airlineAircraft.aircraftICAOcode
                badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
                if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):

                    logger.info ("selected aircraft = {0}".format( aircraftICAOcode ) )
                
                    for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                        logger.info ( airlineRoute )
                        
                        routeAsString = airlineRoute.getRouteAsString()
                        logger.info ( routeAsString )
                        acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
                        #print ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                        #print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
                        
                        flightPath = FlightPath(
                                route = routeAsString, 
                                aircraftICAOcode = aircraftICAOcode,
                                RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet() / 100., 
                                cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                takeOffMassKilograms = acPerformance.getMaximumMassKilograms())

                        flightPath.computeFlight(deltaTimeSeconds = 1.0)
                        airlineCosts = AirlineCosts(
                                    airline = airline ,
                                    airlineAircraft = airlineAircraft,
                                    airlineRoute = airlineRoute,
                                    isAborted = flightPath.abortedFlight,
                                    flightDurationSeconds = flightPath.getFlightDurationSeconds(),
                                    initialTakeOffMassKg = flightPath.aircraft.getAircraftInitialMassKilograms(),
                                    finalMassKg =  flightPath.aircraft.getAircraftCurrentMassKilograms() ,
                                    )
                        airlineCosts.save()
        