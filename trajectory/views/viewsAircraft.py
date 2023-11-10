'''
Created on 14 janv. 2023

@author: robert
'''
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse

from trajectory.models import   BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance

def getAircraft(request):
    
    if (request.method == 'GET'):
        
        acMaxTakeOffWeightKg = 0.0
        acMinTakeOffWeightKg = 0.0
        acReferenceTakeOffWeightKg = 0.0
        acMaxOpAltitudeFeet = 0.0
        
        aircraftICAOcode = request.GET['aircraft']
        
        badaAircraft = BadaSynonymAircraft.objects.filter(AircraftICAOcode=aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            acPerformance = AircraftJsonPerformance(aircraftICAOcode, badaAircraft.getAircraftPerformanceFile())
            if acPerformance.read():
                
                acMaxTakeOffWeightKg = acPerformance.getMaximumMassKilograms()
                acMinTakeOffWeightKg = acPerformance.getMinimumMassKilograms()
                acReferenceTakeOffWeightKg = acPerformance.getReferenceMassKilograms()
                acMaxOpAltitudeFeet = acPerformance.getMaxOpAltitudeFeet()
                ''' @TODO warning : keys must be identical to those defined in utils.getAirlineAircraftsFromDB '''
                response_data = {
                                    'aircraftICAOcode': aircraftICAOcode,
                                    'acMaxTakeOffWeightKg'       : acMaxTakeOffWeightKg ,
                                    'acMinTakeOffWeightKg'       : acMinTakeOffWeightKg ,
                                    'acReferenceTakeOffWeightKg' : acReferenceTakeOffWeightKg ,
                                    'acMaxOpAltitudeFeet'        : acMaxOpAltitudeFeet
                                    }
                return JsonResponse(response_data)
            else:
                response_data = { "errors" : "Aircraft performance data not read correctly = {0}".format(request.GET['aircraft'])}
                return JsonResponse(response_data)
        else:
            response_data = { "errors" : "Aircraft not found = {0}".format(request.GET['aircraft'])}
            return JsonResponse(response_data)
    else:
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)