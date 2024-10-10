'''
Created on 11 août 2024

@author: robert
'''


from django.core.management.base import BaseCommand
from trajectory.models import WindTemperatureAloft, NoaaWeatherStationMeasure, NoaaWeatherStation

from trajectory.Environment.WindTemperature.WindTemperatureFetch import fetchWindTemperature
from trajectory.Environment.WindTemperature.WindTemperatureFeet import WeatherStationFeet
from trajectory.Environment.WindTemperature.WeatherStationClass import WeatherStation
from trajectory.Environment.WindTemperature.WindTemperatureHeader import WindTemperatureHeader

''' to be used in a python anywhere task '''
''' cd $HOME && source .virtualenvs/airlineservices/bin/activate && cd flight-profile && python manage.py WindTemperatureAloft '''

class Command(BaseCommand):
    help = 'Load the Wind Temperature data'

    def handle(self, *args, **options):
        
        print ( "--- about to delete Wind Temperature aloft --- ")
        WindTemperatureAloft.objects.all().delete()
        print ( "--- delete done ---")
        
        USregion = "All"
        ForecastHour = "12-Hour"
        Level = "low"
        
        weatherDataStrList = fetchWindTemperature(USregion , ForecastHour, Level)
        lineNumber = 1
        for weatherDataLine in weatherDataStrList:
            #print ( "line number = {0} - weatherDataLine = {1}".format( str(lineNumber) , weatherDataLine ) )
            lineNumber = lineNumber + 1
            if ( len(str(weatherDataLine).strip()) > 0 ):
                windTemperatureAloft = WindTemperatureAloft ( TextLine = str(weatherDataLine).strip() )
                windTemperatureAloft.save()
                
        if len(weatherDataStrList)>0:
            
            ''' ------------ analyze header ------------- '''
            windTemperatureHead = WindTemperatureHeader()
            windTemperatureHead.analyseHeader( weatherDataStrList )
            
            ''' ----------------------------------------- '''
                    
            print ( "--- about to delete Noaa Weather Station Measure --- ")
            NoaaWeatherStationMeasure.objects.all().delete()
            print ( "--- delete done ---")
            
            weatherStationFeet = WeatherStationFeet()
            feetLevels = weatherStationFeet.readTextLines(weatherDataStrList)
            numberOfLevels = len (feetLevels)
            
            feetLineFound = False
            for weatherDataLine in weatherDataStrList:
                #print ( "line number = {0} - weatherDataLine = {1}".format( str(lineNumber) , weatherDataLine ) )
                if feetLineFound:
                    pass
                    weatherStation = WeatherStation() 
                    weatherStation.ExploitStationData(weatherDataLine, numberOfLevels)
                    
                    FAAstationName = weatherStation.getStationName()
                    print ("------------ " +str(FAAstationName) + " ------------")
                    #print ( "FAA Station Name  = {0}".format(FAAstationName))
                    noaaWeatherStation = NoaaWeatherStation.objects.filter(FAAid=FAAstationName).first()
                    if ( noaaWeatherStation ):
                        print ( "Correct -> nooaWeatherStation = {0} found".format(FAAstationName) )
                        for levelIndex in range(numberOfLevels):
                            
                            noaaWeatherStationMeasure = NoaaWeatherStationMeasure(
                                NoaaWeatherStationInstance = noaaWeatherStation,
                                LevelFeet = weatherStationFeet.getLevelFeet(levelIndex),
                                WindSpeedKnots = weatherStation.getStationWindSpeedOneLevel(levelIndex),
                                WindDirectionTrueNorthDegrees = weatherStation.getStationWindDirectionOneLevel(levelIndex),
                                TemperatureDegreesCelsius = weatherStation.getStationTemperatureOneLevel(levelIndex))
                            noaaWeatherStationMeasure.save()
                        
                    else:
                        print ( "Error -> nooaWeatherStation = {0} not found".format(FAAstationName) )
    
                    
                if ( str(weatherDataLine).startswith("FT")):
                    feetLineFound = True
                
        else:
            print("Error - weather station measures list is empty")    
        