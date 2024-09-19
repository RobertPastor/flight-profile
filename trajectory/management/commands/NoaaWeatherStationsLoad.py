'''
Created on 18 sept. 2024

@author: robert

'''

from django.core.management.base import BaseCommand
from trajectory.models import NoaaWeatherStation
from trajectory.Environment.WindTemperature.NoaaStations.NoaaWeatherStationsFile import NoaaWeatherStationsClass

class Command(BaseCommand):
    help = 'Load the Wind Temperature data'

    def handle(self, *args, **options):
        
        print ( " --- about to delete NOAA Weather Stations --- ")
        NoaaWeatherStation.objects.all().delete()
        print ( " --- NOAA Weather Stations - delete done --- ")
        
        fileName = "noaa-stations.json"
    
        noaaStations = NoaaWeatherStationsClass( fileName )
        noaaStations.readStations()
        
        for station in noaaStations.getNextStation():
            print ( station.getFAAname() )
            
            noaaWeatherStation = NoaaWeatherStation(FAAid = station.getFAAname() ,
                                                    ICAOid = station.getICAOname() ,
                                                    LatitudeDegrees = station.getLatitudeDegrees(),
                                                    LongitudeDegrees = station.getLongitudeDegrees() ,
                                                    ElevationMeters = station.getElevationMeters() ,
                                                    Site = station.getSite() ,
                                                    State = station.getState(),
                                                    Country = station.getCountry()
                                                    )
            noaaWeatherStation.save()
    