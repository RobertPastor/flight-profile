'''
Created on 27 sept. 2024

@author: robert
'''


from django.core.management.base import BaseCommand
from trajectory.Environment.WindTemperature.NoaaStations.NoaaWeatherStationsFile import NoaaWeatherStationsClass

from trajectory.Guidance.ConstraintsFile import Meters2Feet
from trajectory.Guidance.WayPointFile import WayPoint
from trajectory.models import NoaaWeatherStationMeasure
from trajectory.models import NoaaWeatherStation

class Command(BaseCommand):
    help = 'Load the Wind Temperature data'

    def handle(self, *args, **options):
        
        fileName = "noaa-stations.json"
    
        noaaStations = NoaaWeatherStationsClass( fileName )
        noaaStations.readStations()
        
        print ( "is station FAA name DEN existing = " + str(noaaStations.isStationFAAExisting( "DEN")) )
        
        stationICAOname = "KDEN"
        print( "is station ICAO KDEN existing = " + str(noaaStations.isStationICAOExisting( "KDEN")) )
        
        print ( "get DEN ICAO station = " + str(noaaStations.getStationICAOName( "DEN") ) )
        
        stationFAAname = "DEN"
        print ( "station = {0} - latitude degrees = {1}".format( stationFAAname , noaaStations.getStationLatitudeDegrees( stationFAAname ) ) )
        print ( "station = {0} - longitude degrees = {1}".format( stationFAAname , noaaStations.getStationLongitudeDegrees( stationFAAname ) ) )
        print ( "station = {0} - elevation meters = {1}".format( stationFAAname , noaaStations.getStationElevationMeters( stationFAAname ) ) )
        print ( "station = {0} - elevation feet = {1}".format( stationFAAname , noaaStations.getStationElevationFeet( stationFAAname ) ) )
        
        stationFAAname = "JFK"
        print ( "station = {0} - elevation meters = {1}".format( stationFAAname , noaaStations.getStationElevationMeters( stationFAAname ) ) )
        
        currentPosition = WayPoint(Name = "NearKATL",
                                               LatitudeDegrees = 33.70,
                                               LongitudeDegrees = -84.500,
                                               AltitudeMeanSeaLevelMeters = 0.0)
        print ( "nearest weather station = {0}".format ( noaaStations.getNearestWeatherStationICAOname(currentPosition) ) )
