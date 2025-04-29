
from time import time

from django.core.management.base import BaseCommand

from trajectory.Openap.AircraftMainFile import OpenapAircraft
from airline.models import AirlineRoute

from trajectory.GuidanceOpenap.FlightPathOpenapFile import FlightPathOpenap
from openap import prop

from trajectory.Environment.Constants import Meter2NauticalMiles

from trajectory.Environment.Earth import Earth
from trajectory.Environment.Atmosphere import Atmosphere

class Command(BaseCommand):
    help = 'Computes one predefined trajectory for test purpose only'

    def handle(self, *args, **options):
        
        start_time = time()
        
        earth = Earth()
        atmosphere = Atmosphere()
        ''' warning letters in aircraft code must be in mower case '''
        aircraftICAOcode = 'a320'
        route = 'KLAX-KATL'
        
        AdepRunway = "24R"
        AdesRunway = "26L"
        
        if not ( aircraftICAOcode in prop.available_aircraft(use_synonym=True) ):
            print ( "Aircraft code = {0} not in openap Wrap".format( aircraftICAOcode ))
        else:
        #badaAircraft = BadaSynonymAircraft.objects.filter(AircraftICAOcode=aircraftICAOcode).first()
            openapAircraft = OpenapAircraft( aircraftICAOcode , earth , atmosphere , initialMassKilograms = None)
            if ( openapAircraft ):
                print ( openapAircraft )
                Adep = str(route).split("-")[0]
                Ades = str(route).split("-")[1]
                airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
                if ( airlineRoute ):
                    ''' try with direct route '''
                    #routeAsString = airlineRoute.getDirectRouteAsString( AdepRunWayName = AdepRunway, AdesRunWayName = AdesRunway )
                    routeAsString = airlineRoute.getRouteAsString( AdepRunWayName = AdepRunway, AdesRunWayName = AdesRunway , direct = True)
                    print ( routeAsString )
                    
                    print ( "Max TakeOff Weight kilograms = {0}".format(openapAircraft.getMaximumTakeOffMassKilograms() ) )   
                    print ( "Max Cruise Altitude Feet = {0}".format(openapAircraft.getMaxCruiseAltitudeFeet() ) )   
                    print ( "Max Speed MMO Cruise Mach = {0}".format(openapAircraft.getMaximumSpeedMmoMach() ) )   
        
                    flightPath = FlightPathOpenap(
                                        route                = routeAsString, 
                                        aircraftICAOcode     = aircraftICAOcode,
                                        RequestedFlightLevel = openapAircraft.getMaxCruiseAltitudeFeet() / 100., 
                                        cruiseMach           = openapAircraft.getMaximumSpeedMmoMach(), 
                                        takeOffMassKilograms = openapAircraft.getReferenceMassKilograms())
        
                    flightPath.computeFlight(deltaTimeSeconds = 1.0)
                    
                    #print ( "Trajectory Compute - distance flown = {0:.2f} meters - {1:.2f} Nm".format( flightPath.flightLengthMeters , flightPath.flightLengthMeters * Meter2NauticalMiles ))
                    
                    end_time = time()
                    seconds_elapsed = end_time - start_time
                
                    hours, rest = divmod(seconds_elapsed, 3600)
                    minutes, seconds = divmod(rest, 60)
                    print ( "hours = {0} - minutes = {1} - seconds = {2}".format( hours, minutes, seconds))
                    
                else:
                    print ('airline route not found = {0}'.format(route))
            else:
                print ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
                print ("or aircraft performance file = {0} not found".format(openapAircraft))
            
            