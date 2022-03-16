
from django.core.management.base import BaseCommand
from airline.management.commands.AirlineRoutesWayPoints.AirlineRoutesWayPointsReader import AirlineRoutesWayPointsDatabase
from airline.models import AirlineRouteWayPoints

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        AirlineRouteWayPoints.objects.all().delete()
        airlineRoutesWayPointsDatabase = AirlineRoutesWayPointsDatabase()
        if airlineRoutesWayPointsDatabase.exists():
            print("airline routes waypoints database exists")
            ret = airlineRoutesWayPointsDatabase.load()
            print ("load airline routes WayPoints database result = {0}".format(ret))
        else:
            print("airline routes database does not exists")
            
        return
    