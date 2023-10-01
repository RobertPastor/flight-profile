'''
Created on 1 oct. 2023

@author: robert
'''

from django.core.management.base import BaseCommand
from trajectory.Environment.adds_metar import fetch
from trajectory.models import AirlineAirport

class Command(BaseCommand):
    help = 'Load the Airports table'

    def handle(self, *args, **options):
        
        airportICAOcode = "KATL"
        metar = fetch(airportICAOcode)
        
        if metar:
            airportName = AirlineAirport.objects.filter(AirportICAOcode=airportICAOcode).first().AirportName
            metar_data = {
                            "AirportICAOcode"      : airportICAOcode ,
                            "AirportName"          : airportName,
                            "DateTimeUTC"          : metar["observation_time"],
                            "MetarType"            : metar["metar_type"],
                            "TemperatureCelsius"   : metar["temp_c"],
                            "DewPointCelsius"      : metar["dewpoint_c"],
                            "WindSpeedKt"          : metar["wind_speed_kt"],
                            "WindDirectionCompass" : metar["wind_dir_compass"],
                            "WindDirectionDegrees" : metar["wind_dir_degrees"],
                            "WindGustKt"           : metar["wind_gust_kt"] if ("wind_gust_kt" in metar) else " ",
                            "SeaLevelPressureHpa"  : metar["sea_level_pressure_mb"] if ("sea_level_pressure_mb" in metar) else " ",
                            }
            print ( (metar_data))