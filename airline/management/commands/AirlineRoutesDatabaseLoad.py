
from django.core.management.base import BaseCommand

from airline.management.commands.AirlineRoutes.AirlineRoutesAirportsReader import AirlineRoutesDataBase

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        airlineRoutes = AirlineRoutesDataBase()
        if (airlineRoutes.exists()):
            print("airline routes database exists")
            ret = airlineRoutes.read()
            print ("read airline routes database result = {0}".format(ret))
        else:
            print("airline routes database does not exists")
            
        return
    