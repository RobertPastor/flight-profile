'''
Created on 1 mai 2023

@author: robert
'''

import pandas as pd

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
        
        wayPointsList = []
            
        ColumnNames = wayPointsDatabase.getColumnNames()
        
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
                            
                            wayPoint = {}
                            wayPoint[ColumnNames[0]] = row["wayPoint"]
                            wayPoint[ColumnNames[1]] = "Unknown"
                            wayPoint[ColumnNames[2]] = "WayPoint"
                            wayPoint[ColumnNames[3]] = row["latitude"]
                            wayPoint[ColumnNames[4]] = row["longitude"]
                            wayPoint[ColumnNames[5]] = "Unknown Name"
                            wayPointsList.append(wayPoint)
        
                            #df_source = wayPointsDatabase.appendToDataFrame(df_source, wayPointName, latitude, longitude)
                            
        ''' this write operation is preceeded by a drop duplicates '''
        wayPointsDatabase.writeDataFrameFromList( wayPointsList )
        #wayPointsDatabase.dropDuplicates()