'''
Created on 4 août 2024

@author: robert

'''

class WeatherStations(object):
    
    WeatherStationDataList = []
    WeatherStationFAAlist = []
    
    def setData(self, weatherDataList):
        assert ( isinstance ( weatherDataList , list))
        self.WeatherStationDataList = weatherDataList
        
        
    def readStationFAAnames(self):
        for line in self.WeatherStationDataList:
            print ( line )
            
            
            
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