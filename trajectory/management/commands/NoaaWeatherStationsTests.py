'''
Created on 5 oct. 2024

@author: robert
'''

from django.core.management.base import BaseCommand
from trajectory.Environment.WeatherStationsClientFile import WeatherStationsClient
from trajectory.Guidance.WayPointFile import WayPoint
from trajectory.Environment.Constants import Feet2Meter

class Command(BaseCommand):
    help = 'Tests the NOAA weather stations '

    def handle(self, *args, **options):
        
        weatherStationsClient = WeatherStationsClient()
        
        print("--------- another weather station -----------")

        currentPosition = WayPoint(Name = "Near KATL", LatitudeDegrees = 33.70, LongitudeDegrees = -84.500, AltitudeMeanSeaLevelMeters = 0.0)
        
        totalDistanceFlownMeters = 120.0
        weatherStationFAAname = weatherStationsClient.computeNearestNoaaWeatherStationFAAname( currentPosition, totalDistanceFlownMeters)
        
        print ("Nearest Noaa Weather station FAA name = {0}".format(weatherStationFAAname))
        
        altitudeFeet = 3000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter
        
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))

        print("--------------altitude change --------------------")
        altitudeFeet = 9000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter
        
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))
        
        print("--------------altitude change --------------------")

        altitudeFeet = 24000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))


        
        print("--------- another weather station -----------")

        currentPosition = WayPoint (Name = "Near San Francisco", LatitudeDegrees = 37.46, LongitudeDegrees = -122.24, AltitudeMeanSeaLevelMeters = 0.0)
        
        altitudeFeet = 3000.0
        ''' change distance flown to search for another weather station '''
        totalDistanceFlownMeters = 120000.0
        weatherStationFAAname = weatherStationsClient.computeNearestNoaaWeatherStationFAAname( currentPosition, totalDistanceFlownMeters)

        print ("Nearest Noaa Weather station FAA name = {0}".format(weatherStationFAAname))
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))

        ''' change the level '''
        print("--------------altitude change --------------------")

        altitudeFeet = 9000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))
        
        print("--------------altitude change --------------------")

        altitudeFeet = 24000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))


        
        print("--------- another weather station -----------")
        
        currentPosition = WayPoint (Name = "Near Paris", LatitudeDegrees = 48.86, LongitudeDegrees = 2.33, AltitudeMeanSeaLevelMeters = 0.0)
        
        ''' change distance flown to search for another weather station '''
        totalDistanceFlownMeters = 220000.0
        weatherStationFAAname = weatherStationsClient.computeNearestNoaaWeatherStationFAAname( currentPosition, totalDistanceFlownMeters)
        
        altitudeFeet = 3000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter

        print ("Nearest Noaa Weather station FAA name = {0}".format(weatherStationFAAname))
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))

        print("--------------altitude change --------------------")

        altitudeFeet = 9000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))
        
        print("--------------altitude change --------------------")

        altitudeFeet = 24000.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))
        #######################
        
        
        print("--------- another weather station -----------")
        
        currentPosition = WayPoint (Name = "Near Ontario", LatitudeDegrees = 34.0531, LongitudeDegrees = -117.577, AltitudeMeanSeaLevelMeters = 279.0)
        
        ''' change distance flown to search for another weather station '''
        totalDistanceFlownMeters = 320000.0
        weatherStationFAAname = weatherStationsClient.computeNearestNoaaWeatherStationFAAname( currentPosition, totalDistanceFlownMeters)
        
        altitudeFeet = 4746.0
        altitudeMeanSeaLevelMeters = altitudeFeet * Feet2Meter

        print ("Nearest Noaa Weather station FAA name = {0}".format(weatherStationFAAname))
        temperatureCelsiusDegrees = weatherStationsClient.computeTemperatureDegreesCelsiusAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Temperature Celsius = {2}".format(weatherStationFAAname, altitudeFeet, temperatureCelsiusDegrees))
        
        windDirectionTrueNorthDegrees = weatherStationsClient.computeTrueNorthWindDirectionAtStationLevel(weatherStationFAAname , altitudeMeanSeaLevelMeters)
        print (" at {0} -> level feet {1} -> Wind Direction Degrees = {2}".format(weatherStationFAAname , altitudeFeet , windDirectionTrueNorthDegrees ))
        
        windSpeedKnots = weatherStationsClient.computeWindSpeedKnotsAtStationLevel( weatherStationFAAname , altitudeMeanSeaLevelMeters )
        print (" at {0} -> level feet {1} -> Wind Speed Knots  = {2}".format(weatherStationFAAname , altitudeFeet , windSpeedKnots ))
        
        
