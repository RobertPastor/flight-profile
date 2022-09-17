
from django.core.management.base import BaseCommand
from trajectory.management.commands.RunWays.RunWaysDatabaseFile import RunWaysDatabase
from trajectory.models import AirlineRunWay
from airline.models import AirlineRoute

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        
        AirlineRunWay.objects.all().delete()
        
        ''' load only run-ways for airports defined in the airline routes '''
        airlineRoutes = AirlineRoute()
        airlineRoutesAirportsList = airlineRoutes.getAirportsList()

        runwaysDB = RunWaysDatabase()
        if (runwaysDB.exists()):
            print("runwaysDB exists")
            ret = runwaysDB.read(airlineRoutesAirportsList)
            print ("read runways database result = {0}".format(ret))
        else:
            print("runwaysDB does not exists")
            
            