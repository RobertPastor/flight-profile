'''
Created on 16 déc. 2022

@author: robert
'''

from airline.management.commands.AirlineRoutes.AirlineRoutesAirportsReaderNew import AirlineRoutesDataBaseXlsx
from airline.management.commands.AirlineRoutesWayPoints.AirlineOneRouteReaderFile import AirlineOneRouteReaderXlsx
#from airline.management.commands.AirlineRoutesWayPoints.WayPointsDatabaseFile import WayPointsDatabase

from airline.models import AirlineRoute, AirlineRouteWayPoints


class AirlineRoutesWayPointsDatabaseXlsx(object):
    pass

    def __init__(self):
        pass
        self.className = self.__class__.__name__
        
    def exists(self):
        airlineRoutes = AirlineRoutesDataBaseXlsx()
        return airlineRoutes.exists()
    
    def read(self):
        pass
        airlineRoutes = AirlineRoutesDataBaseXlsx()
        if (airlineRoutes.exists()):
            print("airline routes database exists")
            ret = airlineRoutes.read()
            
            if ret:
                for route in airlineRoutes.getICAORoutes():
                    print ( route )
                    oneAirlineRoute = AirlineOneRouteReaderXlsx()
                    oneAirlineRoute.read( route["Adep"] , route["Ades"] )
    
        return ret
    
    ''' loads the WayPoints xlsx database '''
    ''' loads the PostGres / MySQL airline routes WayPoints table '''
    def insertWayPointsDatabase(self):
        
        airlineRoutes = AirlineRoutesDataBaseXlsx()
        if (airlineRoutes.exists()):
            print("airline routes database exists")
            ret = airlineRoutes.read()
            
            if ret:
                for route in airlineRoutes.getICAORoutes():
                    print ( route )
                    
                    airlineRoute = AirlineRoute.objects.filter(DepartureAirportICAOCode = route["Adep"] , ArrivalAirportICAOCode = route["Ades"]).first()
                    if ( airlineRoute ):
                        
                        ''' delete old rows for this foreign key '''
                        AirlineRouteWayPoints.objects.filter(Route = airlineRoute).delete()
                    
                        oneAirlineRoute = AirlineOneRouteReaderXlsx()
                        df_route = oneAirlineRoute.read( route["Adep"] , route["Ades"] )
                        
                        index = 1
                        for index, row in df_route.iterrows():
                            #wayPointsDatabase.insertWayPoint(wayPointName = row["wayPoint"], Latitude = row["latitude"], Longitude = row["longitude"])
                            
                            airlineRouteWayPoints = AirlineRouteWayPoints(
                                Route = airlineRoute,
                                Order = index,
                                WayPoint = row["wayPoint"])
                            airlineRouteWayPoints.save()
                            index = index + 1
                
                    else:
                        print ("Airline Route not found - Adep = {0} - Ades = {1}".format(route["Adep"], route["Ades"]))
            else:
                print ("Error while reading the Airline Routes Database")
        else:
            print ("Error while reading Airline Routes Database")