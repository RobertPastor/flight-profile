
from django.core.management.base import BaseCommand

from trajectory.management.commands.WayPoints.WayPointsDatabaseFile  import WayPointsDatabase

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        wayPointsBD = WayPointsDatabase()
        if (wayPointsBD.exists()):
            print("acBD exists")
            ret = wayPointsBD.read()
            print ("read wayPoints database result = {0}".format(ret))
        else:
            print("wayPoints database does not exists")