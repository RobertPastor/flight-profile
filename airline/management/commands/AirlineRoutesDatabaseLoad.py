
from django.core.management.base import BaseCommand
from airline.management.commands.AirlineRoutes.AirlineRoutesAirportsReaderNew import AirlineRoutesDataBaseXlsx

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
                
        airlineRoutesDB = AirlineRoutesDataBaseXlsx()
        if (airlineRoutesDB.exists()):
            
            print("airline routes database exists")
            
            ret = airlineRoutesDB.createAirlineRoutes()
            
            print ("read airline routes database result = {0}".format(ret))
            
        else:
            print("airline routes database does not exists")
            
        return
    