
from django.core.management.base import BaseCommand
from trajectory.management.commands.WayPoints.WayPointsDatabaseFileXlsx  import WayPointsDatabaseXlsx
from trajectory.models import AirlineWayPoint

class Command(BaseCommand):
    help = 'Reads the WayPoints and write in a table'

    def handle(self, *args, **options):
        
        print ( " --- about to delete --- ")
        AirlineWayPoint.objects.all().delete()
        print ( " delete done")

        wayPointsBD = WayPointsDatabaseXlsx()
        if (wayPointsBD.exists()):
            print("acBD exists")
            ret = wayPointsBD.read()
            print ("read wayPoints database result = {0}".format(ret))
        else:
            print("wayPoints database does not exists")