
from time import time
import cProfile
import pstats
from io import StringIO
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
    
    def commandComputeWrap(self):
        
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

        if aircraftICAOcode in available_acs:
        
            ac = OpenapAircraft( aircraftICAOcode , earth , atmosphere , initialMassKilograms = None)
            logging.info( ac.getAircraftName())

            takeOffWeightKg = ac.getReferenceMassKilograms()
            logging.info("take off weight = {0:.2f} kg".format( takeOffWeightKg ))
            cruiseFlightLevel = ac.getMaxCruiseAltitudeFeet() / 100.0
            logging.info("cruise level FL = {0:.2f} ".format ( cruiseFlightLevel ) )
            
            targetCruiseMach = ac.getMaximumSpeedMmoMach()
            logging.info( "target cruise mach = {0:.2f} ".format( targetCruiseMach ) )
            
            if not ( aircraftICAOcode in prop.available_aircraft(use_synonym=True) ):
                logging.error( "Aircraft code = {0} not in openap Wrap".format( aircraftICAOcode ))
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
                        logging.info ( "hours = {0} - minutes = {1} - seconds = {2:.2f}".format( hours, minutes, seconds))
                        
                        
                        #flightPath.createStateVectorHistoryFile()
                        #flightPath.createKmlXmlDocument()
                    
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
        

    def handle(self, *args, **options):
        ''' start profiling '''
        profiler = cProfile.Profile()
        profiler.enable()
        
        logging.basicConfig(level=logging.INFO)
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.DEBUG)
        
        ''' launch the command '''
        self.commandComputeWrap()
        
        profiler.disable()
        s = StringIO()
        ps = pstats.Stats(profiler, stream=s).sort_stats('cumulative')
        ps.print_stats()

        # Output profiling results
        self.stdout.write(s.getvalue())
            
            