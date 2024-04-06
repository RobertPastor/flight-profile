
from time import time

from django.core.management.base import BaseCommand
from trajectory.models import BadaSynonymAircraft
from airline.models import AirlineRoute
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.Guidance.FlightPathFile import FlightPath
from trajectory.Environment.Constants import Meter2NauticalMiles

class Command(BaseCommand):
    help = 'Computes one predefined trajectory for test purpose only'

    def handle(self, *args, **options):
        
        start_time = time()
        
        aircraftICAOcode = 'A320'
        route = 'KLAX-KATL'
        
        AdepRunway = "24R"
        AdesRunway = "26L"
        badaAircraft = BadaSynonymAircraft.objects.filter(AircraftICAOcode=aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftJsonPerformanceFileExists()):
            print ( badaAircraft )
            Adep = str(route).split("-")[0]
            Ades = str(route).split("-")[1]
            airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
            if ( airlineRoute ):
                ''' try with direct route '''
                #routeAsString = airlineRoute.getDirectRouteAsString( AdepRunWayName = AdepRunway, AdesRunWayName = AdesRunway )
                routeAsString = airlineRoute.getRouteAsString( AdepRunWayName = AdepRunway, AdesRunWayName = AdesRunway , direct = True)
                print ( routeAsString )
                acPerformance = AircraftJsonPerformance(badaAircraft.getICAOcode(), badaAircraft.getAircraftJsonPerformanceFile())
                if acPerformance.read():
                    print ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                    print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
                    print ( "Cruise Mach = {0}".format(acPerformance.getMaxOpMachNumber() ) )   
    
                    flightPath = FlightPath(
                                    route                = routeAsString, 
                                    aircraftICAOcode     = aircraftICAOcode,
                                    RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet() / 100., 
                                    cruiseMach           = acPerformance.getMaxOpMachNumber(), 
                                    takeOffMassKilograms = acPerformance.getReferenceMassKilograms())
    
                    flightPath.computeFlight(deltaTimeSeconds = 1.0)
                    
                    print ( "Trajectory Compute - distance flown = {0:.2f} meters - {1:.2f} Nm".format( flightPath.flightLengthMeters , flightPath.flightLengthMeters * Meter2NauticalMiles ))
                    
                    end_time = time()
                    seconds_elapsed = end_time - start_time
            
                    hours, rest = divmod(seconds_elapsed, 3600)
                    minutes, seconds = divmod(rest, 60)
                    print ( "hours = {0} - minutes = {1} - seconds = {2}".format( hours, minutes, seconds))
                
            else:
                print ('airline route not found = {0}'.format(route))
        else:
            print ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
            print ("or aircraft performance file = {0} not found".format(badaAircraft))
            
            