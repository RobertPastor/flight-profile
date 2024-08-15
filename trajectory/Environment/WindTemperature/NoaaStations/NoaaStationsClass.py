'''
Created on 24 juil. 2024

@author: robert
'''

import json
from trajectory.Guidance.ConstraintsFile import Meters2Feet

class NoaaStations(object):
    fileName = ""
    stations = None

    def __init__(self, fileName)->None:
        object.__init__(self)
        self.fileName = fileName
        
    def readStations(self):
        with open("./" + self.fileName) as json_data:
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

