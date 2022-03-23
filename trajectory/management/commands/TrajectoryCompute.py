
from django.core.management.base import BaseCommand
from trajectory.models import Aircraft, Airport, RunWay
from airline.models import AirlineRoute

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        acICAOcode = 'A320'
        route = 'KATL-KLAX'
        badaAircraft = Aircraft.objects.all().filter(AircraftICAOcode=acICAOcode).first()
        if ( badaAircraft ):
            print ( badaAircraft )
            Adep = str(route).split("-")[0]
            Ades = str(route).split("-")[1]
            airlineRoute = AirlineRoute.objects.all().filter(DepartureAirportICAOCode=Adep, ArrivalAirportICAOCode=Ades).first()
            if ( airlineRoute ):
                print ( airlineRoute )
                Adep = Airport.objects.all().filter(AirportICAOcode=Adep).first()
                Ades = Airport.objects.all().filter(AirportICAOcode=Ades).first()
                if ( Adep and Ades ):
                    print ("Adep= {0} - Ades= {1}".format(Adep,Ades)  )
                    AdepRunWay = RunWay.objects.all().filter(Airport=Adep).first()
                    AdesRunWay = RunWay.objects.all().filter(Airport=Ades).first()
                    if ( AdepRunWay and AdesRunWay):
                        print ("Adep runway= {0} - Ades runway= {1}".format(AdepRunWay,AdesRunWay))
                    else:
                        print ("either Adep runway or Ades runway not found")
                else:
                    print ("either Adep or Ades not found in Airport database")
            else:
                print ('airline route not found = {0}'.format(route))
        else:
            print ("aircraft with ICAO code = {0} not found".format(acICAOcode))
            
            