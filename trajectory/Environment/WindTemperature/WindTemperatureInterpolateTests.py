'''
Created on 23 sept. 2024

@author: rober
'''

from trajectory.Environment.WindTemperature.WeatherStationsClass import WeatherStations
from trajectory.Environment.WindTemperature.WindTemperatureFeet import WeatherStationFeet
from trajectory.Environment.WindTemperature.WeatherStationClass import WeatherStation
    
import numpy as np

def interpolate():
    pass


if __name__ == '__main__':
    
    weatherDataList = []
    line = "FT  3000    6000    9000   12000   18000   24000  30000  34000  39000"
    weatherDataList.append( line )
    line = "ABI      0910+22 0909+13 0406+09 1119-05 1116-18 151032 191340 990049"
    weatherDataList.append( line )
    line = "ABQ              9900+22 9900+13 0611-04 0806-15 040631 010942 011553"
    weatherDataList.append( line )
    line = "ABR 0714 2914+19 2626+13 2735+07 2837-07 2839-18 284334 284746 306650"
    weatherDataList.append( line )
    
    weatherStations = WeatherStations()
    weatherStations.setData(weatherDataList)
    weatherStations.readStationFAAnames()
    
    weatherStationFeet = WeatherStationFeet()
    feetLevels = weatherStationFeet.readTextLines(weatherDataList)
    numberOfLevels = len ( feetLevels )
    print ( feetLevels )
    #print ( weatherStationFeet.getLevelFeet( 0 ))
    #print ( weatherStationFeet.getLevelFeet( 1 ))
    
    xp = []
    for levelIndex in range(0, numberOfLevels):
        print (levelIndex)
        print (weatherStationFeet.getLevelFeet(levelIndex))
        xp.append( weatherStationFeet.getLevelFeet(levelIndex) )
    
    feetLineFound = False
    for weatherDataLine in weatherDataList:
        #print ( "line number = {0} - weatherDataLine = {1}".format( str(lineNumber) , weatherDataLine ) )
        if feetLineFound:
            pass
            weatherStation = WeatherStation() 
            weatherStation.ExploitStationData(weatherDataLine, numberOfLevels)
                
            FAAstationName = weatherStation.getStationName()
            print ("------------ " +str(FAAstationName) + " ------------")
            
            yp = []
                
            for levelIndex in range(numberOfLevels):
                print (weatherStation.getStationTemperatureOneLevel(levelIndex))
                yp.append( weatherStation.getStationTemperatureOneLevel(levelIndex) )
                
            print ( "interpoloate = level 4000 -> {0}".format( np.interp(4000.0 , xp , yp)))
            print ( "interpoloate = level 40000 -> {0}".format( np.interp(40000.0 , xp , yp)))
                    
        if ( str(weatherDataLine).startswith("FT")):
                feetLineFound = True
    