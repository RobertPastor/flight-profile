'''
Created on 14 nov. 2024

@author: robert
'''

from trajectory.Environment.Constants import  Meter2Feet , Feet2Meter, MeterSecond2Knots, RollingFrictionCoefficient, ConstantTaxiSpeedCasKnots,\
    Meter2NauticalMiles
import logging 
import math
from trajectory.Guidance.ConstraintsFile import feet2Meters


logger = logging.getLogger(__name__)
from trajectory.Openap.AircraftEngineFile import OpenapAircraftEngine
from trajectory.Openap.AircaftSpeedsFile import OpenapAircraftSpeeds

from trajectory.Environment.Constants import MeterSecond2Knots

class OpenapAircraftConfiguration(OpenapAircraftSpeeds):
    
    aircraftConfigurationList = ['departure-ground-run',
                                 'take-off', 
                                 'initial-climb', 
                                 'climb',    
                                 'cruise', 
                                 'descent',
                                 'approach', 
                                 'landing',
                                 'arrival-ground-run']
    aircraftCurrentConfiguration = ''
    rollingFrictionCoefficient = RollingFrictionCoefficient        # rolling friction coefficient (mur)
    
    def __init__(self , aircraftICAOcode , earth ):
        
        logger.setLevel(logging.INFO)
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode)
        
        self.earth = earth
        
        self.aircraftCurrentConfiguration = 'departure-ground-run'
        
        logger.info ( self.className  + ' ===================================================' )
        self.aircraftCurrentConfiguration = 'departure-ground-run'
        self.flightPathAngleDegrees = 0.0
        logger.info ( self.className + ' default configuration= ' + self.aircraftCurrentConfiguration )
        logger.info ( self.className + ' ===================================================' )
        
    def computeCurrentThrustNewtons(self , tasKnots, altitudeMSLfeet ):
        if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
            return self.getTakeOffThrust( tasKnots , altitudeMSLfeet )
        
    def computeCurrentDragNewtons(self , massKilograms , tasKnots , altitudeMSLfeet ):
        if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
            flap_angle_degrees = 5.0
            landing_gear = True
            #return self.getCleanDragNewtons( massKilograms = massKilograms , tasKnots = tasKnots , altitudeMSLfeet = altitudeMSLfeet , verticalSpeedFeetMinutes = verticalSpeedFeetMinutes)
            dragNewtons = self.getNonCleanDragNewtons( massKilograms , tasKnots , altitudeMSLfeet , flap_angle_degrees, landing_gear)
            return dragNewtons
        
    def computeCurrentLiftNewtons(self):
        if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
            return 0.0
        
    def computeFlightPathAngleDegrees(self):
        if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
            return 0.0
        
    def computeFuelFlowKilograms(self , TASknots , altitudeMSLfeet ):
        if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
            fuelFlowKilogramseconds = self.getFuelFlowAtTakeOffKgSeconds( TASknots=TASknots, altitudeMSLfeet=altitudeMSLfeet )
            return fuelFlowKilogramseconds
        
    
    def fly(self , elapsedTimeSeconds, 
            deltaTimeSeconds, 
            totalDistanceFlownMeters=0.0,
            distanceStillToFlyMeters=0.0,
            currentPosition=None,
            distanceToLastFixMeters=None):
        '''
        main aircraft entry point : computes for a delta time 
        1) the ground distance flown (hence needs a ground speed)
        Needs = ground speed => obtained from TAS and Wind speed
        2) the delta increase - decrease in altitude
        
        '''
        
        altitudeMSLfeet = 100.0
        latitudeDegrees = 45.0
        
        gravityCenterMetersPerSquaredSeconds = self.earth.gravity(self.earth.getRadiusMeters() + altitudeMSLfeet * feet2Meters, math.radians(latitudeDegrees))[0]
        logger.info( self.className + " --- gravity at a given latitude = {0:.2f} m/s2".format( gravityCenterMetersPerSquaredSeconds ))

        if ( elapsedTimeSeconds < deltaTimeSeconds ):
            ''' display this only once'''
            logger.info( self.className + " -----------------------------")
            logger.info( self.className + " ----- start flying ----------")
            logger.info( self.className + " -----------------------------")
        else:
            logger.info( self.className + " -----------------------------")
            logger.info( self.className + " ----- elapsed {0} seconds----".format (elapsedTimeSeconds ))
            logger.info( self.className + " -----------------------------")
            
        tasKnots = self.getCurrentTASspeedKnots()
        aircraftMassKilograms = self.getCurrentMassKilograms()
        
        thrustNewtons = self.computeCurrentThrustNewtons( tasKnots , altitudeMSLfeet)
        dragNewtons = self.computeCurrentDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet  )
        liftNewtons = self.computeCurrentLiftNewtons()
        
        aircraftAccelerationMetersSecondSquare = thrustNewtons - dragNewtons - self.rollingFrictionCoefficient * ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds - liftNewtons)
        aircraftAccelerationMetersSecondSquare = aircraftAccelerationMetersSecondSquare / aircraftMassKilograms
        trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
        trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + ( aircraftAccelerationMetersSecondSquare * deltaTimeSeconds )
        
        logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
        self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
        
        ''' distance flown '''
        flightPathAngleDegrees = self.computeFlightPathAngleDegrees()
        deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
        totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
        logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

        fuelFlowKilogramsSeconds = self.computeFuelFlowKilograms(trueAirSpeedMetersSecond * MeterSecond2Knots , altitudeMSLfeet)
        aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
        self.setAircraftMassKilograms(aircraftMassKilograms)

        return totalDistanceFlownMeters
        