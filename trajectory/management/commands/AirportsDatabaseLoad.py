
from django.core.management.base import BaseCommand
from trajectory.management.commands.Airports.AirportDatabaseFile import AirportsDatabase
from trajectory.models import Airport
from airline.models import AirlineRoute

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        Airport.objects.all().delete()
        
        ''' load only airports defined in the airline routes '''
        airlineRoutes = AirlineRoute()
        airlineRoutesAirportsList = airlineRoutes.getAirportsList()

        airportsBD = AirportsDatabase()
        if (airportsBD.exists()):
            print("airports database exists")
            ret = airportsBD.read(airlineRoutesAirportsList)
            print ("read airports database result = {0}".format(ret))
        else:
            print("airports database does not exists")
            
        return