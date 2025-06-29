'''
Created on 14 janv. 2023

@author: robert
'''
import logging
logger = logging.getLogger(__name__)
from django.http import JsonResponse
from openap import prop

from trajectory.models import   BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance

from trajectory.Openap.AircraftMainFile import OpenapAircraft
from trajectory.Environment.Earth import Earth
from trajectory.Environment.Atmosphere import Atmosphere

def getAircraft(request):
    
    if (request.method == 'GET'):
        
        acMaxTakeOffWeightKg = 0.0
        acMinTakeOffWeightKg = 0.0
        acReferenceTakeOffWeightKg = 0.0
        acMaxOpAltitudeFeet = 0.0
        
        aircraftICAOcode = request.GET['aircraft']
        BadaWrapMode = request.GET['BadaWrap']
        
        if ( BadaWrapMode == "BADA" ):
        
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
                                        'aircraftICAOcode'           : aircraftICAOcode,
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
            ''' Wrap mode '''
            earth = Earth()
            atmosphere = Atmosphere()

            print("Wrap mode")
            ac = None
            available_acs = prop.available_aircraft(use_synonym=True)
            for WrapAcCode in available_acs:
                if str(WrapAcCode).upper() == aircraftICAOcode:
                    ac = OpenapAircraft( aircraftICAOcode , earth , atmosphere , initialMassKilograms = None)
                    logging.info( ac.getAircraftName())
                    
                    response_data = {
                                        'aircraftICAOcode'           : str(aircraftICAOcode).upper(),
                                        'acMaxTakeOffWeightKg'       : ac.getMaxCruiseAltitudeFeet() ,
                                        'acMinTakeOffWeightKg'       : ac.getMinimumMassKilograms() ,
                                        'acReferenceTakeOffWeightKg' : ac.getReferenceMassKilograms() ,
                                        'acMaxOpAltitudeFeet'        : ac.getMaxCruiseAltitudeFeet()
                                        }
                    return JsonResponse(response_data)
                    
            if ac is None:
                response_data = { "errors" : "Aircraft not found = {0}".format(request.GET['aircraft'])}
                return JsonResponse(response_data)
            


    else:
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)