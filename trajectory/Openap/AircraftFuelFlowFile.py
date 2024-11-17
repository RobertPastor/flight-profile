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
        
    def getFuelFlowAtTakeOffKgSeconds(self, TASknots , altitudeMSLfeet ):
        fuelFlowKgSeconds = self.fuelFlow.takeoff(tas = TASknots, alt = altitudeMSLfeet, throttle=1)
        logger.info(self.className + " - fuel flow takeOff {0:.2f} kilograms per seconds".format( fuelFlowKgSeconds ))
        return fuelFlowKgSeconds
        