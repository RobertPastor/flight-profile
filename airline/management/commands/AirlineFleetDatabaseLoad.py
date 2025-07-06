from django.core.management.base import BaseCommand

from airline.management.commands.AirlineFleet.AirlineFleetReaderXlsx import AirlineFleetDataBase
from trajectory.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase


class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        
        #AirlineAircraft.objects.all().delete()
        
        airlineFleetDatabase = AirlineFleetDataBase()
        badaAircraftDatabase = BadaAircraftDatabase()
        if (airlineFleetDatabase.exists() and badaAircraftDatabase.exists()):
            print("airline fleet database exists")
            ret = badaAircraftDatabase.read()
            print("Bada aircraft database read correctly = {0}".format(ret))
            ret = airlineFleetDatabase.read()
            print ("read airline fleet database result = {0}".format(ret))
            
        else:
            print("airline fleet database does not exists")
            
        return