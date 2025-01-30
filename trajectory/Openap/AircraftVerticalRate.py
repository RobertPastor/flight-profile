'''
Created on 25 déc. 2024

@author: robert
'''

import json
import logging 
from trajectory.Environment.Constants import Meter2Feet
logger = logging.getLogger(__name__)

import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, FuelFlow, Emission, WRAP

from trajectory.Openap.AircraftFlightPhasesFile import OpenapAircraftFlightPhases


class OpenapAircraftVerticalRate(OpenapAircraftFlightPhases):
    pass

    def __init__(self, aircraftICAOcode):
        
        self.className = self.__class__.__name__
        self.aircraftICAOcode = aircraftICAOcode
        
        super().__init__(aircraftICAOcode)
        self.aircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True )
        
        self.wrap = WRAP(str(aircraftICAOcode).upper(), use_synonym=True)
        
    def getInitialClimbVerticalRateMeterSeconds(self):
        self.initialClimbVerticalRateDictMeterSeconds = self.wrap.initclimb_vs()
        logger.info( self.className + " - initial climb vertical rate = {0} m/s".format ( json.dumps( self.initialClimbVerticalRateDictMeterSeconds ) ) )
        return self.initialClimbVerticalRateDictMeterSeconds['default']
    
    def getClimbVerticalRateMeterSeconds(self , altitudeMSLfeet ):
        #print ( json.dumps ( self.wrap.climb_vs_pre_concas() ) )
        logger.info( self.className + " cross over altitude constant CAS = {0:.2f} kilometers - {1:.2f} feet ".format( self.wrap.climb_cross_alt_concas()['default'] , self.wrap.climb_cross_alt_concas()['default'] * 1000.0 * Meter2Feet ) )
        logger.info( self.className + " cross over altitude constant Mach = {0:.2f} kilometers - {1:.2f} feet ".format( self.wrap.climb_cross_alt_conmach()['default'] , self.wrap.climb_cross_alt_conmach()['default'] * 1000.0 * Meter2Feet) )
        ''' cross over altitude expressed in kilometers '''
        if ( altitudeMSLfeet < self.wrap.climb_cross_alt_concas()['default'] * 1000.0 * Meter2Feet ):
            self.climbVerticalRateMeterSeconds = self.wrap.climb_vs_pre_concas()['minimum']
            
        elif ( ( altitudeMSLfeet >= ( self.wrap.climb_cross_alt_concas()['default'] * 1000.0 * Meter2Feet ) ) and \
            ( altitudeMSLfeet < ( self.wrap.climb_cross_alt_conmach()['default'] * 1000.0 * Meter2Feet ) ) ) :
            self.climbVerticalRateMeterSeconds = self.wrap.climb_vs_concas()['minimum']
            
        else:
            self.climbVerticalRateMeterSeconds = self.wrap.climb_vs_conmach()['minimum']
            
        logger.info( self.className + " - climb vertical rate = {0} m/s".format (  self.climbVerticalRateMeterSeconds ) )
        return self.climbVerticalRateMeterSeconds

    def getDescentVerticalRateMeterSeconds(self , altitudeMSLfeet ):
        #print ( json.dumps ( self.wrap.descent_cross_alt_conmach() ) )
        #print ( json.dumps ( self.wrap.descent_cross_alt_concas() ) )
        
        if ( altitudeMSLfeet > self.wrap.descent_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet ):
            self.descentVerticalRateMeterSeconds = self.wrap.descent_vs_conmach()['default']
            
        elif ( altitudeMSLfeet <= self.wrap.descent_cross_alt_conmach() ['default'] * 1000.0 * Meter2Feet ) and \
            ( altitudeMSLfeet > self.wrap.descent_cross_alt_concas() ['default'] * 1000.0 * Meter2Feet ):
            self.descentVerticalRateMeterSeconds = self.wrap.descent_vs_concas()['default']
        else:
            self.descentVerticalRateMeterSeconds = self.wrap.descent_vs_post_concas()['default']
            
        logger.info( self.className + " - descent vertical rate = {0} m/s".format (  self.descentVerticalRateMeterSeconds ) )
        return self.descentVerticalRateMeterSeconds