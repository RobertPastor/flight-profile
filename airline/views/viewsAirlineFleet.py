'''
Created on 4 sept. 2022

@author: robert
'''

from django.http import  JsonResponse

# Create your views here.
from airline.models import Airline, AirlineAircraft
from trajectory.models import BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance

import logging
logger = logging.getLogger(__name__)


def getAirlineFleetFromDB(airline):
    airlineFleetList = []
    for airlineAircraft in AirlineAircraft.objects.filter(airline = airline):
        
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=airlineAircraft.aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            #print ( badaAircraft )
            
            aircraftPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
            if ( aircraftPerformance.read() ):
            
                #logger.debug ( str ( airlineAircraft ) )
                airlineFleetList.append({
                    "Airline"                     : airline.Name,
                    "AircraftICAOcode"            : airlineAircraft.aircraftICAOcode,
                    "AircraftFullName"            : airlineAircraft.aircraftFullName,
                    "NumberOfAircrafts"           : airlineAircraft.numberOfAircraftsInService,
                    "MaxNumberOfPassengers"       : airlineAircraft.maximumOfPassengers,
                    "CostsFlyingHoursDollars"     : airlineAircraft.costsFlyingPerHoursDollars,
                    "CrewCostsFlyingHoursDollars" : airlineAircraft.crewCostsPerFlyingHoursDollars,
                    "MinimumTakeOffMassKg"        : aircraftPerformance.getMinimumMassTons() * 1000.0,
                    "ReferenceMassKg"             : aircraftPerformance.getReferenceMassKilograms(),
                    "MaximumTakeOffMassKg"        : aircraftPerformance.getMaximumMassTons() * 1000.0,
                    "AircraftTurnAroundTimeMinutes"       : airlineAircraft.getTurnAroundTimesMinutes()
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
    