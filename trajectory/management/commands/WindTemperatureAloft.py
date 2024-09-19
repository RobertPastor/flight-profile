'''
Created on 11 août 2024

@author: robert
'''


from django.core.management.base import BaseCommand
from trajectory.models import WindTemperatureAloft

from trajectory.Environment.WindTemperature.WindTemperatureFetch import fetchWindTemperature

class Command(BaseCommand):
    help = 'Load the Wind Temperature data'

    def handle(self, *args, **options):
        
        print ( " --- about to delete --- ")
        WindTemperatureAloft.objects.all().delete()
        print ( " delete done")
        
        USregion = "All"
        ForecastHour = "12-Hour"
        Level = "low"
        
        weatherDataList = fetchWindTemperature(USregion , ForecastHour, Level)
        lineNumber = 1
        for weatherDataLine in weatherDataList:
            print ( "line number = {0} - weatherDataLine = {1}".format( str(lineNumber) , weatherDataLine ) )
            lineNumber = lineNumber + 1
            if ( len(str(weatherDataLine).strip()) > 0 ):
                windTemperatureAloft = WindTemperatureAloft ( TextLine = str(weatherDataLine).strip() )
                windTemperatureAloft.save()
        
        