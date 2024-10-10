'''
Created on 27 juil. 2024

@author: robert

ABI      9900+17 0507+13 0414+08 9900-08 3416-19 363832 363440 352550
ABQ              3415+17 3315+10 3310-05 3318-17 323032 324142 312551
ABR 2016 2129+20 2130+12 2230+06 2235-07 2338-19 223934 213943 233649
AMA      2016    2317+15 1810+08 3208-07 3614-18 353032 354041 354051
AST 9900 9900+12 3209+07 2913+01 3023-13 2932-24 304439 304847 303953


Wind direction is always in reference to true north, and wind speed is given in knots.

The temperature is given in degrees Celsius.

No winds are forecast when a given level is within 1,500 feet of the
station elevation. Similarly, temperatures are not forecast for
any station within 2,500 feet of the station elevation.

'''

class WeatherStation(object):
    
    stationDataDict = {}
    stationName = ""
    
    def getStationName(self):
        return self.stationName
    
    def getStationsFirstLevel(self):
        return self.stationDataDict["firstLevel"] 
    
    def getStationLevels(self):
        return self.stationDataDict['levelsData']
    
    def getStationTemperatureLevels(self):
        return self.stationDataDict['temperatureData']
    
    def getStationTemperatureOneLevel(self, levelIndex):
        ''' zero based level index '''
        index = 0
        for stationTemperatureDataLevel in self.getStationTemperatureLevels():
            if ( index == levelIndex):
                return stationTemperatureDataLevel
            index = index + 1
        return 0.0
    
    def getStationWindSpeedLevels(self):
        return self.stationDataDict['windSpeedData']
    
    def getStationWindSpeedOneLevel(self, levelIndex):
        index = 0
        for stationWindSpeedDataLevel in self.getStationWindSpeedLevels():
            if ( index ==  levelIndex):
                return stationWindSpeedDataLevel
            index = index + 1
        return 0.0
    
    def getStationWindDirectionLevels(self):
        return self.stationDataDict['windDirectionData']
    
    def getStationWindDirectionOneLevel(self, levelIndex):
        index = 0
        for stationWindDirectionDataLevel in self.getStationWindDirectionLevels():
            if ( index == levelIndex):
                return stationWindDirectionDataLevel
            index = index + 1
        return 0.0
    
    def extractTemperature(self, levelDataStr):
        assert( isinstance( levelDataStr , str ))
        strResult = ""
        if ( len ( levelDataStr ) == 4 ):
            strResult = " "
        posPlus = str(levelDataStr).find("+")
        if ( posPlus>0 ):
            strResult = str(levelDataStr)[posPlus:]
        posMinus = str(levelDataStr).find("-")
        if ( posMinus>0 ):
            strResult = str(levelDataStr)[posMinus:]
        if (posPlus==-1)and(posMinus==-1):
            strResult = "-"+str(levelDataStr)[-2:]
        try:
            return float(strResult)
        except:
            return 0.0
        
   
    ''' If the wind speed is forecast to be greater than 99 knots but '''
    ''' less than 199 knots, the computer adds 50 to the direction '''
    ''' and subtracts 100 from the speed. To decode this type of data '''
    ''' group, the reverse must be accomplished. For example, when '''
    ''' the data appears as “731960,” subtract 50 from the 73 and '''
    ''' add 100 to the 19, and the wind would be 230° at 119 knots '''
    ''' with a temperature of –60 °C. '''
    def extractWindSpeed(self, levelDataStr ):
        ''' wind speed in knots '''
        assert( isinstance( levelDataStr , str ))
        try:
            windSpeedFloat = 0.0
            windSpeedStr = str(levelDataStr)[2:4]
            if str(windSpeedStr).isdigit():
                windSpeedFloat = float(windSpeedStr)
                
                windDirectionStr = str(levelDataStr)[0:2]
                ''' When the forecast wind speed is calm, or less than '''
                ''''5 knots, the data group is coded “9900" '''
                if windDirectionStr == "99" and windSpeedStr == "00":
                    windSpeedFloat = 0.0
                else:
                    if str(windDirectionStr).isdigit():
                        windDirectionFloat = float(windDirectionStr)
                        if ( windDirectionFloat > 36.0 ):
                            ''' add 100 to wind speed '''
                            windSpeedFloat = windSpeedFloat + 100.0
    
            return windSpeedFloat
        except:
            return 0.0
        
    ''' If the wind speed is forecast to be greater than 99 knots but '''
    ''' less than 199 knots, the computer adds 50 to the direction '''
    ''' and subtracts 100 from the speed. To decode this type of data '''
    ''' group, the reverse must be accomplished. For example, when '''
    ''' the data appears as “731960,” subtract 50 from the 73 and '''
    ''' add 100 to the 19, and the wind would be 230° at 119 knots '''
    ''' with a temperature of –60 °C. '''
    def extractWindDirection(self, levelDataStr):
        ''' wind direction in degrees '''
        assert( isinstance( levelDataStr , str ))
        try:
            windDirectionFloat = 0.0
            windDirectionStr = str(levelDataStr)[0:2]
            windSpeedStr = str(levelDataStr)[2:4]
            if str(windDirectionStr).isdigit():
                windDirectionFloat = float(windDirectionStr)
                ''' When the forecast wind speed is calm, or less than '''
                ''' '5 knots, the data group is coded “9900" '''
                if windDirectionStr == "99" and windSpeedStr == "00":
                    windDirectionFloat = 0.0
                else:
                    if ( windDirectionFloat > 36.0 ):
                        windDirectionFloat = ( windDirectionFloat - 50.0 )
                    windDirectionFloat = windDirectionFloat * 10.0
            
            return windDirectionFloat
        except:
            return 0.0
    
    def ExploitStationData( self, stationData , numberOfLevels ):
        pass
        assert( isinstance( stationData , str ))
        assert( isinstance( numberOfLevels , int ))
        self.stationDataDict = {}
    
        #print( stationData )
        if len ( str ( stationData ) ) > 3:
            stationName = str(stationData)[0:3]
            #print ( "Station name = {0}".format(stationName) )
            self.stationDataDict['name'] = stationName
            self.stationName = stationName
            
            '''1st level data is always composed of 4 digits '''
            firstLevelData = str(stationData)[4:8]
            #print ( firstLevelData )
            self.stationDataDict["firstLevel"] = firstLevelData
                
            levelsData = []
            temperatureData = []
            temperatureFirstValue = 0.0
            windSpeedData = []
            windDirectionData = []
            First = True
            
            stationData = stationData[4:]
            stationArr = str(stationData).split(" ")
            for elem in stationArr:
                if len( str(elem).strip()) > 0:
                    
                    levelsData.append( str(elem).strip() )
                    if len(str(elem).strip()) > 4:
                        temperatureData.append( self.extractTemperature( str(elem).strip()) )
                        if First == True:
                            First = False
                            temperatureFirstValue = self.extractTemperature( str(elem).strip())
                        
                    windSpeedData.append( self.extractWindSpeed( str(elem).strip() ) )
                    windDirectionData.append( self.extractWindDirection( str(elem).strip() ) )
                    
                    
            ''' insert empty elements '''
            for n in range ( numberOfLevels - len(levelsData) ):      
                levelsData.insert( n , 0.0 )
                windSpeedData.insert( n , 0.0)
                windDirectionData.insert( n , 0.0)
                
            ''' insert initial temperature '''
            for n in range ( numberOfLevels - len ( temperatureData )):
                temperatureData.insert( n , temperatureFirstValue)
                
            self.stationDataDict['levelsData'] = levelsData
            self.stationDataDict['temperatureData'] = temperatureData
            self.stationDataDict['windSpeedData'] = windSpeedData
            self.stationDataDict['windDirectionData'] = windDirectionData
            
        else:
            print ( "Error = cannot find station name")
        return self.stationDataDict



if __name__ == '__main__':
    stationData = "ABI      9900+17 0507+13 0414+08 9900-08 3416-19 363832 363440 352550"
    numberOfLevels = 9
    weatherStation = WeatherStation()
    weatherStation.ExploitStationData(stationData, numberOfLevels)
    
    print ( weatherStation.getStationName() )
    
    stationData = "ABQ              3415+17 3315+10 3310-05 3318-17 323032 324142 312551"
    numberOfLevels = 9
    weatherStation = WeatherStation()
    weatherStation.ExploitStationData(stationData, numberOfLevels)
    
    print ( weatherStation.getStationName() )
    print ( weatherStation.getStationTemperatureOneLevel(0))
    print ( weatherStation.getStationTemperatureLevels())
    
    stationData = "ABR 0906 1005+14 3306+11 3217+07 3227-08 3135-20 305135 295444 306751"
    
    numberOfLevels = 9
    weatherStation = WeatherStation()
    weatherStation.ExploitStationData(stationData, numberOfLevels)
    
    print ( weatherStation.getStationName() )
    print ( weatherStation.getStationLevels())
    