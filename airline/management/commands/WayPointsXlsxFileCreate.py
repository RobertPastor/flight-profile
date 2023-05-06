'''
Created on 1 mai 2023

@author: robert
'''

from django.core.management.base import BaseCommand
from airline.management.commands.AirlineRoutesWayPoints.WayPointsDatabaseFile import WayPointsDatabase

from airline.management.commands.AirlineRoutes.AirlineRoutesAirportsReaderNew import AirlineRoutesDataBaseXlsx
from airline.management.commands.AirlineRoutesWayPoints.AirlineOneRouteReaderFile import AirlineOneRouteReaderXlsx
from airline.models import AirlineRoute

''' this command uses as inputs all the EXCEL Routes with the wayPoints , lat/long as strings as available in the EXCEL Routes configuration files '''
class Command(BaseCommand):
    help = 'Reads the WayPoints of the Routes '

    def handle(self, *args, **options):
        
        wayPointsDatabase = WayPointsDatabase()
        if not wayPointsDatabase.exists():
            print ("WayPoints EXCEL database is not existing")
            wayPointsDatabase.create()
            
        ''' retrieve initial pandas dataframe '''
        df_source = wayPointsDatabase.getDataFrame()
            
        ''' loop through wayPoints '''
        airlineRoutes = AirlineRoutesDataBaseXlsx()
        if (airlineRoutes.exists()):
            print("airline routes database exists")
            ret = airlineRoutes.read()
            
            if ret:
                for route in airlineRoutes.getICAORoutes():
                    print ( route )
                    
                    airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode = route["Adep"] , ArrivalAirportICAOCode = route["Ades"]).first()
                    if ( airlineRoute ):
                    
                        oneAirlineRoute = AirlineOneRouteReaderXlsx()
                        df_route = oneAirlineRoute.read(route["Adep"] , route["Ades"] )
                        
                        index = 1
                        for index, row in df_route.iterrows():
                            print ( "{0} - {1}".format( str(index) , str(row)  ) )
                        
                            wayPointName = row["wayPoint"]
                            latitude     = row["latitude"]
                            longitude    = row["longitude"]
        
                            df_source = wayPointsDatabase.appendToDataFrame(df_source, wayPointName, latitude, longitude)
                            
        wayPointsDatabase.writeDataFrame(df_source)
        wayPointsDatabase.dropDuplicates()