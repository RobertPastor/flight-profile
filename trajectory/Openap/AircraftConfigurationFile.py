'''
Created on 14 nov. 2024

@author: robert
'''

import sys
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, FuelFlow, Emission, WRAP

from trajectory.Environment.Constants import  Meter2Feet , Feet2Meter, MeterSecond2Knots, RollingFrictionCoefficient, ConstantTaxiSpeedCasKnots
from trajectory.Environment.Constants import     Meter2NauticalMiles, MaxRateOfClimbFeetPerMinutes , FeetMinutes2MetersSeconds
import logging 
import math
from trajectory.Guidance.ConstraintsFile import feet2Meters


logger = logging.getLogger(__name__)
from trajectory.Openap.AircraftEngineFile import OpenapAircraftEngine
from trajectory.Openap.AircaftSpeedsFile import OpenapAircraftSpeeds
from trajectory.aerocalc.airspeed import tas2cas, tas2mach

from trajectory.Environment.Constants import MeterSecond2Knots, Knots2MetersSeconds

class OpenapAircraftConfiguration(OpenapAircraftSpeeds):
    
    rollingFrictionCoefficient = RollingFrictionCoefficient        # rolling friction coefficient (mur)
    
    def __init__(self , aircraftICAOcode , earth , atmosphere ):
        
        logger.setLevel(logging.INFO)
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode)
        
        self.earth = earth
        self.atmosphere = atmosphere
        
        self.distanceFlownMeters = 0.0
        
        self.aircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True )
        self.ceilingMeters = self.aircraft['ceiling']

        
    def computeLiftCoeff(self, aircraftMassKilograms, altitudeMSLmeters, TrueAirSpeedMetersSecond, latitudeDegrees):
        '''
        lift coeff = ( 2 * aircraft-mass * gravity ) / ( rho * TAS * TAS * WingSurface ) 
        '''
        if self.isDepartureGroundRun():
            liftCoeff = 0.1
        else:
            gravityCenterMetersPerSquaredSeconds = self.earth.gravityWelmec( heightMSLmeters = altitudeMSLmeters , latitudeDegrees = latitudeDegrees)
            airDensity = self.atmosphere.getAirDensityKilogramsPerCubicMeters(altitudeMSLmeters)
            liftCoeff = 2 * aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds
            if TrueAirSpeedMetersSecond > 0.0:
                wingAreaSurfaceSquareMeters = self.getWingAreaSurfaceSquareMeters()
                liftCoeff = liftCoeff / ( airDensity * TrueAirSpeedMetersSecond * TrueAirSpeedMetersSecond * wingAreaSurfaceSquareMeters)
            else:
                liftCoeff = 0.0
        return liftCoeff

        
    def computeLiftNewtons(self, aircraftMassKilograms, altitudeMeanSeaLevelMeters, trueAirSpeedMetersSecond, latitudeDegrees):
        '''  Qinf = 0.5 * rho * (aircraftSpeed ** 2) '''
        '''  Lift = Qinf * aircraft.WingPlanformAreaSquareMeters * CL '''
        ''' @todo '''
        #@TODO logger.info 'to be fixed... aircraft mass ... depends upon flight path range in Kilometers + reserve'
        liftCoeff = self.computeLiftCoeff(  aircraftMassKilograms, altitudeMeanSeaLevelMeters, trueAirSpeedMetersSecond, latitudeDegrees)
        liftNewtons = 0.5 * self.atmosphere.getAirDensityKilogramsPerCubicMeters(altitudeMeanSeaLevelMeters)
        liftNewtons = liftNewtons * trueAirSpeedMetersSecond * trueAirSpeedMetersSecond
        liftNewtons = liftNewtons * self.getWingAreaSurfaceSquareMeters() * liftCoeff
        logger.info ( self.className + ' - lift = {0:.2f} Newtons'.format( liftNewtons ) )

        return liftNewtons
        
    def computeFlightPathAngleDegrees(self , rateOfClimbMetersPerSeconds = 0.0, trueAirspeedMetersPerSeconds = 0.0):
        if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
            return 0.0
        else:
            flightPathAngleDegrees = math.degrees(math.asin( rateOfClimbMetersPerSeconds / trueAirspeedMetersPerSeconds))
            logger.info ( self.className + ' - flight path angle = {0:.2f} degrees'.format( flightPathAngleDegrees) )
            return flightPathAngleDegrees
        
    
    def setAltitudeMSLfeet(self , altitudeMSLfeet ):
        self.altitudeMSLmeters = altitudeMSLfeet * feet2Meters
        
    def getAltitudeMSLmeters(self):
        return self.altitudeMSLmeters
    
    def setDistanceFlownMeters(self , distanceFlownMeters ):
        self.distanceFlownMeters = distanceFlownMeters
        
    def getDistanceFlownMeters(self):
        return self.distanceFlownMeters
    
    def setDepartureRunwayMSLmeters(self, departureRunwayMSLmeters ):
        self.departureRunwayMSLmeters = departureRunwayMSLmeters
        
    def getDepartureRunwayMSLmeters(self):
        return self.departureRunwayMSLmeters
    
    def fly(self , elapsedTimeSeconds, 
            deltaTimeSeconds, 
            totalDistanceFlownMeters=0.0,
            altitudeMSLmeters=0.0,
            distanceStillToFlyMeters=0.0,
            currentPosition=None,
            distanceToLastFixMeters=None):
        '''
        main aircraft entry point : computes for a delta time 
        1) the ground distance flown (hence needs a ground speed)
        Needs = ground speed => obtained from TAS and Wind speed
        2) the delta increase - decrease in altitude
        
        '''
        
        altitudeMSLfeet = altitudeMSLmeters * Meter2Feet
        self.setAltitudeMSLfeet(altitudeMSLfeet)
        
        latitudeDegrees = 45.0
        latitudeRadians = math.radians(latitudeDegrees)
        
        gravityCenterMetersPerSquaredSeconds = self.earth.gravityWelmec( heightMSLmeters = altitudeMSLmeters, latitudeDegrees = latitudeDegrees )
        logger.info( self.className + " --- gravity at a given altitude = {0:.2f} m/s2 at altitude = {1:.2f} meters".format( gravityCenterMetersPerSquaredSeconds , altitudeMSLmeters ))

        if ( elapsedTimeSeconds < deltaTimeSeconds ):
            ''' display this only once'''
            logger.info( self.className + " -----------------------------")
            logger.info( self.className + " ----- start flying ----------")
            logger.info( self.className + " -----------------------------")
        else:
            logger.info( self.className + " ---------------------------------------------------")
            logger.info( self.className + " ----- {0} - elapsed time {1} seconds----".format ( self.aircraftCurrentConfiguration , elapsedTimeSeconds ) )
            logger.info( self.className + " ---------------------------------------------------")
            
        tasKnots = self.getCurrentTASspeedKnots()
        aircraftMassKilograms = self.getCurrentMassKilograms()
        
        if self.isDepartureGroundRun():
            
            rateOfClimbFeetMinutes = 0.0
            ''' as openap wrap has not a correct drag computation during ground run '''
            ''' use the mean acceleration '''
            
            aircraftAccelerationMetersSecondSquare = self.getMinimumTakeOffAccelerationMetersSecondsSquare()
            logger.info( self.className + " - aircraft acceleration = {0:.2f} meters per seconds square".format( aircraftAccelerationMetersSecondSquare ))

            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + ( aircraftAccelerationMetersSecondSquare * deltaTimeSeconds )
            
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
            
            ''' distance flown '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees()
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))
    
            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilograms(trueAirSpeedMetersSecond * MeterSecond2Knots , altitudeMSLfeet , aircraftMassKilograms , rateOfClimbFeetMinutes)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)
            
            casKnots = tas2cas( tas = trueAirSpeedMetersSecond, altitude = altitudeMSLfeet , temp = 'std' , speed_units = 'm/s', alt_units = 'ft') * MeterSecond2Knots
            logger.info( self.className + " - CAS = {0:.2f} meters per second - CAS = {1:.2f} knots ".format( casKnots * Knots2MetersSeconds , casKnots ) )
    
            if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
                if ( casKnots >= ( 1.2 * self.getDefaultTakeOffCASknots() ) ):
                    logger.debug ( self.className + ' CAS= {0:.2f} knots >= takeoff Stall Speed= {1:.2f} knots'.format(casKnots, self.getDefaultTakeOffCASknots()) )
                    self.setTakeOffConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
            
            
        elif self.isTakeOff():
                        
            ''' no more rolling friction and usage of flaps and flight angle = 8 degrees '''
            ''' gear is still extended '''
            rateOfClimbFeetMinutes = 1000.0
            rateOfClimbMetersSeconds = rateOfClimbFeetMinutes * FeetMinutes2MetersSeconds
            
            thrustNewtons = self.computeCurrentThrustNewtons( tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes)
            dragNewtons = self.computeCurrentDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet  )
            
            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            liftNewtons = self.computeLiftNewtons( aircraftMassKilograms = aircraftMassKilograms, altitudeMeanSeaLevelMeters =  altitudeMSLmeters, trueAirSpeedMetersSecond = trueAirSpeedMetersSecond , latitudeDegrees=latitudeDegrees)

            ''' compute new True Air Speed '''
            aircraftAccelerationMetersSecondSquare = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * rateOfClimbMetersSeconds )/ trueAirSpeedMetersSecond ) 
            trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + aircraftAccelerationMetersSecondSquare * deltaTimeSeconds
            
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
             
            ''' distance flown '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees( rateOfClimbMetersSeconds , trueAirSpeedMetersSecond )
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilograms(TASknots=trueAirSpeedMetersSecond * MeterSecond2Knots , 
                                                                     aircraftAltitudeMSLfeet=altitudeMSLfeet , 
                                                                     aircraftMassKilograms=aircraftMassKilograms, 
                                                                     rateOfClimbFeetMinutes=rateOfClimbFeetMinutes)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)

            ''' transition to initial climb as soon as height above ground is 1000 feet / 300 meters '''
            deltaAltitudeMeters = rateOfClimbMetersSeconds * deltaTimeSeconds
            altitudeMSLmeters = altitudeMSLmeters + deltaAltitudeMeters
            logger.info( self.className + " - departure runway MSL altitude = {0:.2f} meters - aircraft altitude MSL = {1:.2f} meters ".format( self.getDepartureRunwayMSLmeters() , altitudeMSLmeters ))
            
            AboveGroundMeters = 300.0
            if ( altitudeMSLmeters > self.getDepartureRunwayMSLmeters() + AboveGroundMeters):
                self.setInitialClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
                
        
        elif self.isInitialClimb():
            ''' aircraft is airborne and landing gear is retracted '''
            
            rateOfClimbFeetMinutes = 2000.0
            rateOfClimbMetersSeconds = rateOfClimbFeetMinutes * FeetMinutes2MetersSeconds
            
            thrustNewtons = self.computeCurrentThrustNewtons( tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes)
            dragNewtons = self.computeCurrentDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet  )
            
            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            liftNewtons = self.computeLiftNewtons( aircraftMassKilograms = aircraftMassKilograms, altitudeMeanSeaLevelMeters =  altitudeMSLmeters, trueAirSpeedMetersSecond = trueAirSpeedMetersSecond , latitudeDegrees=latitudeDegrees)
            
            ''' compute new True Air Speed '''
            aircraftAccelerationMetersSecondSquare = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * rateOfClimbMetersSeconds )/ trueAirSpeedMetersSecond ) 
            trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + aircraftAccelerationMetersSecondSquare * deltaTimeSeconds
            
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
             
            ''' distance flown '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees( rateOfClimbMetersSeconds , trueAirSpeedMetersSecond )
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilograms(TASknots=trueAirSpeedMetersSecond * MeterSecond2Knots , 
                                                                     aircraftAltitudeMSLfeet=altitudeMSLfeet , 
                                                                     aircraftMassKilograms=aircraftMassKilograms , 
                                                                     rateOfClimbFeetMinutes=rateOfClimbFeetMinutes,
                                                                     acceleationMetersSecondsSquare=aircraftAccelerationMetersSecondSquare)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)

            ''' transition to initial climb as soon as height above ground is 1000 feet / 300 meters '''
            deltaAltitudeMeters = rateOfClimbMetersSeconds * deltaTimeSeconds
            altitudeMSLmeters = altitudeMSLmeters + deltaAltitudeMeters
            if ( ( altitudeMSLmeters * Meter2Feet ) > 1500.0):
                self.setClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
                

        elif self.isClimb():
            ''' We consider the climbing section up to 1500 ft to be the initial climb. '''

            rateOfClimbFeetMinutes = 2500.0
            rateOfClimbMetersSeconds = rateOfClimbFeetMinutes * FeetMinutes2MetersSeconds
            
            thrustNewtons = self.computeCurrentThrustNewtons( tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes)
            dragNewtons = self.computeCurrentDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet  )
            
            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            liftNewtons = self.computeLiftNewtons( aircraftMassKilograms = aircraftMassKilograms, altitudeMeanSeaLevelMeters =  altitudeMSLmeters, trueAirSpeedMetersSecond = trueAirSpeedMetersSecond , latitudeDegrees=latitudeDegrees)
            
            ''' compute new True Air Speed '''
            aircraftAccelerationMetersSecondSquare = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * rateOfClimbMetersSeconds )/ trueAirSpeedMetersSecond ) 
            trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + aircraftAccelerationMetersSecondSquare * deltaTimeSeconds
            
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
             
            ''' distance flown '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees( rateOfClimbMetersSeconds , trueAirSpeedMetersSecond )
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilograms(TASknots=trueAirSpeedMetersSecond * MeterSecond2Knots , 
                                                                     aircraftAltitudeMSLfeet=altitudeMSLfeet , 
                                                                     aircraftMassKilograms=aircraftMassKilograms , 
                                                                     rateOfClimbFeetMinutes=rateOfClimbFeetMinutes,
                                                                     acceleationMetersSecondsSquare=aircraftAccelerationMetersSecondSquare)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)

            ''' transition to initial climb as soon as height above ground is 1000 feet / 300 meters '''
            deltaAltitudeMeters = rateOfClimbMetersSeconds * deltaTimeSeconds
            altitudeMSLmeters = altitudeMSLmeters + deltaAltitudeMeters
            if ( altitudeMSLmeters > ( self.ceilingMeters - 300.0 )) and ( altitudeMSLmeters < ( self.ceilingMeters - 300.0   ) ):
                self.setCruiseConfiguration( elapsedTimeSeconds + deltaTimeSeconds )


        elif self.isCruise():
            '''The final approach starts from 1000 ft toward the end of the descent '''
            
            rateOfClimbFeetMinutes = 0.0
            rateOfClimbMetersSeconds = 0.0

            
        
        
        
        else:
            
            raise ValueError("not yet implemented")
    
  

        return totalDistanceFlownMeters , altitudeMSLmeters
        