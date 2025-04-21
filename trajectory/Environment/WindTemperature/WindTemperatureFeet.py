'''
Created on 26 juil. 2024

@author: robert

FT  3000    6000    9000   12000   18000   24000  30000  34000  39000
https://www.faa.gov/regulationspolicies/handbooksmanuals/aviation/phak/chapter-13-aviation-weather-services

'''

class WeatherStationFeet(object):
    
    feetLevels = []
    
    def readTextLines(self, windTemperatureList):
        assert ( isinstance ( windTemperatureList , list))
        for textLine in windTemperatureList:
            if ( str(textLine).startswith("FT") ):
                self.exploitFeetLine(textLine)
        return self.feetLevels

    def exploitFeetLine(self, feetLine):
        #print ( feetLine )
        self.feetLevels = []
        if str(feetLine).startswith( "FT" ):
            #print ( "Feet line starts with FT as expected ")
            feetLine = str(feetLine)[2:]
            #print ( feetLine )
            splitArray = str(feetLine).split(" ")
            for elem in splitArray:
                elem = str( elem.strip( ))
                if len ( elem ) > 0:
                    #print (elem.strip(" "))
                    self.feetLevels.append(elem.strip(" "))
                    
        else:
            print ( "Error = Feet line does not start with FT as expected ")     
            
    def getLevelFeet(self, levelIndex):
        index = 0
        for feetLevel in self.feetLevels:
            if ( index == levelIndex ):
                return float(feetLevel)
            index = index + 1
        return 0.0
       

if __name__ == '__main__':
    feetLine = "FT  3000    6000    9000   12000   18000   24000  30000  34000  39000"
    windTemperatureList = []
    windTemperatureList.append(feetLine)
    weatherStationFeet = WeatherStationFeet()
    
    feetLevels = weatherStationFeet.readTextLines(windTemperatureList)
    print ( feetLevels )
    print ( weatherStationFeet.getLevelFeet( 0 ))
    print ( weatherStationFeet.getLevelFeet( 1 ))
    
    print ( "------------------")
    
    feetLine = "FE 3000    6000    9000   12000   18000   24000  30000  34000  39000"
    windTemperatureList = []
    windTemperatureList.append(feetLine)
    weatherStationFeet = WeatherStationFeet()
    
    feetLevels = weatherStationFeet.readTextLines(windTemperatureList)
    print ( feetLevels )
    print ( weatherStationFeet.getLevelFeet(0 ))
    