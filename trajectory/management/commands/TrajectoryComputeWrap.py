
from time import time

import logging


from django.core.management.base import BaseCommand
from airline.models import AirlineRoute

from trajectory.GuidanceOpenap.FlightPathOpenapFile import FlightPathOpenap
from openap import prop


class Command(BaseCommand):
    help = 'Computes one predefined trajectory for test purpose only'

    def handle(self, *args, **options):
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        #handler = logging.StreamHandler()
        #logger.addHandler(handler)
        
        start_time = time()
        
        ''' warning letters in aircraft code must be in lower case '''
        aircraftICAOcode = 'a320'
        logging.info("Trajectory Compute Wrap - " + aircraftICAOcode)
        route = 'KLAX-KATL'
        
        AdepRunway = "24R"
        AdesRunway = "26L"
        
        if not ( aircraftICAOcode in prop.available_aircraft(use_synonym=True) ):
            print ( "Aircraft code = {0} not in openap Wrap".format( aircraftICAOcode ))
        else:
            
            Adep = str(route).split("-")[0]
            Ades = str(route).split("-")[1]
            airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
            if ( airlineRoute ):
                ''' try with direct route '''
                routeAsString = airlineRoute.getRouteAsString( AdepRunWayName = AdepRunway, AdesRunWayName = AdesRunway , direct = True)
                logging.info ( "Trajectory Compute Wrap - " + routeAsString )
                
                flightPath = FlightPathOpenap(
                        route                = routeAsString, 
                        aircraftICAOcode     = aircraftICAOcode,
                        RequestedFlightLevel = 330.0, 
                        cruiseMach           = 0.82, 
                        takeOffMassKilograms = 62000.0)
                try:
                    flightPath.computeFlight(deltaTimeSeconds = 1.0)
                except:
                    flightPath.createStateVectorOutputFile()

                
                #print ( "Trajectory Compute - distance flown = {0:.2f} meters - {1:.2f} Nm".format( flightPath.flightLengthMeters , flightPath.flightLengthMeters * Meter2NauticalMiles ))
                
                end_time = time()
                seconds_elapsed = end_time - start_time
                
                hours, rest = divmod(seconds_elapsed, 3600)
                minutes, seconds = divmod(rest, 60)
                print ( "hours = {0} - minutes = {1} - seconds = {2}".format( hours, minutes, seconds))
                    
            else:
                print ('airline route not found = {0}'.format(route))
            
            