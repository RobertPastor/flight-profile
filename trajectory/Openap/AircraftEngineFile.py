'''
Created on 12 nov. 2024

@author: robert
'''

import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop
import json
from trajectory.Openap.AircraftThrustFile import OpenapAircraftThrust

import logging 
logger = logging.getLogger(__name__)

class OpenapAircraftEngine(OpenapAircraftThrust):
    pass

    def __init__(self, aircraftICAOcode ):
        logger.setLevel(logging.INFO)
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode)
        
        self.engineOptions = prop.aircraft_engine_options(aircraftICAOcode)
        
        self.aircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True )
        self.defaultEngine = self.aircraft['engine']['default']
        self.numberOfEngines = self.aircraft['engine']['number']
        
        logger.info("default engine = {}".format(self.defaultEngine))
        logger.info("number of engines = {}".format(self.numberOfEngines))
        logger.info("engines options = {}".format(self.engineOptions))
        

    def getNumberOfEngines(self):
        return self.numberOfEngines


    def getDefaultEngine(self):
        return self.defaultEngine
    
    
    def getEngineOptions(self):
        return self.engineOptions