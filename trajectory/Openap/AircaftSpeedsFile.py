'''
Created on 15 nov. 2024

@author: robert

'''


import sys
import math
from trajectory.Environment.Constants import Knots2MetersSeconds,  MeterSecond2Knots
from trajectory.Environment.Constants import Meter2Feet
from trajectory.aerocalc.airspeed import mach_alt2cas
from trajectory.Environment.Constants import NauticalMiles2Meter
from sqlalchemy.sql._elements_constructors import false

#sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, FuelFlow, Emission, WRAP
import json
from trajectory.Openap.AircraftEngineFile import OpenapAircraftEngine

import logging
# create logger
logger = logging.getLogger()
import numpy as np

class OpenapAircraftSpeeds(OpenapAircraftEngine):

    maximumSpeedVmoKnots = 0.0
    initialTASknots = 0.0
    currentTASknots = 0.0
    maximumSpeedMmoMach = 0.0
    targetCruiseMach = 0.0

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
        
        self.wrap = WRAP(str(aircraftICAOcode).upper(), use_synonym=True)
        self.takeOffCASspeedsMeterSecondsDict = self.wrap.takeoff_speed() 
        logger.info( self.className + " - Take Off CAS speeds = (m/s)" + json.dumps ( self.takeOffCASspeedsMeterSecondsDict ) )
        
        self.takeOffMeanAccelerationMetersSecondsSquareDict = self.wrap.takeoff_acceleration()
        logger.info( self.className + " - Take Off mean acceleration = {0} meters per seconds square".format( json.dumps ( self.takeOffMeanAccelerationMetersSecondsSquareDict ) ) )

        self.initialDescentCASset = False
        self.initialDescentCASknots = 0.0
        self.initialDescentAltitudeFeet = 0.0
        
        self.initialClimbCASset = False
        self.initialClimbCASknots = 0.0
        self.initialClimbAltitudeFeet = 0.0
        
    def getMaximumSpeedMmoMach(self):
        return self.maximumSpeedMmoMach
    
    def setTargetCruiseMach(self, targetCruiseMach ):
        self.targetCruiseMach = targetCruiseMach
        
    def getDefaultTakeOffCASknots(self):
        ''' @TODO correct for difference to reference mass '''
        return self.takeOffCASspeedsMeterSecondsDict['default'] * MeterSecond2Knots
    
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
        
        
    def getFinalApproachCASknots( self ):
        return self.wrap.finalapp_vcas()['default'] 
    
    def computeLandingStallSpeedCasKnots(self):
        return self.wrap.landing_speed()['default'] 
    
    def computeClimbCASknots(self , altitudeMSLfeet , CASknots ):
        
        if self.initialClimbCASset == False:
            self.initialClimbCASset = True
            self.initialClimbCASknots = CASknots
            self.initialClimbAltitudeFeet = altitudeMSLfeet
        
        self.climbCASknots = CASknots
        ''' cross over altitude when constant CAS climb starts '''
        if ( altitudeMSLfeet < self.wrap.climb_cross_alt_concas() ['default'] * 1000.0 * Meter2Feet ):
            ''' below cross over altitude when constant CAS climb starts '''
            
            self.constantClimbCASknots = self.wrap.climb_const_vcas()['default']
            ''' xp must be in increasing order '''
            if ( self.initialClimbCASknots < self.constantClimbCASknots):
                self.climbCASknots = np.interp ( x = altitudeMSLfeet , 
                                            xp = [ self.initialClimbAltitudeFeet , self.wrap.climb_cross_alt_concas() ['default'] * 1000.0 * Meter2Feet ],
                                            fp = [ self.initialClimbCASknots , self.constantClimbCASknots ] )
            else:
                self.climbCASknots = self.initialClimbCASknots
                self.initialClimbCASknots = self.climbCASknots
                
        elif ( altitudeMSLfeet < self.wrap.climb_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet ):
            
            self.constantClimbMach = self.wrap.climb_const_mach()['default']
            
            self.constantClimbCASknots = mach_alt2cas( mach = self.constantClimbMach , 
                                                         altitude = altitudeMSLfeet , 
                                                         alt_units = 'ft',
                                                         speed_units = 'kt')
            self.climbCASknots = np.interp ( x = altitudeMSLfeet , 
                                            xp = [ self.wrap.climb_cross_alt_concas() ['default'] * 1000.0 * Meter2Feet , self.wrap.climb_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet ],
                                            fp = [ self.initialClimbCASknots , self.constantClimbCASknots ] )
           
        else:
            self.constantClimbMach = self.wrap.climb_const_mach()['default']
            
            self.climbCASknots = mach_alt2cas( mach = self.constantClimbMach , 
                                                         altitude = altitudeMSLfeet , 
                                                         alt_units = 'ft',
                                                         speed_units = 'kt')
        
        logger.info( self.className + " - climb CAS speed = {0} kt".format (  self.climbCASknots ) )
        return self.climbCASknots
        
    def computeDescentCASknots(self , altitudeMSLfeet , CASknots ):
        if self.initialDescentCASset == False:
            self.initialDescentCASset = True
            self.initialDescentCASknots = CASknots
            self.initialDescentAltitudeFeet = altitudeMSLfeet
        
        ''' distance from runway = 10 Nautical miles '''
        glideSlopeLenthFeet = 10.0 * NauticalMiles2Meter * Meter2Feet  # 10.0 Nautical miles
        ''' 3 degrees glide slope '''
        glideSlopeHeightFeet = math.tan( math.radians( 3.0 )) * glideSlopeLenthFeet
        
        self.constantCASdescentKnots = 0.0
        
        if ( altitudeMSLfeet > self.wrap.descent_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet ):
            ''' above altitude to transition from constant Mach to constant CAS '''
            constantMachDescent = self.wrap.descent_const_mach()['default']
            self.constantCASDescentKnots = mach_alt2cas( mach = constantMachDescent , 
                                                         altitude = altitudeMSLfeet , 
                                                         alt_units = 'ft',
                                                         speed_units = 'kt')
            
            if ( CASknots > self.constantCASDescentKnots ):
                ''' xp must be in increasing order '''
                self.constantCASdescentKnots = np.interp ( x = altitudeMSLfeet , 
                                                      xp = [ self.wrap.descent_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet , self.initialDescentAltitudeFeet],
                                                      fp = [ self.constantCASDescentKnots , self.initialDescentCASknots ])
            else:
                self.constantCASdescentKnots = self.initialDescentCASknots
            
            
        elif ( altitudeMSLfeet <= self.wrap.descent_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet ) and \
            ( altitudeMSLfeet > self.wrap.descent_cross_alt_concas() ['default'] * 1000.0 * Meter2Feet ):
            
            ''' below altitude to transition from constant MACH to constant CAS '''
            
            constantMachDescent = self.wrap.descent_const_mach()['default']
            self.constantMachdescentKnots = mach_alt2cas( mach = constantMachDescent , 
                                                         altitude = altitudeMSLfeet , 
                                                         alt_units = 'ft',
                                                         speed_units = 'kt')
            
            self.constantCASdescentKnots = self.wrap.descent_const_vcas()['default']
            ''' xp must be in increasing order '''            
            self.constantCASdescentKnots = np.interp ( x = altitudeMSLfeet , 
                                                  xp = [ self.wrap.descent_cross_alt_concas() ['default'] * 1000.0 * Meter2Feet , self.wrap.descent_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet ],
                                                  fp = [ self.constantCASdescentKnots , self.initialDescentCASknots ])
             
            
        else:
            ''' low altitude to transition from constant CAS to final approach CAS '''
            altitudeConstantCASfeet = self.wrap.descent_cross_alt_concas() ['default'] * 1000.0 * Meter2Feet
            ''' altitude of final approach '''
            altitudeFinalApproachStartFeet = altitudeConstantCASfeet - glideSlopeHeightFeet
            ''' transition speed before entering final approach configuration '''
            descentConstantCAS = self.wrap.descent_const_vcas()['default']
            finalApproachCAS = self.wrap.finalapp_vcas()['default']
            
            ''' xp must be in increasing order '''
            self.constantCASdescentKnots = np.interp ( x = altitudeMSLfeet , 
                                                       xp = [ altitudeFinalApproachStartFeet , altitudeConstantCASfeet  ] , 
                                                       fp = [ finalApproachCAS , descentConstantCAS ])
            
        logger.info( self.className + " - descent CAS speed = {0} m/s".format (  self.constantCASdescentKnots ) )
        return self.constantCASdescentKnots
    
    def computeApproachCASknots(self):
        self.approachCASknots = self.wrap.finalapp_vcas()['default']
        logging.info( self.className + ' - approach CAS = {0:.2f} knots'.format( self.approachCASknots ))
        return self.approachCASknots
        
        
    def isCruiseSpeedReached(self):
        return False