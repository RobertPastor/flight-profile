'''
Created on 12 nov. 2024

@author: robert
'''

''' Thrust expressed in Newtons '''

import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, Thrust
import json

from trajectory.Openap.AircraftMassFile import OpenapAircraftMass
from trajectory.Openap.AircraftDragFile import OpenapAircraftDrag

import logging 
logger = logging.getLogger(__name__)


class OpenapAircraftThrust(OpenapAircraftDrag):

    def __init__(self, aircraftICAOcode ):
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode)
        
        self.aircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True )
        self.thrust = Thrust(ac=str( aircraftICAOcode ).lower() , eng=None)

        
    def getTakeOffThrust(self, tasKnots , altitudeFeet ):
        self.takeOffThrust = self.thrust.takeoff(tas = tasKnots, alt=altitudeFeet)
        logger.info ( self.className + ': take off thrust = {0:.2f} newtons - tas = {1:.2f} knots at MSL altitude {2} feet'.format(self.takeOffThrust , tasKnots , altitudeFeet) )
        return self.takeOffThrust
