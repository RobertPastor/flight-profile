
from django.core.management.base import BaseCommand
from airline.management.commands.AirlineRoutesWayPoints.AirlineRoutesWayPointsReaderNew import AirlineRoutesWayPointsDatabaseXlsx
from airline.models import AirlineRouteWayPoints
from airline.management.commands.AirlineRoutesWayPoints.WayPointsDatabaseFile import WayPointsDatabase

class Command(BaseCommand):
    help = 'Reads the WayPoints of the Routes '

    def handle(self, *args, **options):
        
        AirlineRouteWayPoints.objects.all().delete()
        
        wayPointsDatabase = WayPointsDatabase()
        if not wayPointsDatabase.exists():
            print ("WayPoints EXCEL database is not existing")
            wayPointsDatabase.create()
            
        
        airlineRoutesWayPointsDatabaseXlsx = AirlineRoutesWayPointsDatabaseXlsx()
        if (airlineRoutesWayPointsDatabaseXlsx.exists()):
            pass
            ret = airlineRoutesWayPointsDatabaseXlsx.read()
            
            if ret:
                airlineRoutesWayPointsDatabaseXlsx.insertWayPointsDatabase(wayPointsDatabase)
            
        #airlineRoutesWayPointsDatabase = AirlineRoutesWayPointsDatabase()
        #if airlineRoutesWayPointsDatabase.exists():
            
        #    ''' create the EXCEL files containing the WayPoints '''
        #    airlineRoutesWayPointsDatabase.createRoutesFiles()
                
        #    print("airline routes waypoints database exists")
        #    ret = airlineRoutesWayPointsDatabase.load()
        #    print ("load airline routes WayPoints database result = {0}".format(ret))
                
        #    airlineRoutesWayPointsDatabase.fillWayPointsFile(wayPointsDatabase)
                
        #else:
        #    print("airline routes database does not exists")
                
        
        #wayPointsDatabase.dropDuplicates()
        return
        
        
            
    
    