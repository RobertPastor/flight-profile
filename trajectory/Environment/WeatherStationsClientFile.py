'''
Created on 5 oct. 2024

@author: robert
'''

from trajectory.Environment.WindTemperature.NoaaStations.NoaaWeatherStationsFile import NoaaWeatherStationsClass
from trajectory.Guidance.WayPointFile import WayPoint
from trajectory.models import NoaaWeatherStation

from trajectory.Environment.Constants import Meter2Feet
import numpy as np

DistanceFlownBeforeSearchingNextWeatherStationMeters = 50000.0
LevelThresholdFeet = 300.0

class WeatherStationsClient(object):
    
    ''' 5th October 2024 - get temperature aloft from weather station '''
    nooaWeatherStations = None
    distanceFlowMeters = 0.0
    latestLevelFeet = 0.0
    latestInterpolatedTemperature = 0.0
    FirstNoaaWeatherStation = True
    FirstTemperatureInterpolation = True
    nearestNoaaWeatherStation = ""
    
    def __init__(self):
        
        self.className = self.__class__.__name__
        
        print ("{0} -- init --".format(self.className))
        
        fileName = "noaa-stations.json"
        self.nooaWeatherStations = NoaaWeatherStationsClass(fileName)
        self.nooaWeatherStations.readStations()
        
        self.distanceFlowMeters = 0.0
        self.latestLevelFeetTemperature = 0.0
        self.latestLevelFeetWindDirection = 0.0
        self.latestLevelFeetWindSpeed = 0.0
        
        self.FirstNoaaWeatherStation = True
        
        self.FirstTemperatureInterpolation = True
        self.latestInterpolatedTemperature = 0.0
        
        self.FirstTrueNorthWindDirectionInterpolation = True
        self.latestInterpolatedWindDirection = 0.0
        
        self.FirstWindSpeedInterpolation = True
        self.latestInterpolatedWindSpeedKnots = 0.0
        
        self.nearestNoaaWeatherStationFAA = "None"
        
    def computeNearestNoaaWeatherStationFAAname(self, currentPosition, totalDistanceFlownMeters):
        ''' 28th September 2024 - search for next weather station if distance flown is more than 50 Kilometers '''
        #assert ( isinstance ( currentPosition , WayPoint ) )
        if (not currentPosition is None) and ( isinstance ( currentPosition , WayPoint ) ) :
            if self.FirstNoaaWeatherStation == True:
                self.FirstNoaaWeatherStation = False
                self.nearestNoaaWeatherStationFAA = self.nooaWeatherStations.getNearestWeatherStationFAAname(currentPosition)
                self.distanceFlowMeters = totalDistanceFlownMeters
            else:
                ''' 15th September 2024 - every 50 Kilo meters - compute nearest weather station '''
                if totalDistanceFlownMeters > self.distanceFlowMeters + DistanceFlownBeforeSearchingNextWeatherStationMeters:
                    self.nearestNoaaWeatherStationFAA = self.nooaWeatherStations.getNearestWeatherStationFAAname(currentPosition)
                    self.distanceFlowMeters = totalDistanceFlownMeters

        return self.nearestNoaaWeatherStationFAA
    
    def computeWindSpeedKnotsAtStationLevel(self, weatherStationFAAname , altitudeMeanSeaLevelMeters):
        
        altitudeMeanSeaLevelFeet = altitudeMeanSeaLevelMeters * Meter2Feet
        if self.FirstWindSpeedInterpolation == True:
            
            self.latestLevelFeetWindSpeed = altitudeMeanSeaLevelFeet
            noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=weatherStationFAAname).first()
            if noaaWeatherStation:
                self.FirstWindSpeedInterpolation = False
                levelsFeetList = noaaWeatherStation.getWeatherStationForecastsLevels()
                # create the y list for the interpolation
                WindSpeedForecastsList = noaaWeatherStation.getWeatherStationForecastsWindSpeed()
                
                try:
                    self.latestInterpolatedWindSpeedKnots = np.interp( altitudeMeanSeaLevelFeet , levelsFeetList , WindSpeedForecastsList )
                except:
                    pass

            
        else:
            ''' if more than 300 feet level changes then interpolate again'''
            if abs( altitudeMeanSeaLevelFeet - self.latestLevelFeetWindSpeed) > LevelThresholdFeet:

                self.latestLevelFeetWindSpeed = altitudeMeanSeaLevelFeet
                noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=weatherStationFAAname).first()
                if noaaWeatherStation:
                    levelsFeetList = noaaWeatherStation.getWeatherStationForecastsLevels() 
                    WindSpeedForecastsList = noaaWeatherStation.getWeatherStationForecastsWindSpeed()
                    try:
                        self.latestInterpolatedWindSpeedKnots = np.interp( altitudeMeanSeaLevelFeet , levelsFeetList , WindSpeedForecastsList )
                    except:
                        pass

        return self.latestInterpolatedWindSpeedKnots
    
    def computeTrueNorthWindDirectionAtStationLevel(self, weatherStationFAAname , altitudeMeanSeaLevelMeters):
        
        altitudeMeanSeaLevelFeet = altitudeMeanSeaLevelMeters * Meter2Feet
        if self.FirstTrueNorthWindDirectionInterpolation == True:
            
            self.latestLevelFeetWindDirection = altitudeMeanSeaLevelFeet
            noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=weatherStationFAAname).first()
            if noaaWeatherStation:
                
                self.FirstTrueNorthWindDirectionInterpolation = False
                
                levelsFeetList = noaaWeatherStation.getWeatherStationForecastsLevels()
                WindDirectionForecastsList = noaaWeatherStation.getWeatherStationForecastsWindDirection()
                try:
                    self.latestInterpolatedWindDirection = np.interp( altitudeMeanSeaLevelFeet , levelsFeetList , WindDirectionForecastsList )
                except:
                    pass
    
        else:
            ''' if more than 300 feet level changes then interpolate again'''
            if abs( altitudeMeanSeaLevelFeet - self.latestLevelFeetWindDirection) > LevelThresholdFeet:
                
                self.latestLevelFeetWindDirection = altitudeMeanSeaLevelFeet
                    
                noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=weatherStationFAAname).first()
                if noaaWeatherStation:
                        
                    levelsFeetList = noaaWeatherStation.getWeatherStationForecastsLevels()
                    WindDirectionForecastsList = noaaWeatherStation.getWeatherStationForecastsWindDirection()
                    try:
                        #print ( "interpolate > {0}  ".format( np.interp(altitudeMeanSeaLevelFeet , levelsFeetList , temperaturesForecastsList) ) )
                        self.latestInterpolatedWindDirection = np.interp(altitudeMeanSeaLevelFeet , levelsFeetList , WindDirectionForecastsList)
                        #print ( "interpolated temperature -> {0} - for level -> {1}".format(temperatureDegreesCelsius,altitudeMeanSeaLevelFeet ))
                    except:
                        pass
        
        return self.latestInterpolatedWindDirection
        
    def computeTemperatureDegreesCelsiusAtStationLevel(self , weatherStationFAAname , altitudeMeanSeaLevelMeters):
        ''' 28th September 2024 - search for next interpolated temperature if level changes more than 300 feet '''
        #print ( weatherStationFAAname )
        altitudeMeanSeaLevelFeet = altitudeMeanSeaLevelMeters * Meter2Feet
        
        if self.FirstTemperatureInterpolation == True:
            #print( str ( self.FirstTemperatureInterpolation ) )
            
            self.latestLevelFeetTemperature = altitudeMeanSeaLevelFeet

            noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=weatherStationFAAname).first()
            if noaaWeatherStation:
                
                self.FirstTemperatureInterpolation = False
                
                levelsFeetList = noaaWeatherStation.getWeatherStationForecastsLevels()
                temperaturesForecastsList = noaaWeatherStation.getWeatherStationForecastsTemperatures()
                
                try:
                    #print ( "interpolate > {0}  ".format( np.interp(altitudeMeanSeaLevelFeet , levelsFeetList , temperaturesForecastsList) ) )
                    self.latestInterpolatedTemperature = np.interp(altitudeMeanSeaLevelFeet , levelsFeetList , temperaturesForecastsList)
                    #print ( "interpolated temperature -> {0} - for level -> {1}".format(temperatureDegreesCelsius,altitudeMeanSeaLevelFeet ))
                except:
                    pass
                    #print (" feet levels list size = {0} - temperature values list size {1}".format ( len ( levelsFeetList ) , len ( temperaturesForecastsList ) ) )
        else:
            ''' if more than 300 feet level changes then interpolate again'''
            if abs( altitudeMeanSeaLevelFeet - self.latestLevelFeetTemperature) > LevelThresholdFeet:
                
                self.latestLevelFeetTemperature = altitudeMeanSeaLevelFeet
                
                noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=weatherStationFAAname).first()
                if noaaWeatherStation:
                    
                    levelsFeetList = noaaWeatherStation.getWeatherStationForecastsLevels()
                    temperaturesForecastsList = noaaWeatherStation.getWeatherStationForecastsTemperatures()
                    
                    try:
                        #print ( "interpolate > {0}  ".format( np.interp(altitudeMeanSeaLevelFeet , levelsFeetList , temperaturesForecastsList) ) )
                        self.latestInterpolatedTemperature = np.interp(altitudeMeanSeaLevelFeet , levelsFeetList , temperaturesForecastsList)
                        #print ( "interpolated temperature -> {0} - for level -> {1}".format(temperatureDegreesCelsius,altitudeMeanSeaLevelFeet ))

                    except:
                        pass
                    
        return self.latestInterpolatedTemperature
    
    
    