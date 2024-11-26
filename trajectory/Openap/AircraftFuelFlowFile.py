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
from trajectory.Openap.AircraftFlightPhasesFile import OpenapAircraftFlightPhases

class OpenapAircraftFuelFlow(OpenapAircraftFlightPhases):
    
    aircraftICAOcode = ""

    def __init__(self , aircraftICAOcode ):
        
        self.className = self.__class__.__name__
        self.aircraftICAOcode = aircraftICAOcode
        
        super().__init__(aircraftICAOcode)

        self.fuelFlow = FuelFlow(ac=aircraftICAOcode)
        
    def getFuelFlowAtTakeOffKgSeconds(self, TASknots , aircraftAltitudeMSLfeet ):
        fuelFlowKgSeconds = self.fuelFlow.takeoff(tas = TASknots, alt = aircraftAltitudeMSLfeet, throttle=1)
        logger.info(self.className + " - fuel flow takeOff {0:.2f} kilograms per second".format( fuelFlowKgSeconds ))
        return fuelFlowKgSeconds
    
    def getFuelFlowClimbKgSeconds(self , aircraftMassKilograms , TASknots , aircraftAltitudeMSLfeet , rateOfClimbFeetMinutes , acceleationMetersSecondsSquare ):
        fuelFlowKgSeconds = self.fuelFlow.enroute(mass=aircraftMassKilograms, tas=TASknots, alt=aircraftAltitudeMSLfeet, vs=rateOfClimbFeetMinutes, acc=acceleationMetersSecondsSquare, limit=True)
        logger.info(self.className + " - fuel flow climb {0:.2f} kilograms per second".format( fuelFlowKgSeconds ))
        return fuelFlowKgSeconds

    def computeFuelFlowKilograms(self , TASknots , aircraftAltitudeMSLfeet , aircraftMassKilograms=0.0, rateOfClimbFeetMinutes=0.0, acceleationMetersSecondsSquare=0.0):
        fuelFlowKilogramseconds = None
        
        if self.isDepartureGroundRun():
            fuelFlowKilogramseconds = self.getFuelFlowAtTakeOffKgSeconds( TASknots=TASknots, aircraftAltitudeMSLfeet=aircraftAltitudeMSLfeet )
            
        elif self.isTakeOff():
            fuelFlowKilogramseconds = self.getFuelFlowClimbKgSeconds( aircraftMassKilograms=aircraftMassKilograms , TASknots=TASknots , aircraftAltitudeMSLfeet=aircraftAltitudeMSLfeet , rateOfClimbFeetMinutes=rateOfClimbFeetMinutes, acceleationMetersSecondsSquare=acceleationMetersSecondsSquare)

        elif self.isInitialClimb():
            fuelFlowKilogramseconds = self.getFuelFlowClimbKgSeconds( aircraftMassKilograms=aircraftMassKilograms , TASknots=TASknots , aircraftAltitudeMSLfeet=aircraftAltitudeMSLfeet , rateOfClimbFeetMinutes=rateOfClimbFeetMinutes, acceleationMetersSecondsSquare=acceleationMetersSecondsSquare)

        elif self.isClimb():
            fuelFlowKilogramseconds = self.getFuelFlowClimbKgSeconds( aircraftMassKilograms=aircraftMassKilograms , TASknots=TASknots , aircraftAltitudeMSLfeet=aircraftAltitudeMSLfeet , rateOfClimbFeetMinutes=rateOfClimbFeetMinutes, acceleationMetersSecondsSquare=acceleationMetersSecondsSquare)

        else:
            fuelFlowKilogramseconds = None

        return fuelFlowKilogramseconds