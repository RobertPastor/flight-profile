
from time import time

import logging


from django.core.management.base import BaseCommand
from airline.models import AirlineRoute

from trajectory.GuidanceOpenap.FlightPathOpenapFile import FlightPathOpenap
from trajectory.Openap.AircraftMainFile import OpenapAircraft

from trajectory.Environment.Earth import Earth
from trajectory.Environment.Atmosphere import Atmosphere

from openap import prop


class Command(BaseCommand):
    help = 'Computes one predefined trajectory for test purpose only'

    def handle(self, *args, **options):
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        earth = Earth()
        atmosphere = Atmosphere()
        
        start_time = time()
        
        ''' warning : wrap aircraft code letters must be in lower case '''
        aircraftICAOcode = 'a320'
        #aircraftICAOcode = 'a332'
        
        logging.info("Trajectory Compute Wrap - " + aircraftICAOcode)
        route = 'KLAX-KATL'
        #route = "MMMX-KSEA"
        
        AdepRunway = "24R"
        #AdepRunway = "05L"
        
        AdesRunway = "26L"
        #AdesRunway = "16L"
        
        available_acs = prop.available_aircraft(use_synonym=True)

        for aircraftICAOcode in available_acs:
            
            if ( str( aircraftICAOcode ).lower() in ['a359','a388','b38m','b744','b748','b752','b763','b773','b77w','b788','b789','c550'] \
                 or str( aircraftICAOcode ).lower() in ['e145','glf6','a124','a306','a310','at72','at75','at76','b733','b735','b762','b77l'] \
                 or str ( aircraftICAOcode ).lower() in ['c25a','c525','c56x','crj2','crj9','e290','glf5','gl5t','gl6t','tj45','md11','pc24','su95','lj45','bx3m'] ):
                #pass
                continue
        
            ac = OpenapAircraft( aircraftICAOcode , earth , atmosphere , initialMassKilograms = None)
            logging.info( ac.getAircraftName())

            takeOffWeightKg = ac.getReferenceMassKilograms()
            logging.info("take off weight = {0:.2f} kg".format( takeOffWeightKg ))
            cruiseFlightLevel = ac.getMaxCruiseAltitudeFeet() / 100.0
            logging.info("cruise level FL = {0:.2f} ".format ( cruiseFlightLevel ) )
            
            targetCruiseMach = ac.getMaximumSpeedMmoMach()
            logging.info( "target cruise mach = {0:.2f} ".format( targetCruiseMach ) )
            
            if not ( aircraftICAOcode in prop.available_aircraft(use_synonym=True) ):
                print ( "Aircraft code = {0} not in openap Wrap".format( aircraftICAOcode ))
            else:
            
                Adep = str(route).split("-")[0]
                Ades = str(route).split("-")[1]
                airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
                if ( airlineRoute ):
                    ''' try with direct route '''
                    routeAsString = airlineRoute.getRouteAsString( AdepRunWayName = AdepRunway, AdesRunWayName = AdesRunway , direct = False)
                    logging.info ( "Trajectory Compute Wrap - " + routeAsString )
                    
                    flightPath = FlightPathOpenap(
                            route                = routeAsString, 
                            aircraftICAOcode     = aircraftICAOcode,
                            RequestedFlightLevel = cruiseFlightLevel, 
                            cruiseMach           = targetCruiseMach, 
                            takeOffMassKilograms = takeOffWeightKg)
                    try:
                        flightPath.computeFlight(deltaTimeSeconds = 1.0)
                        
                        end_time = time()
                        seconds_elapsed = end_time - start_time
                    
                        hours, rest = divmod(seconds_elapsed, 3600)
                        minutes, seconds = divmod(rest, 60)
                        print ( "hours = {0} - minutes = {1} - seconds = {2:.2f}".format( hours, minutes, seconds))
                    
                        flightPath.createStateVectorHistoryFile()
                        flightPath.createKmlXmlDocument()
                    
                    except Exception as e:
                        logging.error("Trajectory Compute Wrap - Exception = {0}".format( str(e ) ) )

                    #print ( "Trajectory Compute - distance flown = {0:.2f} meters - {1:.2f} Nm".format( flightPath.flightLengthMeters , flightPath.flightLengthMeters * Meter2NauticalMiles ))
                    
                    end_time = time()
                    seconds_elapsed = end_time - start_time
                    
                    hours, rest = divmod(seconds_elapsed, 3600)
                    minutes, seconds = divmod(rest, 60)
                    print ( "hours = {0} - minutes = {1} - seconds = {2}".format( hours, minutes, seconds))
                    
                else:
                    print ('airline route not found = {0}'.format(route))
            
            