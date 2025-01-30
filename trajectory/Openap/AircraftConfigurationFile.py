'''
Created on 14 nov. 2024

@author: robert
'''

import sys
import math
import json
sys.path.append("C:/Users/rober/git/openap/") #replace PATH with the path to Foo

from openap import prop, FuelFlow, Emission, WRAP

from trajectory.Environment.Constants import  Meter2Feet , Feet2Meter, MeterSecond2Knots, RollingFrictionCoefficient, ConstantTaxiSpeedCasKnots
from trajectory.Environment.Constants import Meter2NauticalMiles, MaxRateOfClimbFeetPerMinutes , FeetMinutes2MetersSeconds
from trajectory.Environment.Constants import MeterSeconds2FeetMinutes 
from trajectory.Environment.Constants import MeterSecond2Knots, Knots2MetersSeconds

import logging 
import math
from trajectory.Guidance.ConstraintsFile import feet2Meters


logger = logging.getLogger(__name__)
from trajectory.Openap.AircaftSpeedsFile import OpenapAircraftSpeeds
from trajectory.aerocalc.airspeed import tas2cas, tas2mach, cas2tas


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
        
        self.wrap = WRAP(str(aircraftICAOcode).upper(), use_synonym=True)
        #self.ceilingMeters = self.aircraft['ceiling']

        
    def computeLiftCoeff(self, aircraftMassKilograms, altitudeMSLmeters, TrueAirSpeedMetersSecond, latitudeDegrees):
        '''
        lift coeff = ( 2 * aircraft-mass * gravity ) / ( rho * TAS * TAS * WingSurface ) 
        '''
        if self.isTakeOff():
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
            if trueAirspeedMetersPerSeconds < 3e-3:
                return 0.0
            try:
                flightPathAngleDegrees = min ( math.degrees ( math.asin( rateOfClimbMetersPerSeconds / trueAirspeedMetersPerSeconds)) , 4.0 )
            except Exception as e:
                print( self.className + " - exception = {0}".format( e ))
                return 0.0
            logger.info ( self.className + ' - flight path angle = {0:.2f} degrees'.format( flightPathAngleDegrees) )
            return flightPathAngleDegrees
        
    
    def setAltitudeMSLfeet(self , altitudeMSLfeet ):
        self.altitudeMSLmeters = altitudeMSLfeet * feet2Meters
        
    def getAltitudeMSLmeters(self):
        return self.altitudeMSLmeters
    
    def setDepartureRunwayMSLmeters(self, departureRunwayMSLmeters ):
        self.departureRunwayMSLmeters = departureRunwayMSLmeters
        
    def getDepartureRunwayMSLmeters(self):
        return self.departureRunwayMSLmeters
    
    def setArrivalRunwayMSLmeters(self , arrivalRunwayMSLmeters ):
        self.arrivalRunwayMSLmeters = arrivalRunwayMSLmeters
        
    def getArrivalRunwayMSLmeters(self):
        return self.arrivalRunwayMSLmeters
    
    def setCruiseLevelFeet(self ):
        print ( json.dumps ( self.wrap.cruise_alt() ) )
        self.cruiseLevelFeet = self.wrap.cruise_alt()['default'] * 1000.0 * Meter2Feet
        
    def getCruiseLevelFeet(self):
        return self.cruiseLevelFeet
    
    def computeRateOfClimbFeetMinutes(self , rateOfClimbFeetMinutes , altitudeMSLfeet ):
        if ( altitudeMSLfeet < ( self.getCruiseLevelFeet() - 2500.0 )):
            return rateOfClimbFeetMinutes
        else:
            if (altitudeMSLfeet < ( self.cruiseLevelFeet - 100.0 ) ):
                ''' 5 minutes to close the gap '''
                rateOfClimbFeetMinutes = abs ( self.getCruiseLevelFeet() - altitudeMSLfeet ) / 5.0
            else:
                rateOfClimbFeetMinutes = 100.0
        return rateOfClimbFeetMinutes
    
    def fly(self , elapsedTimeSeconds, 
            deltaTimeSeconds, 
            totalDistanceFlownMeters = 0.0,
            altitudeMSLmeters        = 0.0,
            distanceStillToFlyMeters = 0.0,
            currentPosition          = None,
            distanceToLastFixMeters  = None):
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

        tasKnots = self.getCurrentTASspeedKnots()
        aircraftMassKilograms = self.getCurrentMassKilograms()

        if ( elapsedTimeSeconds < deltaTimeSeconds ):
            ''' display this only once'''
            logger.info( self.className + " -----------------------------")
            logger.info( self.className + " ----- start flying ----------")
            logger.info( self.className + " -----------------------------")
            self.initStateVector(elapsedTimeSeconds , self.getCurrentConfiguration() , 0.0 , 0.0 , altitudeMSLmeters , aircraftMassKilograms)
        else:
            logger.info( self.className + " ---------------------------------------------------")
            logger.info( self.className + " ----- {0} - elapsed time {1} seconds----".format ( self.aircraftCurrentConfiguration , elapsedTimeSeconds ) )
            logger.info( self.className + " ---------------------------------------------------")
            
        
        if self.isTakeOff():
            
            rateOfClimbFeetMinutes = 0.0
            rateOfClimbMetersSeconds = rateOfClimbFeetMinutes * FeetMinutes2MetersSeconds
            
            thrustNewtons = self.computeThrustNewtons( tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes)
            dragNewtons = self.computeDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet  )

            ''' as openap wrap has not a correct drag computation during ground run / takeoff '''
            ''' use the mean acceleration '''
            
            aircraftAccelerationMetersSecondSquare = self.getDefaultTakeOffAccelerationMetersSecondsSquare()
            logger.info( self.className + " - aircraft acceleration = {0:.2f} meters per seconds square".format( aircraftAccelerationMetersSecondSquare ))

            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + ( aircraftAccelerationMetersSecondSquare * deltaTimeSeconds )
            
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
            
            ''' distance flown '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees( rateOfClimbMetersSeconds , trueAirSpeedMetersSecond )
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            self.setTotalDistanceFlownMeters(totalDistanceFlownMeters)
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))
    
            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilogramsSeconds(trueAirSpeedMetersSecond * MeterSecond2Knots , altitudeMSLfeet , aircraftMassKilograms , rateOfClimbFeetMinutes)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)
            
            casKnots = tas2cas( tas = trueAirSpeedMetersSecond, altitude = altitudeMSLfeet , temp = 'std' , speed_units = 'm/s', alt_units = 'ft') * MeterSecond2Knots
            logger.info( self.className + " - CAS = {0:.2f} meters per second - CAS = {1:.2f} knots ".format( casKnots * Knots2MetersSeconds , casKnots ) )
    
            if ( casKnots >= self.getDefaultTakeOffCASknots() ):
                logger.debug ( self.className + ' CAS= {0:.2f} knots >= takeoff Stall Speed= {1:.2f} knots'.format(casKnots, self.getDefaultTakeOffCASknots()) )
                self.setInitialClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
            
        
        elif self.isInitialClimb():
            ''' aircraft is airborne and landing gear is retracted '''
            
            rateOfClimbMetersSeconds = self.getInitialClimbVerticalRateMeterSeconds()
            rateOfClimbFeetMinutes = rateOfClimbMetersSeconds * MeterSeconds2FeetMinutes
            
            thrustNewtons = self.computeThrustNewtons( tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes)
            dragNewtons = self.computeDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet  )
            
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
            self.setTotalDistanceFlownMeters(totalDistanceFlownMeters)
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilogramsSeconds(TASknots         = trueAirSpeedMetersSecond * MeterSecond2Knots , 
                                                                     aircraftAltitudeMSLfeet = altitudeMSLfeet , 
                                                                     aircraftMassKilograms   = aircraftMassKilograms , 
                                                                     verticalRateFeetMinutes  = rateOfClimbFeetMinutes,
                                                                     accelerationMetersSecondsSquare = aircraftAccelerationMetersSecondSquare)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)
                
            ''' transition to  climb as soon as height above ground is 35 feet above ground '''
            deltaAltitudeMeters = rateOfClimbMetersSeconds * deltaTimeSeconds
            altitudeMSLmeters = altitudeMSLmeters + deltaAltitudeMeters
            logger.info( self.className + " - departure runway MSL altitude = {0:.2f} meters - aircraft altitude MSL = {1:.2f} meters ".format( self.getDepartureRunwayMSLmeters() , altitudeMSLmeters ))
            
            AboveGroundMeters = 35.0 * feet2Meters
            ''' From the application of takeoff power, through rotation and to an altitude of 35 feet above runway elevation.  '''
            if ( altitudeMSLmeters > self.getDepartureRunwayMSLmeters() + AboveGroundMeters):
                self.setClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)


        elif self.isClimb():
            ''' We consider the climbing section up to 1500 ft to be the initial climb. '''
            ''' The climb segment starts when the aircraft reaches clean configuration ''' 
            ''' and lasts until the moment when it reaches cruise altitude '''
            
            rateOfClimbMetersSeconds = self.getClimbVerticalRateMeterSeconds( altitudeMSLfeet )
            rateOfClimbFeetMinutes = rateOfClimbMetersSeconds * MeterSeconds2FeetMinutes

            rateOfClimbFeetMinutes = self.computeRateOfClimbFeetMinutes ( rateOfClimbFeetMinutes , altitudeMSLfeet )
            rateOfClimbMetersSeconds = rateOfClimbFeetMinutes * FeetMinutes2MetersSeconds
            
            #rateOfClimbMetersSeconds = self.computeROCD(deltaTimeSeconds, thrustNewtons, dragNewtons, trueAirSpeedMetersSecond, aircraftMassKilograms, gravityCenterMetersPerSquaredSeconds)
            
            thrustNewtons = self.computeThrustNewtons( tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes)
            dragNewtons = self.computeDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes )
            
            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            liftNewtons = self.computeLiftNewtons( aircraftMassKilograms = aircraftMassKilograms, altitudeMeanSeaLevelMeters =  altitudeMSLmeters, trueAirSpeedMetersSecond = trueAirSpeedMetersSecond , latitudeDegrees=latitudeDegrees)
            
            ''' compute new True Air Speed '''
            ''' dVTAS/dt = ( T - D ) / m - ( ( g0 * dh /dt ) / VTas ) '''
            aircraftAccelerationMetersSecondSquare = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * rateOfClimbMetersSeconds )/ trueAirSpeedMetersSecond ) 
            #trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + aircraftAccelerationMetersSecondSquare * deltaTimeSeconds
            
            climbCASknots = self.computeClimbCASknots( altitudeMSLfeet = altitudeMSLfeet ,
                                                       CASknots        = tas2cas ( 
                                                                            tas         = self.getCurrentTASspeedKnots() ,
                                                                            altitude    = altitudeMSLfeet ,
                                                                            temp        = 'std' ,
                                                                            speed_units = 'kt' , 
                                                                            alt_units   = 'ft' , 
                                                                            temp_units  = 'C' ) )
            
            trueAirSpeedKnots = cas2tas( cas         = climbCASknots ,
                                         altitude    = altitudeMSLfeet ,
                                         temp        = 'std' ,
                                         speed_units = 'kt' ,
                                         alt_units   = 'ft' ,
                                         temp_units  = 'C' )
            
            trueAirSpeedMetersSecond = trueAirSpeedKnots * Knots2MetersSeconds
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
            ''' verify that speeds limits have been met '''
            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()

             
            ''' distance flown '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees( rateOfClimbMetersSeconds , trueAirSpeedMetersSecond )
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            self.setTotalDistanceFlownMeters(totalDistanceFlownMeters)
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilogramsSeconds(TASknots                 =trueAirSpeedMetersSecond * MeterSecond2Knots , 
                                                                     aircraftAltitudeMSLfeet         =altitudeMSLfeet , 
                                                                     aircraftMassKilograms           =aircraftMassKilograms , 
                                                                     verticalRateFeetMinutes         =rateOfClimbFeetMinutes,
                                                                     accelerationMetersSecondsSquare =aircraftAccelerationMetersSecondSquare)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)

            ''' transition to initial climb as soon as height above ground is 1000 feet / 300 meters '''
            deltaAltitudeMeters = rateOfClimbMetersSeconds * deltaTimeSeconds
            altitudeMSLmeters = altitudeMSLmeters + deltaAltitudeMeters
            
            logger.info( self.className + " - cruise level feet = {0:.2f} feet ".format ( self.getCruiseLevelFeet() ) )
            if ( ( altitudeMSLmeters * Meter2Feet ) > ( self.getCruiseLevelFeet() - 1000.0 ) ) and  \
                     ( ( altitudeMSLmeters * Meter2Feet )  < ( self.getCruiseLevelFeet() + 1000.0 ) ):
                self.setCruiseConfiguration( elapsedTimeSeconds + deltaTimeSeconds )


        elif self.isCruise():
            '''The final approach starts from 1000 ft toward the end of the descent '''
            
            rateOfClimbFeetMinutes = 0.0
            rateOfClimbMetersSeconds = 0.0
            
            thrustNewtons = self.computeThrustNewtons( tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes)
            dragNewtons = self.computeDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet , rateOfClimbFeetMinutes )
            
            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            liftNewtons = self.computeLiftNewtons( aircraftMassKilograms = aircraftMassKilograms, altitudeMeanSeaLevelMeters =  altitudeMSLmeters, trueAirSpeedMetersSecond = trueAirSpeedMetersSecond , latitudeDegrees=latitudeDegrees)
            
            ''' compute new True Air Speed '''
            ''' dVTAS/dt = ( T - D ) / m - ( ( g0 * dh /dt ) / VTas ) '''
            aircraftAccelerationMetersSecondSquare = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * rateOfClimbMetersSeconds )/ trueAirSpeedMetersSecond ) 
            #trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + aircraftAccelerationMetersSecondSquare * deltaTimeSeconds
            
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
             
            ''' distance flown '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees( rateOfClimbMetersSeconds , trueAirSpeedMetersSecond )
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            self.setTotalDistanceFlownMeters(totalDistanceFlownMeters)
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilogramsSeconds(TASknots         =trueAirSpeedMetersSecond * MeterSecond2Knots , 
                                                                     aircraftAltitudeMSLfeet =altitudeMSLfeet , 
                                                                     aircraftMassKilograms   =aircraftMassKilograms , 
                                                                     verticalRateFeetMinutes  =rateOfClimbFeetMinutes,
                                                                     accelerationMetersSecondsSquare=aircraftAccelerationMetersSecondSquare)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)
            
            ''' altitude does not change , or increases slightly due to lighter aircraft '''

            if ( totalDistanceFlownMeters > 500.0 * 1000.0 ):
                self.setDescentConfiguration( elapsedTimeSeconds )
  
            
        elif self.isDescent():
            
            rateOfDescentMetersSeconds = self.getDescentVerticalRateMeterSeconds( altitudeMSLfeet )
            rateOfDescentFeetMinutes   = rateOfDescentMetersSeconds * MeterSeconds2FeetMinutes

            thrustNewtons = self.computeThrustNewtons( tasKnots , altitudeMSLfeet , rateOfDescentFeetMinutes)
            dragNewtons = self.computeDragNewtons ( aircraftMassKilograms , tasKnots , altitudeMSLfeet , rateOfDescentFeetMinutes )

            trueAirSpeedMetersSecond = self.getCurrentTASmetersSeconds()
            liftNewtons = self.computeLiftNewtons( aircraftMassKilograms      = aircraftMassKilograms, 
                                                   altitudeMeanSeaLevelMeters = altitudeMSLmeters, 
                                                   trueAirSpeedMetersSecond   = trueAirSpeedMetersSecond , 
                                                   latitudeDegrees            = latitudeDegrees)
            
            ''' compute new True Air Speed '''
            ''' dVTAS/dt = ( T - D ) / m - ( ( g0 * dh /dt ) / VTas ) '''
            aircraftAccelerationMetersSecondSquare = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * rateOfDescentMetersSeconds )/ trueAirSpeedMetersSecond ) 
            #trueAirSpeedMetersSecond = trueAirSpeedMetersSecond + aircraftAccelerationMetersSecondSquare * deltaTimeSeconds
            
            descentCASknots = self.computeDescentCASknots( altitudeMSLfeet = altitudeMSLfeet ,
                                                       CASknots        = tas2cas ( 
                                                                            tas         = self.getCurrentTASspeedKnots() ,
                                                                            altitude    = altitudeMSLfeet ,
                                                                            temp        = 'std' ,
                                                                            speed_units = 'kt' , 
                                                                            alt_units   = 'ft' , 
                                                                            temp_units  = 'C' ) )
            trueAirSpeedKnots = cas2tas( cas         = descentCASknots ,
                                         altitude    = altitudeMSLfeet ,
                                         temp        = 'std' ,
                                         speed_units = 'kt' ,
                                         alt_units   = 'ft' ,
                                         temp_units  = 'C' )
            
            trueAirSpeedMetersSecond = trueAirSpeedKnots * Knots2MetersSeconds
            logger.info( self.className + " - TAS = {0:.2f} meters per second - TAS = {1:.2f} knots ".format( trueAirSpeedMetersSecond , trueAirSpeedMetersSecond * MeterSecond2Knots))
            self.setCurrentTASmetersSeconds(trueAirSpeedMetersSecond)
             
            ''' flight path angle  '''
            flightPathAngleDegrees = self.computeFlightPathAngleDegrees( rateOfDescentMetersSeconds , trueAirSpeedMetersSecond )
            
            ''' distance flown '''
            deltaDistanceFlownMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            totalDistanceFlownMeters = totalDistanceFlownMeters + deltaDistanceFlownMeters
            self.setTotalDistanceFlownMeters(totalDistanceFlownMeters)
            logger.info( self.className + " - distance flown = {0:.2f} meters - distance flown = {1:.2f} Nautical miles ".format( totalDistanceFlownMeters , totalDistanceFlownMeters * Meter2NauticalMiles ))

            ''' mass loss due to fuel flow '''
            fuelFlowKilogramsSeconds = self.computeFuelFlowKilogramsSeconds(TASknots          = trueAirSpeedMetersSecond * MeterSecond2Knots , 
                                                                     aircraftAltitudeMSLfeet  = altitudeMSLfeet , 
                                                                     aircraftMassKilograms    = aircraftMassKilograms , 
                                                                     verticalRateFeetMinutes  = rateOfDescentMetersSeconds,
                                                                     accelerationMetersSecondsSquare = aircraftAccelerationMetersSecondSquare)
            aircraftMassKilograms = aircraftMassKilograms - ( fuelFlowKilogramsSeconds * deltaTimeSeconds )
            self.setAircraftMassKilograms(aircraftMassKilograms)
            
            ''' transition to initial climb as soon as height above ground is 1000 feet / 300 meters '''
            deltaAltitudeMeters = rateOfDescentMetersSeconds * deltaTimeSeconds
            altitudeMSLmeters = altitudeMSLmeters + deltaAltitudeMeters
            
            if ( descentCASknots < self.getFinalApproachCASknots() ):
                raise ValueError( " should transition to final approach - speed ")
            
            if ( altitudeMSLmeters < self.getArrivalRunwayMSLmeters()):
                raise ValueError(" should transition to final approach - altitude ")
        
        
        else:
            
            raise ValueError("not yet implemented")
    
        elapsedTimeSeconds = elapsedTimeSeconds + deltaTimeSeconds 
        self.updateAircraftStateVector( elapsedTimeSeconds       = elapsedTimeSeconds , 
                                        flightPhase              = self.getCurrentConfiguration() , 
                                        flightPathAngleDegrees   = flightPathAngleDegrees , 
                                        trueAirSpeedMeterSecond  = trueAirSpeedMetersSecond , 
                                        altitudeMSLmeters        = altitudeMSLmeters ,
                                        totalDistanceFlownMeters = totalDistanceFlownMeters , 
                                        distanceStillToFlyMeters = 0.0 , 
                                        aircraftMassKilograms    = aircraftMassKilograms , 
                                        thrustNewtons            = thrustNewtons , 
                                        dragNewtons              = dragNewtons)
        return totalDistanceFlownMeters , altitudeMSLmeters
        