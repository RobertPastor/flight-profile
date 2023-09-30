'''
Created on 25 sept. 2023

@author: robert

retrieve the METAR for each airline airport

'''

from django.http import JsonResponse
import logging
logger = logging.getLogger(__name__)

from trajectory.models import AirlineAirport
from airline.models import Airline, AirlineRoute
from trajectory.Environment.adds_metar import fetch

def getMetarForAirports(request, airline):
    airportsList = []
    for airport in AirlineAirport.objects.all():
        for airlineRoute in AirlineRoute.objects.filter(airline = airline):
            if (airport.AirportICAOcode == airlineRoute.getDepartureAirportICAOcode()) or (airport.AirportICAOcode == airlineRoute.getArrivalAirportICAOcode() ):
                if not( airport.AirportICAOcode in airportsList):
                    logger.debug (airport.AirportICAOcode)
                    airportsList.append(airport.AirportICAOcode)
                    
    
    airportsMetarList = []
    for airportICAOcode in airportsList:
        logger.debug (airportICAOcode)
        metar = fetch(airportICAOcode)
        
        if metar:
            airportName = AirlineAirport.objects.filter(AirportICAOcode=airportICAOcode).first().AirportName
            airportsMetarList.append({
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
                            })
    return airportsMetarList

def getMetar(request , airlineName):
    logger.debug ("get Metar")
    if (request.method == 'GET'):
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            logger.debug ( airline )
            airportsMetarList = getMetarForAirports(request , airline)
            response_data = {'metars': airportsMetarList}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})
    else:
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)