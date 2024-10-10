'''
Created on 24 juil. 2024

@author: robert
'''

import json
import os
from trajectory.Guidance.ConstraintsFile import Meters2Feet
from trajectory.Guidance.WayPointFile import WayPoint
from trajectory.models import NoaaWeatherStationMeasure
from trajectory.models import NoaaWeatherStation


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
    finalStations = []
    FilesFolder = ""
    FilePath = ""

    def __init__(self, fileName):
        object.__init__(self)
        self.fileName = fileName
        
        self.className = self.__class__.__name__
        
        self.FilesFolder = os.path.dirname(__file__)
        self.FilePath = os.path.join(self.FilesFolder , self.fileName)
        
    def readStations(self):
        with open( self.FilePath ) as json_data:
            self.stations = json.load(json_data)
            #print ( type ( self.stations  ))
            #print ( len(self.stations) )
            for station in self.stations:
                
                if len(str(station['faaId']))>=3:
                    FAAstationName = str(station['faaId'])
                    #print ( "---- {0} ----".format(FAAstationName))
                    noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=FAAstationName).first()
                    if  (len(str(station['faaId']))>=3) and noaaWeatherStation :
                        weatherStationMeasure = NoaaWeatherStationMeasure.objects.filter(NoaaWeatherStationInstance=noaaWeatherStation).first()
                        #print ( station['icaoId'] + " - " + station['site'] )
                        if ( weatherStationMeasure ):
                            pass
                            #print ( "There is a station with measure {0}".format(str(weatherStationMeasure) ) )
                            self.finalStations.append(station)
        
        #print("------- after cleaning ------------")
        print ( "{0} - final number of weather stations = {1}".format( self.className , len(self.finalStations) ) )
        #for station in self.finalStations:
        #    FAAstationName = str(station['faaId'])
        #    ICAOstationName = str(station['icaoId'])
        #    print ( "{0} ---- {1} ---- {2} ".format(self.className , FAAstationName,ICAOstationName))
            
        #print ( len(self.finalStations) )
                    
    def isStationFAAExisting(self , stationFAAname):
        for station in self.finalStations:
            if str(station['faaId']) == stationFAAname :
                return True
        return False
    
    def isStationICAOExisting(self , stationICAOname ):
        for station in self.finalStations:
            if str(station['icaoId']) == stationICAOname :
                return True
        return False
    
    def getStationICAOName(self , stationFAAname ):
        for station in self.finalStations:
            if str(station['faaId']) == stationFAAname :
                return str(station['icaoId'])
        return None
    
    def getStationLatitudeDegrees(self, stationFAAname):
        for station in self.finalStations:
            if str(station['faaId']) == stationFAAname :
                return float(station['lat'])
        return None
    
    def getStationLongitudeDegrees(self, stationFAAname):
        for station in self.finalStations:
            if str(station['faaId']) == stationFAAname :
                return float(station['lon'])
        return None
    
    def getStationElevationMeters(self, stationFAAname):
        for station in self.finalStations:
            if str(station['faaId']) == stationFAAname :
                return float(station['elev'])
        return None
    
    def getStationElevationFeet(self, stationFAAname):
        for station in self.finalStations:
            if str(station['faaId']) == stationFAAname :
                return float(station['elev']) * Meters2Feet
        return None
    
    def getNextStation(self):
        for station in self.finalStations:
            if ( len ( str(station['faaId'] ) ) >= 3 ) and ( len ( str(station['icaoId'] ) ) >= 3 ):
                nooaWeatherStation = NoaaWeatherStationClass(station)
                yield nooaWeatherStation
                
    ''' return only weather station having a forecast weather measure '''
    def getNearestWeatherStationICAOname(self, currentPosition):
        assert( isinstance( currentPosition , WayPoint ))
        First = True
        lowestDistanceMeters = 0.0 
        nearestWeatherStationsICAOname = ""
        for station in self.finalStations:
            if ( len(str(station['icaoId'])) == 4 ) and ( float(station['lat']) > -90.0 )  :
                    
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
    
    def getNearestWeatherStationFAAname(self, currentPosition):
        assert( isinstance( currentPosition , WayPoint ))
        First = True
        lowestDistanceMeters = 0.0 
        nearestWeatherStationsFAAname = ""
        for station in self.finalStations:
            if ( len(str(station['icaoId'])) == 4 ) and ( float(station['lat']) > -90.0 )  :
                    
                #print ( str(station['icaoId']) )
                #print ( float(station['lat']) )
                #print ( float(station['lon']) )
                
                stationWayPoint = WayPoint(Name = str(station['faaId']),
                                           LatitudeDegrees = float(station['lat']),
                                           LongitudeDegrees = float(station['lon']),
                                           AltitudeMeanSeaLevelMeters = 0.0)
                
                currentDistanceMeters = currentPosition.getDistanceMetersTo(stationWayPoint)
                #print ( currentDistanceMeters )
                if ( First == True ):
                    First = False
                    lowestDistanceMeters = currentDistanceMeters
                    nearestWeatherStationsFAAname = str(station['faaId'])
                else:
                    if ( currentDistanceMeters < lowestDistanceMeters):
                        nearestWeatherStationsFAAname = str(station['faaId'])
                        lowestDistanceMeters = currentDistanceMeters
        return nearestWeatherStationsFAAname
        
if __name__ == '__main__':
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

