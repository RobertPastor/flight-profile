'''
Created on 14 janv. 2023

@author: robert
'''
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse

from trajectory.models import   BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance

def getAircraft(request, airlineName):
    logger.debug ("get Airports")
    if (request.method == 'GET'):
        
        acMaxTakeOffWeightKg = 0.0
        acMinTakeOffWeightKg = 0.0
        acMaxOpAltitudeFeet = 0.0
        
        aircraftICAOcode = request.GET['aircraft']
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
            if acPerformance:
                acMaxTakeOffWeightKg = acPerformance.getMaximumMassKilograms()
                acMinTakeOffWeightKg = acPerformance.getMinimumMassKilograms()
                acMaxOpAltitudeFeet = acPerformance.getMaxOpAltitudeFeet()
                
                response_data = {
                                    'aircraftICAOcode': aircraftICAOcode,
                                    'acMaxTakeOffWeightKg' : acMaxTakeOffWeightKg ,
                                    'acMinTakeOffWeightKg' : acMinTakeOffWeightKg ,
                                    'acMaxOpAltitudeFeet' : acMaxOpAltitudeFeet
                                    }
                return JsonResponse(response_data)
            
        else:
            response_data = { "errors" : "Aircraft not found = {0}".format(request.GET['aircraft'])}
            return JsonResponse(response_data)
        
    else:
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)