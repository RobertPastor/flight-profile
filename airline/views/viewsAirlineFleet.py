'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse

# Create your views here.
from airline.models import Airline, AirlineAircraft
from trajectory.models import BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance

import logging
logger = logging.getLogger(__name__)
from openap import prop

from trajectory.Environment.Earth import Earth
from trajectory.Environment.Atmosphere import Atmosphere

from trajectory.Openap.AircraftMainFile import OpenapAircraft

def getAirlineFleetFromDB(airline):
    airlineFleetList = []
    
    available_acs = prop.available_aircraft(use_synonym=True)

    for airlineAircraft in AirlineAircraft.objects.filter(airline = airline):
        
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=airlineAircraft.aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftJsonPerformanceFileExists()):
            #print ( badaAircraft.getAircraftJsonPerformanceFile() )
            
            aircraftPerformance = AircraftJsonPerformance(badaAircraft.getICAOcode(), badaAircraft.getAircraftJsonPerformanceFile())
            if ( aircraftPerformance.read() ):
            
                #logger.debug ( str ( airlineAircraft ) )
                airlineFleetList.append({
                    "Airline"                           : airline.Name,
                    "AircraftICAOcode"                  : airlineAircraft.aircraftICAOcode,
                    "AircraftFullName"                  : airlineAircraft.aircraftFullName,
                    "NumberOfAircrafts"                 : airlineAircraft.numberOfAircraftsInService,
                    "MaxNumberOfPassengers"             : airlineAircraft.maximumOfPassengers,
                    "CostsFlyingHoursDollars"           : airlineAircraft.costsFlyingPerHoursDollars,
                    "CrewCostsFlyingHoursDollars"       : airlineAircraft.crewCostsPerFlyingHoursDollars,
                    "MinimumTakeOffMassKg"              : aircraftPerformance.getMinimumMassKilograms() ,
                    "ReferenceMassKg"                   : aircraftPerformance.getReferenceMassKilograms(),
                    "MaximumTakeOffMassKg"              : aircraftPerformance.getMaximumMassKilograms() ,
                    "AircraftTurnAroundTimeMinutes"     : airlineAircraft.getTurnAroundTimesMinutes()
                    })
        elif  airlineAircraft.aircraftICAOcode.lower() in available_acs:
            
            aircraftICAOcode = airlineAircraft.aircraftICAOcode.lower()
            ac = OpenapAircraft( aircraftICAOcode , Earth() , Atmosphere() , initialMassKilograms = None)
            
            airlineFleetList.append({
                    "Airline"                           : airline.Name,
                    "AircraftICAOcode"                  : airlineAircraft.aircraftICAOcode,
                    "AircraftFullName"                  : airlineAircraft.aircraftFullName,
                    "NumberOfAircrafts"                 : airlineAircraft.numberOfAircraftsInService,
                    "MaxNumberOfPassengers"             : airlineAircraft.maximumOfPassengers,
                    "CostsFlyingHoursDollars"           : airlineAircraft.costsFlyingPerHoursDollars,
                    "CrewCostsFlyingHoursDollars"       : airlineAircraft.crewCostsPerFlyingHoursDollars,
                    "MinimumTakeOffMassKg"              : ac.getMinimumMassKilograms() ,
                    "ReferenceMassKg"                   : ac.getReferenceMassKilograms(),
                    "MaximumTakeOffMassKg"              : ac.getMaximumTakeOffMassKilograms() ,
                    "AircraftTurnAroundTimeMinutes"     : airlineAircraft.getTurnAroundTimesMinutes()
                    })

            
    return airlineFleetList
    
    
def getAirlineFleet(request, airlineName):
    logger.debug ("get Airline Fleet for airline = {0}".format(airlineName))
    if (request.method == 'GET'):
        logger.debug("get request received - Airline Fleet")
        airline = Airline.objects.filter(Name=airlineName).first()
        if (airline):
            airlineFleet = getAirlineFleetFromDB(airline)
            response_data = {'airlineFleet': airlineFleet}
            return JsonResponse(response_data)
        else:
            return JsonResponse({'errors': "airline with name {0} not found".format(airlineName)})
    
    else:
        response_data = { "errors" : "Expecting a GET - received something else = {0}".format(request.method)}
        return JsonResponse(response_data)
    