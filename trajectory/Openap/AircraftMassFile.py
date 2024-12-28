'''
Created on 12 nov. 2024

@author: robert
'''
from trajectory.Openap.AircraftFuelFlowFile import OpenapAircraftFuelFlow
import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, FuelFlow, Emission, WRAP

import logging
# create logger
logger = logging.getLogger()


class OpenapAircraftMass(OpenapAircraftFuelFlow):

    takeOfMassKilograms = 0.0 
    initialMassKilograms = 0.0
    currentMassKilograms = 0.0
    fuelCapacityKilograms = 0.0
    
    referenceMassKilograms = 0.0
    minimumMassKilograms = 0.0
    maximumMassKilograms = 0.0
    
    
    def __init__(self , aircraftICAOcode ):
        
        logger.setLevel(logging.INFO)
        self.className = self.__class__.__name__
        
        super().__init__(aircraftICAOcode)
        
        self.openapAircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True) 
        
        self.maximumTakeOffMassKilograms   = self.openapAircraft['mtow']
        self.maxLandingMassKilograms       = self.openapAircraft['mlw']
        self.operatingEmptyWeightKilograms = self.openapAircraft['oew']
        self.referenceMassKilograms        = self.maximumTakeOffMassKilograms * 0.85
        
        logger.info ( self.className + " max TakeOff mass = {0} kilograms ".format(self.maximumTakeOffMassKilograms))
        logger.info ( self.className + " max Landing mass = {0} kilograms".format(self.maxLandingMassKilograms))
        
    def getReferenceMassKilograms (self):
        return self.referenceMassKilograms
        
    def setInitialMassKilograms(self, initialMassKilograms):
        logger.info ( self.className + " --- set initial mass = {0} kilograms".format(initialMassKilograms))
        self.takeOfMassKilograms  = initialMassKilograms
        self.initialMassKilograms = initialMassKilograms
        self.currentMassKilograms = initialMassKilograms
        
        
    def getCurrentMassKilograms(self):
        logger.info ( self.className + " --- current mass = {0:.2f} kilograms".format(self.currentMassKilograms))
        return self.currentMassKilograms
    
    def setAircraftMassKilograms(self, aircraftMassKilograms ):
        ''' @TODO add check that current mass not lower to minimum mass '''
        if ( aircraftMassKilograms < self.operatingEmptyWeightKilograms ):
            raise ValueError("Error - aircraft mass lower than Operating Empty weight = {0} kilograms".format( self.operatingEmptyWeightKilograms ))
        self.currentMassKilograms = aircraftMassKilograms
    
    def getTakeOffMassKilograms(self):
        return self.initialMassKilograms
        
    def getInitialMassKilograms(self):
        return self.initialMassKilograms
        
    def getMinimumMassKilograms(self):
        return self.minimumMassKilograms
    
    def getMaximumMassKilograms(self):
        return self.maximumMassKilograms
    