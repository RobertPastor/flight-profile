'''
Created on 30 juil. 2024

@author: robert
'''

class WindTemperature(object):
    pass
    stationShortNameList = []

    ''' name of the station as in FAA list '''
    def getStationShortFAAName(self):
        pass
    
    def getStationICAOName (self):
        pass
    
    def getStationWindSpeedKnots(self, stationShortName , levelFeet):
        pass
    
    def getStationTemperatureDegreesCelsius(self, stationShortName , levelFeet ):
        pass
    
    def setStationList(self, stationShortNameList ):
        pass
        self.stationShortNameList = stationShortNameList