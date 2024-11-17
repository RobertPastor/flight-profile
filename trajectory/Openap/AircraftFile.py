'''
Created on 12 nov. 2024

@author: robert
'''

import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, FuelFlow, Emission, WRAP
import json

from trajectory.Openap.AircraftConfigurationFile import OpenapAircraftConfiguration


from trajectory.Environment.Earth import Earth
from trajectory.Environment.Constants import Meter2NauticalMiles

import logging
# create logger
logger = logging.getLogger()


class OpenapAircraft(OpenapAircraftConfiguration):
    
    aircraftICAOcode = ""
    openapAircraft = None

    def __init__( self, aircraftICAOcode , initialMassKilograms , earth ):
        
        logger.setLevel(logging.INFO)
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode , earth )

        self.aircraftICAOcode = aircraftICAOcode
        self.openapAircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True) 
        
        self.setInitialMassKilograms(initialMassKilograms)
        
        logger.info ( self.className  + " --- " + self.getAircraftName() )
        
        
    def getAircraftName(self):
        return self.openapAircraft['aircraft']
    
    
    def __str__(self):
        return json.dumps( self.openapAircraft )
    
    
    
if __name__ == '__main__':
    
    earth = Earth()
    
    logging.basicConfig(level=logging.INFO)
    logger.setLevel(logging.INFO)
    print("-"*80)
    
    initialMassKilograms = 68715.00
    ac = OpenapAircraft("A320" , initialMassKilograms , earth)
    
    logger.info( ac )
        
    elapsedTimeSeconds = 0.0
    deltaTimeSeconds = 1.0
    totalDistanceFlownMeters = 0.0
    while ( elapsedTimeSeconds < 60.0 ):
        totalDistanceFlownMeters = ac.fly(elapsedTimeSeconds = elapsedTimeSeconds , 
               deltaTimeSeconds = deltaTimeSeconds ,
               totalDistanceFlownMeters = totalDistanceFlownMeters)
        
        elapsedTimeSeconds = elapsedTimeSeconds + deltaTimeSeconds 
        
        logger.info( " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))


