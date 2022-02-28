
from django.core.management.base import BaseCommand

from trajectory.management.commands.Airports.AirportDatabaseFile import AirportsDatabase

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        airportsBD = AirportsDatabase()
        if (airportsBD.exists()):
            print("airports database exists")
            ret = airportsBD.read()
            print ("read airports database result = {0}".format(ret))
        else:
            print("airports database does not exists")
            
            