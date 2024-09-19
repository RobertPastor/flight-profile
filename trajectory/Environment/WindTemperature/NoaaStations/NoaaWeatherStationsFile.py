'''
Created on 24 juil. 2024

@author: robert
'''

import json
import os
from trajectory.Guidance.ConstraintsFile import Meters2Feet
from trajectory.Guidance.WayPointFile import WayPoint


class NoaaWeatherStationClass(object):
    FAAname = ""
    ICAOname = ""
    LatitudeDegrees = 0.0
    LongitudeDegrees = 0.0
    ElevationMeters = 0.0
    Site = ""
    State = ""
    Country = ""
    
    def __init__(self, station):
        self.FAAname = str(station['faaId'])
        self.ICAOname = str(station['icaoId'])
        self.LatitudeDegrees = float(station['lat'])
        self.LongitudeDegrees = float(station['lon'])
        self.ElevationMeters = float(station['elev'])
        self.Site = str(station['site'])
        self.State = str(station['state'])
        self.Country = str(station['country'])
        
    def getFAAname(self):
        return self.FAAname
    
    def getICAOname(self):
        return self.ICAOname
    
    def getLatitudeDegrees(self):
        return self.LatitudeDegrees
    
    def getLongitudeDegrees(self):
        return self.LongitudeDegrees
    
    def getElevationMeters(self):
        return self.ElevationMeters
    
    def getSite(self):
        return self.Site
    
    def getState(self):
        return self.State
    
    def getCountry(self):
        return self.Country


class NoaaWeatherStationsClass(object):
    fileName = ""
    stations = None
    FilesFolder = ""
    FilePath = ""

    def __init__(self, fileName):
        object.__init__(self)
        self.fileName = fileName
        
        self.FilesFolder = os.path.dirname(__file__)
        self.FilePath = os.path.join(self.FilesFolder , self.fileName)
        
    def readStations(self):
        with open( self.FilePath ) as json_data:
            self.stations = json.load(json_data)
            #for station in self.stations:
            #    if str(station['icaoId']).startswith("K"):
            #        print ( station['icaoId'] + " - " + station['site'] )
                    
    def isStationFAAExisting(self , stationFAAname):
        for station in self.stations:
            if str(station['faaId']) == stationFAAname :
                return True
        return False
    
    def isStationICAOExisting(self , stationICAOname ):
        for station in self.stations:
            if str(station['icaoId']) == stationICAOname :
                return True
        return False
    
    def getStationICAOName(self , stationFAAname ):
        for station in self.stations:
            if str(station['faaId']) == stationFAAname :
                return str(station['icaoId'])
        return None
    
    def getStationLatitudeDegrees(self, stationFAAname):
        for station in self.stations:
            if str(station['faaId']) == stationFAAname :
                return float(station['lat'])
        return None
    
    def getStationLongitudeDegrees(self, stationFAAname):
        for station in self.stations:
            if str(station['faaId']) == stationFAAname :
                return float(station['lon'])
        return None
    
    def getStationElevationMeters(self, stationFAAname):
        for station in self.stations:
            if str(station['faaId']) == stationFAAname :
                return float(station['elev'])
        return None
    
    def getStationElevationFeet(self, stationFAAname):
        for station in self.stations:
            if str(station['faaId']) == stationFAAname :
                return float(station['elev']) * Meters2Feet
        return None
    
    def getNextStation(self):
        for station in self.stations:
            if ( len ( str(station['faaId'] ) ) >= 3 ) and ( len ( str(station['icaoId'] ) ) >= 3 ):
                nooaWeatherStation = NoaaWeatherStationClass(station)
                yield nooaWeatherStation
                
    def getNearestWeatherStationICAOname(self, currentPosition):
        assert( isinstance( currentPosition , WayPoint ))
        First = True
        lowestDistanceMeters = 0.0 
        nearestWeatherStationsICAOname = ""
        for station in self.stations:
            if ( len(str(station['icaoId'])) == 4 ) and ( float(station['lat']) > -90.0 ) and str(station['icaoId']).startswith("K") :
                    
                #print ( str(station['icaoId']) )
                #print ( float(station['lat']) )
                #print ( float(station['lon']) )
                
                stationWayPoint = WayPoint(Name = str(station['icaoId']),
                                           LatitudeDegrees = float(station['lat']),
                                           LongitudeDegrees = float(station['lon']),
                                           AltitudeMeanSeaLevelMeters = 0.0)
                
                currentDistanceMeters = currentPosition.getDistanceMetersTo(stationWayPoint)
                #print ( currentDistanceMeters )
                if ( First == True ):
                    First = False
                    lowestDistanceMeters = currentDistanceMeters
                    nearestWeatherStationsICAOname = str(station['icaoId'])
                else:
                    if ( currentDistanceMeters < lowestDistanceMeters):
                        nearestWeatherStationsICAOname = str(station['icaoId'])
                        lowestDistanceMeters = currentDistanceMeters
        return nearestWeatherStationsICAOname
        
if __name__ == '__main__':
    fileName = "noaa-stations.json"
    
    noaaStations = NoaaStations( fileName )
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

