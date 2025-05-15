'''
Created on 6 mai 2025

@author: robert
'''
import logging 
from trajectory.Openap.AircraftFlightPhasesFile import OpenapAircraftFlightPhases
from trajectory.Guidance.WayPointFile import WayPoint

from openap import prop, WRAP


class OpenapAircraftMiscelleaneous(OpenapAircraftFlightPhases):
    pass

    def __init__(self, aircraftICAOcode):
        
        self.className = self.__class__.__name__
        self.aircraftICAOcode = aircraftICAOcode
        
        super().__init__(aircraftICAOcode)
        self.wrap = WRAP(str(aircraftICAOcode).upper(), use_synonym=True)
        
    def getLandingLengthMeters(self):
        self.LandingLengthMetersDict = self.wrap.landing_distance()
        self.LandingLengthMeters = self.LandingLengthMetersDict['default'] * 1000.0
        logging.info( self.className + " - landing length = {0} meters".format(self.LandingLengthMeters))
        return self.LandingLengthMeters
    
    def setTargetApproachWayPoint(self , approachWayPoint):
        ''' it is the top of the last turn before the descent glide slope to the arrival runway '''
        self.approachWayPoint = approachWayPoint
        
    def getTargetApproachWayPoint(self):
        ''' it is the top of the last turn before the descent glide slope to the arrival runway '''
        assert ( self.approachWayPoint and isinstance(self.approachWayPoint, WayPoint) )
        return self.approachWayPoint
    
    def setArrivalRunwayTouchDownWayPoint(self , touchDownWayPoint ):
        self.touchDownWayPoint = touchDownWayPoint
        
    def getArrivalRunwayTouchDownPoint(self):
        assert ( self.touchDownWayPoint and isinstance( self.touchDownWayPoint , WayPoint ))
        return self.touchDownWayPoint