'''
Created on 23 juil. 2024

@author: robert

https://aviationweather.gov/data/windtemp/?region=bos&fcst=12&level=high

The forecasts are made twice a day based on the
radio-sonde upper air observations taken at 0000Z and 1200Z

Altitudes through 12,000 feet are classified as true altitudes,
while altitudes 18,000 feet and above are classified as
altitudes and are termed flight levels

'''

from trajectory.Environment.WindTemperature.WindTemperatureFetch import fetchWindTemperature
from trajectory.Environment.WindTemperature.WindTemperatureFetch import USregions

if __name__ == '__main__':

    USregion = "All"
    ForecastHour = "12-Hour"
    Level = "low"
    
    weatherDataList = fetchWindTemperature(USregion , ForecastHour, Level)
    lineNumber = 1
    for weatherDataLine in weatherDataList:
        print ( "line number = {0} - weatherDataLine = {1}".format( str(lineNumber) , weatherDataLine ) )
        lineNumber = lineNumber + 1
        
    