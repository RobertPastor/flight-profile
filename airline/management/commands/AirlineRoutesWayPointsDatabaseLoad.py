
from django.core.management.base import BaseCommand
from airline.management.commands.AirlineRoutesWayPoints.AirlineRoutesWayPointsReaderNew import AirlineRoutesWayPointsDatabaseXlsx
from airline.models import AirlineRouteWayPoints

class Command(BaseCommand):
    help = 'Reads the WayPoints of the Routes '

    def handle(self, *args, **options):
        
        #AirlineRouteWayPoints.objects.all().delete()
        
        airlineRoutesWayPointsDatabaseXlsx = AirlineRoutesWayPointsDatabaseXlsx()
        if (airlineRoutesWayPointsDatabaseXlsx.exists()):
            pass
            ret = airlineRoutesWayPointsDatabaseXlsx.read()
            
            if ret:
                airlineRoutesWayPointsDatabaseXlsx.insertWayPointsDatabase()
               
            
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
        
        
            
    
    