'''
Created on 15 nov. 2024

@author: robert

'''

from trajectory.Openap.AircraftEngineFile import OpenapAircraftEngine

import sys
from trajectory.Environment.Constants import Knots2MetersSeconds,\
    MeterSecond2Knots
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, FuelFlow, Emission, WRAP
import json
from trajectory.Openap.AircraftEngineFile import OpenapAircraftEngine

import logging
# create logger
logger = logging.getLogger()


class OpenapAircraftSpeeds(OpenapAircraftEngine):
    pass

    maximumSpeedVmoKnots = 0.0
    initialTASknots = 0.0
    currentTASknots = 0.0
    maximumSpeedMmoMach = 0.0

    def __init__(self , aircraftICAOcode):
        logger.setLevel(logging.INFO)
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode)

        self.aircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True )
        
        self.maximumSpeedVmoKnots = self.aircraft['vmo']
        logger.info( self.className + " - max operational speed = {0} knots".format ( self.maximumSpeedVmoKnots ))
        
        self.maximumSpeedMmoMach = self.aircraft['mmo']
        logger.info( self.className + " - max operational speed = {0} mach".format ( self.maximumSpeedMmoMach ))

        self.initialTASknots = 0.0
        self.currentTASknots = self.initialTASknots
        
        wrap = WRAP(str(aircraftICAOcode).upper(), use_synonym=True)
        self.takeOffCASspeedsKnotsDict = wrap.takeoff_speed()
        logger.info( self.className + " - Take Off CAS speeds = (knots)" + json.dumps ( self.takeOffCASspeedsKnotsDict ) )
        
        self.takeOffMeanAccelerationMetersSecondsSquareDict = wrap.takeoff_acceleration()
        logger.info( self.className + " - Take Off mean acceleration = {0} meters per seconds square".format( json.dumps ( self.takeOffMeanAccelerationMetersSecondsSquareDict ) ) )

        
    def getDefaultTakeOffCASknots(self):
        ''' @TODO correct for difference to reference mass '''
        return self.takeOffCASspeedsKnotsDict['default']
    
    def getDefaultTakeOffAccelerationMetersSecondsSquare(self):
        ''' @TODO correct for difference to reference mass '''
        return self.takeOffMeanAccelerationMetersSecondsSquareDict['default']
    
    def getMinimumTakeOffAccelerationMetersSecondsSquare(self):
        return self.takeOffMeanAccelerationMetersSecondsSquareDict['minimum']
        
    def getCurrentTrueAirSpeedMetersSecond(self):
        return self.currentTASknots * Knots2MetersSeconds
        
    def getCurrentTASspeedKnots(self):
        logger.info ( self.className + " --- current TAS = {0:.2f} knots".format( self.currentTASknots ))
        return self.currentTASknots
    
    def getCurrentTASmetersSeconds(self):
        return self.currentTASknots * Knots2MetersSeconds
    
    def setCurrentTASmetersSeconds(self, TASmetersSeconds ):
        if TASmetersSeconds < 0.0:
            logger.info ( self.className + " - Error - TAS is negative " )
            raise ValueError( self.className + " - Error - TAS is negative ")
        if (TASmetersSeconds * MeterSecond2Knots) > self.maximumSpeedVmoKnots:
            self.currentTASknots = self.maximumSpeedVmoKnots
        else:
            self.currentTASknots = TASmetersSeconds * MeterSecond2Knots
        
        
        