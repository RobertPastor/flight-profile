
from time import time

from django.core.management.base import BaseCommand
from trajectory.models import BadaSynonymAircraft
from airline.models import AirlineRoute
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.Guidance.FlightPathFile import FlightPath
from trajectory.Environment.Constants import Meter2NauticalMiles

class Command(BaseCommand):
    help = 'Coùputes one predefined trajectory for test purpose only'

    def handle(self, *args, **options):
        
        start_time = time()
        
        aircraftICAOcode = 'A320'
        route = 'KLAX-KATL'
        route = "MMMX-KSEA"
        route = "LEMD-EDDB"
        AdepRunway = "36R"
        AdesRunway = "25L"
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            print ( badaAircraft )
            Adep = str(route).split("-")[0]
            Ades = str(route).split("-")[1]
            airlineRoute = AirlineRoute.objects.all().filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
            if ( airlineRoute ):
                routeAsString = airlineRoute.getRouteAsString( AdepRunWayName = AdepRunway, AdesRunWayName = AdesRunway )
                print ( routeAsString )
                acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
                print ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   
                print ( "Cruise Mach = {0}".format(acPerformance.getMaxOpMachNumber() ) )   

                flightPath = FlightPath(
                                route = routeAsString, 
                                aircraftICAOcode = aircraftICAOcode,
                                RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet() / 100., 
                                cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                takeOffMassKilograms = 67000.0)

                flightPath.computeFlight(deltaTimeSeconds = 1.0)
                
                print ( "distance flown = {0} meters - {1} NM".format( flightPath.flightLengthMeters , flightPath.flightLengthMeters * Meter2NauticalMiles ))
    
                print ( "=========== Flight Plan create output files  =========== " )
    
                #flightPath.createFlightOutputFiles()
                #flightPath.createXlsOutputFile()
                #flightPath.createStateVectorOutputFile()
                print ( "=========== Flight Plan end  =========== "  )
                
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
            
            