'''
Created on 12 nov. 2024

@author: robert

'''

import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import FuelFlow
import logging 
logger = logging.getLogger(__name__)
from trajectory.Openap.AircraftStateVectorFile import AircraftStateVector

class OpenapAircraftFuelFlow(object):
    
    aircraftICAOcode = ""

    def __init__(self , aircraftICAOcode ):
        
        self.className = self.__class__.__name__
        self.aircraftICAOcode = aircraftICAOcode
        
        self.fuelFlow = FuelFlow(ac=aircraftICAOcode)
        
    def getFuelFlowAtTakeOffKgSeconds(self, TASknots , aircraftAltitudeMSLfeet ):
        fuelFlowKgSeconds = self.fuelFlow.takeoff(tas = TASknots, alt = aircraftAltitudeMSLfeet, throttle=1)
        logger.info(self.className + " - fuel flow takeOff {0:.2f} kilograms per second".format( fuelFlowKgSeconds ))
        return fuelFlowKgSeconds
    
    def getFuelFlowClimbKgSeconds(self , aircraftMassKilograms , TASknots , aircraftAltitudeMSLfeet , rateOfClimbFeetMinutes , acceleationMetersSecondsSquare ):
        fuelFlowKgSeconds = self.fuelFlow.enroute(mass=aircraftMassKilograms, tas=TASknots, alt=aircraftAltitudeMSLfeet, vs=rateOfClimbFeetMinutes, acc=acceleationMetersSecondsSquare, limit=True)
        logger.info(self.className + " - fuel flow climb {0:.2f} kilograms per second".format( fuelFlowKgSeconds ))
        return fuelFlowKgSeconds
