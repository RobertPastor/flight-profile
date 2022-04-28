
import time

from django.core.management.base import BaseCommand
from trajectory.models import BadaSynonymAircraft
from airline.models import AirlineRoute
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.Guidance.FlightPathFile import FlightPath


class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        t0 = time.clock()
        
        aircraftICAOcode = 'A320'
        route = 'KATL-KLAX'
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            print ( badaAircraft )
            Adep = str(route).split("-")[0]
            Ades = str(route).split("-")[1]
            airlineRoute = AirlineRoute.objects.all().filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
            if ( airlineRoute ):
                routeAsString = airlineRoute.getRouteAsString()
                print ( routeAsString )
                acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
                print ( "Max TakeOff Weight kilograms = {0}".format(acPerformance.getMaximumMassKilograms() ) )   
                print ( "Max Operational Altitude Feet = {0}".format(acPerformance.getMaxOpAltitudeFeet() ) )   

                flightPath = FlightPath(
                                route = routeAsString, 
                                aircraftICAOcode = aircraftICAOcode,
                                RequestedFlightLevel = acPerformance.getMaxOpAltitudeFeet()/100., 
                                cruiseMach = acPerformance.getMaxOpMachNumber(), 
                                takeOffMassKilograms = acPerformance.getMaximumMassKilograms())

                flightPath.computeFlight(deltaTimeSeconds = 1.0)
                print ( 'simulation duration= ' + str(time.clock()-t0) + ' seconds' )
    
                print ( "=========== Flight Plan create output files  =========== " )
    
                flightPath.createFlightOutputFiles()
                print ( "=========== Flight Plan end  =========== "  )
                
            else:
                print ('airline route not found = {0}'.format(route))
        else:
            print ("aircraft with ICAO code = {0} not found".format(aircraftICAOcode))
            print ("or aircraft performance file = {0} not found".format(badaAircraft))
            
            