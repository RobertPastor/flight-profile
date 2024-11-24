'''
Created on 14 nov. 2024

@author: robert
'''

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
    
    def __init__(self , aircraftICAOcode , earth , atmosphere ):
        
        logger.setLevel(logging.INFO)
        self.className = self.__class__.__name__
        super().__init__(aircraftICAOcode)
        
        self.earth = earth
        self.atmosphere = atmosphere
        
        self.aircraftCurrentConfiguration = 'departure-ground-run'
        
        logger.info ( self.className  + ' ===================================================' )
        self.aircraftCurrentConfiguration = 'departure-ground-run'
        self.flightPathAngleDegrees = 0.0
        logger.info ( self.className + ' default configuration= ' + self.aircraftCurrentConfiguration )
        logger.info ( self.className + ' ===================================================' )
        
        self.distanceFlownMeters = 0.0
        
    def computeCurrentThrustNewtons(self , tasKnots, altitudeMSLfeet , rateOfClimbFeetMinutes = 0.0):
        if self.isDepartureGroundRun():
            return self.getTakeOffThrustNewtons( tasKnots = tasKnots, altitudeMSLfeet = altitudeMSLfeet)
        elif self.isTakeOff():
            return self.getClimbThrustNewtons( tasKnots = tasKnots ,  altitudeMSLfeet = altitudeMSLfeet , rateOfClimbFeetMinutes = rateOfClimbFeetMinutes)
        elif self.isInitialClimb():
            return self.getClimbThrustNewtons( tasKnots = tasKnots ,  altitudeMSLfeet = altitudeMSLfeet , rateOfClimbFeetMinutes = rateOfClimbFeetMinutes)
        elif self.isClimb():
            return self.getClimbThrustNewtons( tasKnots = tasKnots ,  altitudeMSLfeet = altitudeMSLfeet , rateOfClimbFeetMinutes = rateOfClimbFeetMinutes)
        elif self.isCruise():
            return self.getCruiseThrustNewtons ( tasKnots = tasKnots ,  altitudeMSLfeet = altitudeMSLfeet )
            
        
    def computeCurrentDragNewtons(self , massKilograms , tasKnots , altitudeMSLfeet ):
        dragNewtons = 0.0
        if self.isDepartureGroundRun():
            flap_angle_degrees = 5.0
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
            ''' landing gear is retracted '''
            flap_angle_degrees = 15.0
            landing_gear = False
            #return self.getCleanDragNewtons( massKilograms = massKilograms , tasKnots = tasKnots , altitudeMSLfeet = altitudeMSLfeet , verticalSpeedFeetMinutes = verticalSpeedFeetMinutes)
            dragNewtons = self.getNonCleanDragNewtons( massKilograms , tasKnots , altitudeMSLfeet , flap_angle_degrees, landing_gear)
            
        else:
            raise ValueError("not yet implemented")
        
        logger.info ( self.className + ' - drag = {0:.2f} Newtons'.format( dragNewtons ) )
        return dragNewtons
        
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
        
    def computeFuelFlowKilograms(self , TASknots , aircraftAltitudeMSLfeet , aircraftMassKilograms=0.0, rateOfClimbFeetMinutes=0.0, acceleationMetersSecondsSquare=0.0):
        if self.isDepartureGroundRun():
            fuelFlowKilogramseconds = self.getFuelFlowAtTakeOffKgSeconds( TASknots=TASknots, aircraftAltitudeMSLfeet=aircraftAltitudeMSLfeet )
            return fuelFlowKilogramseconds
        elif self.isTakeOff():
            fuelFlowKilogramseconds = self.getFuelFlowClimbKgSeconds( aircraftMassKilograms=aircraftMassKilograms , TASknots=TASknots , aircraftAltitudeMSLfeet=aircraftAltitudeMSLfeet , rateOfClimbFeetMinutes=rateOfClimbFeetMinutes, acceleationMetersSecondsSquare=acceleationMetersSecondsSquare)
            return fuelFlowKilogramseconds
        elif self.isInitialClimb():
            fuelFlowKilogramseconds = self.getFuelFlowClimbKgSeconds( aircraftMassKilograms=aircraftMassKilograms , TASknots=TASknots , aircraftAltitudeMSLfeet=aircraftAltitudeMSLfeet , rateOfClimbFeetMinutes=rateOfClimbFeetMinutes, acceleationMetersSecondsSquare=acceleationMetersSecondsSquare)
            return fuelFlowKilogramseconds
            
        
    def setTakeOffConfiguration(self, elapsedTimeSeconds):
        ''' take off starts at the end of the ground-run when speed > 1.2 * Take-off stall speed '''
        ''' high lifting devices are used '''
        newConfiguration = 'take-off'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration
        
    def setInitialClimbConfiguration(self, elapsedTimeSeconds):
        ''' high lifting devices are used - wheels are hidden '''
        newConfiguration = 'initial-climb'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration
            
    def isDepartureGroundRun(self):
        return (self.aircraftCurrentConfiguration=='departure-ground-run')
    
    def isTakeOff(self):
        return (self.aircraftCurrentConfiguration=='take-off')
    
    def isInitialClimb(self):
        return (self.aircraftCurrentConfiguration=='initial-climb')

    def isClimb(self):
        return (self.aircraftCurrentConfiguration=='climb')
            
    def isCruise(self):
        return (self.aircraftCurrentConfiguration=='cruise')
    
    def isDescent(self):
        return (self.aircraftCurrentConfiguration=='descent')
    
    def isApproach(self):
        return (self.aircraftCurrentConfiguration=='approach')
    
    def isLanding(self):
        return (self.aircraftCurrentConfiguration=='landing')
    
    def isArrivalGroundRun(self):
        return (self.aircraftCurrentConfiguration=='arrival-ground-run')
            
    def showConfigurationChange(self, newConfiguration, elapsedTimeSeconds):
        assert isinstance(newConfiguration, str)
        altitudeMeanSeaLevelMeters = self.getAltitudeMSLmeters()
        currentDistanceFlownMeters = self.getDistanceFlownMeters()
        tas = self.getCurrentTrueAirSpeedMetersSecond()
        #cas = self.atmosphere.tas2cas(tas = tas, altitude = altitudeMeanSeaLevelMeters,alt_units='m', speed_units='m/s',)
        cas = tas2cas(tas = tas, altitude = altitudeMeanSeaLevelMeters, temp='std', speed_units='m/s', alt_units='m')
        #mach = self.atmosphere.tas2mach(tas = tas, altitude = altitudeMeanSeaLevelMeters, alt_units='m', speed_units='m/s')
        mach = tas2mach(tas = tas , temp='std', altitude = altitudeMeanSeaLevelMeters, temp_units= 'C', speed_units='m/s')
        logger.info ( self.className + ' ====================================' )
        logger.info ( self.className + ' entering {0} configuration - distance flown {1:.2f} meters - distance flown {2:.2f} Nm'.format(newConfiguration, currentDistanceFlownMeters, currentDistanceFlownMeters*Meter2NauticalMiles) )
        logger.info ( self.className + ' alt= {0:.2f} meters alt= {1:.2f} feet'.format(altitudeMeanSeaLevelMeters, altitudeMeanSeaLevelMeters * Meter2Feet ) ) 
        logger.info ( self.className + ' TAS= {0:.2f} m/s - TAS= {1:.2f} knots - CAS= {2:.2f} m/s - CAS= {3:.2f} knots - Mach= {4:.2f}'.format(tas, (tas*MeterSecond2Knots), cas, (cas*MeterSecond2Knots), mach) )
        logger.info ( self.className + ' ====================================' )

    
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
            logger.info( self.className + " -----------------------------")
            logger.info( self.className + " ----- elapsed {0} seconds----".format (elapsedTimeSeconds ))
            logger.info( self.className + " -----------------------------")
            
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
                    logger.debug ( self.className + ' CAS= {0:.2f} knots >= Initial Climb Stall Speed= {1:.2f} knots'.format(casKnots, self.getDefaultTakeOffCASknots()) )
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
            
            if ( altitudeMSLmeters > self.getDepartureRunwayMSLmeters() + 300.0):
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

            
        
        else:
            
        
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
            
            casKnots = tas2cas( tas = trueAirSpeedMetersSecond, altitude = altitudeMSLfeet , temp = 'std' , speed_units = 'm/s', alt_units = 'ft') * MeterSecond2Knots
            logger.info( self.className + " - CAS = {0:.2f} meters per second - CAS = {1:.2f} knots ".format( casKnots * Knots2MetersSeconds , casKnots ) )
    
            if ( self.aircraftCurrentConfiguration == 'departure-ground-run' ):
                if ( casKnots >= ( 1.2 * self.getDefaultTakeOffCASknots() ) ):
                    logger.debug ( self.className + ' CAS= {0:.2f} knots >= Initial Climb Stall Speed= {1:.2f} knots'.format(casKnots, self.getDefaultTakeOffCASknots()) )
                    self.setInitialClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)


        return totalDistanceFlownMeters , altitudeMSLmeters
        