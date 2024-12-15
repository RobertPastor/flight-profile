'''
Created on 15 nov. 2024

@author: robert
'''

from trajectory.Openap.AircraftMassFile import OpenapAircraftMass

import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, Thrust, Drag
import json

from trajectory.Openap.AircraftMassFile import OpenapAircraftMass

import logging 
logger = logging.getLogger(__name__)

class OpenapAircraftDrag(OpenapAircraftMass):
    
    def __init__(self , aircraftICAOcode ):
        pass
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode)
                
        self.aircraftDict = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True )
        self.drag = Drag(ac=str( aircraftICAOcode ).lower() , wave_drag=True)
        
        
    def getWingAreaSurfaceSquareMeters(self):
        return self.aircraftDict['wing']['area']
        
        
    def getCleanDragNewtons(self , massKilograms , tasKnots , altitudeMSLfeet , verticalSpeedFeetMinutes ):
        self.currentDragNewtons = self.drag.clean( mass = massKilograms, tas = tasKnots, alt = altitudeMSLfeet, vs = verticalSpeedFeetMinutes )
        logger.info( self.className + " - clean drag = {0:.2f} Newtons".format ( self.currentDragNewtons ))
        return self.currentDragNewtons
    
    
    def getNonCleanDragNewtons(self , massKilograms , tasKnots , altitudeMSLfeet , flap_angle_degrees, landing_gear):
        ''' Wing flaps are a significant part of the takeoff and landing process. When the airplane is taking off, the flaps help to produce more lift. '''
        ''' Conversely, flaps allow for a steep but controllable angle during landing. '''
        ''' During both, efficient use of flaps help to shorten the amount of runway length needed for takeoff and landing '''
        self.currentDragNewtons = self.drag.nonclean( mass = massKilograms, tas = tasKnots, alt = altitudeMSLfeet, flap_angle = flap_angle_degrees, landing_gear = landing_gear )
        logger.info( self.className + " - non clean drag = {0:.2f} Newtons".format ( self.currentDragNewtons ))
        return self.currentDragNewtons
        
        
    def computeDragNewtons(self , massKilograms , tasKnots , altitudeMSLfeet , verticalSpeedFeetMinutes = 0.0):
        dragNewtons = 0.0
        if self.isDepartureGroundRun():
            flap_angle_degrees = 5.0
            ''' landing gear is extended '''
            landing_gear = True
            #return self.getCleanDragNewtons( massKilograms = massKilograms , tasKnots = tasKnots , altitudeMSLfeet = altitudeMSLfeet , verticalSpeedFeetMinutes = verticalSpeedFeetMinutes)
            dragNewtons = self.getNonCleanDragNewtons( massKilograms , tasKnots , altitudeMSLfeet , flap_angle_degrees, landing_gear)
            
        elif self.isTakeOff():
            flap_angle_degrees = 20.0
            ''' landing gear is extended '''
            landing_gear = True
            #return self.getCleanDragNewtons( massKilograms = massKilograms , tasKnots = tasKnots , altitudeMSLfeet = altitudeMSLfeet , verticalSpeedFeetMinutes = verticalSpeedFeetMinutes)
            dragNewtons = self.getNonCleanDragNewtons( massKilograms , tasKnots , altitudeMSLfeet , flap_angle_degrees, landing_gear)
            
        elif self.isInitialClimb():
            flap_angle_degrees = 15.0
            ''' landing gear is retracted '''
            landing_gear = False
            #return self.getCleanDragNewtons( massKilograms = massKilograms , tasKnots = tasKnots , altitudeMSLfeet = altitudeMSLfeet , verticalSpeedFeetMinutes = verticalSpeedFeetMinutes)
            dragNewtons = self.getNonCleanDragNewtons( massKilograms , tasKnots , altitudeMSLfeet , flap_angle_degrees, landing_gear)
            
        elif self.isClimb():
            #verticalSpeedFeetMinutes = 100.0
            #return self.getCleanDragNewtons( massKilograms = massKilograms , tasKnots = tasKnots , altitudeMSLfeet = altitudeMSLfeet , verticalSpeedFeetMinutes = verticalSpeedFeetMinutes)
            dragNewtons = self.getCleanDragNewtons( massKilograms , tasKnots , altitudeMSLfeet , verticalSpeedFeetMinutes )
            
        elif self.isCruise():
            dragNewtons = self.getCleanDragNewtons( massKilograms , tasKnots , altitudeMSLfeet , verticalSpeedFeetMinutes )
            
        else:
            raise ValueError("not yet implemented")
        
        #logger.info ( self.className + ' - drag = {0:.2f} Newtons'.format( dragNewtons ) )
        return dragNewtons
        
