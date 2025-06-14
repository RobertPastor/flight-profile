# -*- coding: UTF-8 -*-
'''
Created on 22 february 2015

@ author: PASTOR Robert

        Written By:
                Robert PASTOR 
                @Email: < robert [--DOT--] pastor0691 (--AT--) gmail [--DOT--] com >

        http://trajectoire-predict.monsite-orange.fr/ 
        Copyright 2015 Robert PASTOR 

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 3 of the License, or
        (at your option) any later version.
 
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
 
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
        
'''

import math
import logging 

logger = logging.getLogger(__name__)

from trajectory.Environment.Constants import  MaxRateOfClimbFeetPerMinutes , MaxRateOfDescentFeetPerMinutes, Knots2MetersPerSecond
from trajectory.Environment.Constants import  Meter2Feet , Feet2Meter, MeterSecond2Knots, RollingFrictionCoefficient, ConstantTaxiSpeedCasKnots
from trajectory.Environment.Constants import MaxSpeedNoiseRestrictionsKnots, MaxSpeedNoiseRestrictionMeanSeaLevelFeet

from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.BadaAircraftPerformance.BadaEngineFile import Engine
from trajectory.BadaAircraftPerformance.BadaAircraftMassFile import AircraftMass
from trajectory.BadaAircraftPerformance.BadaGroundMovementFile import GroundMovement
from trajectory.BadaAircraftPerformance.BadaTransitionAltitudeFile import TransitionAltitude

from trajectory.BadaAircraftPerformance.BadaFlightEnvelopeFile import FlightEnvelope

from trajectory.Environment.Atmosphere import Atmosphere
from trajectory.Environment.Earth import Earth
from trajectory.aerocalc.airspeed import tas2cas, tas2mach, default_temp_units
from trajectory.Environment.Utils import logElapsedRealTime
from trajectory.Environment.Constants import Meter2NauticalMiles

class EnergyShareFactor(object):
    className = ""

    SpeedConfiguration = ['constant-CAS-below-tropopause', 
                          'constant-CAS-above-tropopause' ,
                          'constant-Mach-below-tropopause',
                          'constant-Mach-above-tropopause']
    currentSpeedConfiguration = ''
    
    def __init__(self):
        self.className = self.__class__.__name__
        self.currentSpeedConfiguration = self.SpeedConfiguration[0]
        
    def setConstantCASbelowTropopause(self):
        self.currentSpeedConfiguration = self.SpeedConfiguration[0]
        
    def setConstantMachbelowTropopause(self):
        self.currentSpeedConfiguration = self.SpeedConfiguration[2]
        
    def computeEnergyShareFactor(self, mach):
        ''' R is the real gas constant for air, R = 287.05287 [m2/Ks2] '''
        ''' k is the adiabatic index of air, k = 1.4 '''
        ''' b is the ISA temperature gradient with altitude below the tropopause, T,< b = -0.0065 [°K/m] '''
        
        if self.currentSpeedConfiguration == self.SpeedConfiguration[0]:
            ''' constant CAS below tropopause '''
            
            ESF1 = 1.0 + ((1.4 * 287.05287 *(-0.0065)* mach * mach) /(2.0 * 9.80665)) 
            ESF2 = math.pow((1.0 + ((1.4-1.0)/2.0)* mach * mach), (-1.0/(1.4-1.0)))
            ESF3 = math.pow((1.0 + ((1.4-1.0)/2.0)* mach * mach) , (1.4/(1.4-1.0))) - 1.0
            ESF = ESF1 + ESF2 * ESF3
            ESF = math.pow(ESF, -1.0)

        elif self.currentSpeedConfiguration == self.SpeedConfiguration[1]:
            ''' 'constant-CAS-above-tropopause' '''
            ESF1 = 1 + math.pow( ((1.4-1.0)/2.0) * mach * mach ,  (-1.0/(1.4-1.0)))
            ESF2 = math.pow ( 1 + ((1.4-1.0)/2.0) * mach * mach , (1.4 /(1.4-1.0)))
            ESF = 1 + ESF1 * (ESF2 - 1.0)
            ESF = math.pow(ESF, -1.0)
            
        elif self.currentSpeedConfiguration == self.SpeedConfiguration[2]:
            ''' Constant Mach number below tropopause '''
            ESF = 1 + (1.4*287.05287*(-0.0065)*mach*mach)/(2*9.80665)
            ESF = math.pow(ESF, -1.0)
            
        elif self.currentSpeedConfiguration == self.SpeedConfiguration[3]:
            ''' Constant Mach number in stratosphere (i.e. above tropopause) '''
            ESF = 1.0
        
        ESF = 0.85
        return ESF
    
            
class AircraftConfiguration(FlightEnvelope):
    
    '''
    Take-off         - take-off     lift/drag configuration      - max climb thrust settings
    initial-climb    - initial climb lift-drag configuration     - max climb thrust settings
    climb            - clean a/c configuration                   - max climb thrust settings
    
    cruise         - clean a/c configuration         - cruise thrust settings
    descent        - clean a/c configuration         - descent-high thrust settings
    descent        - clean a/c configuration         - descent-low thrust settings
    
    approach       - approach a/c configuration      - approach thrust settings
    landing        - landing a/c configuration       - landing thrust settings
    '''
    
    className = ""
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
    engine = None
    
    rollingFrictionCoefficient = RollingFrictionCoefficient        # rolling friction coefficient (mur)
    flightPathAngleDegrees = 0.0              # angle between Velocity and local horizon
    ''' vertical phase from airlines procedure '''
    verticalPhase = None
    transitionAltitude = None # this is an object class
    
    ROCDsmoothingStarted = False
    ROCDbeforeSmoothingtarted = 0.0
    
    def __init__(self, 
                 badaPerformanceFilePath ,
                 ICAOcode,
                 atmosphere,
                 earth ):
        
        self.className = self.__class__.__name__ 
        
        self.badaPerformanceFilePath = badaPerformanceFilePath
        
        ''' 2nd-November-2023 - moving to json performance files '''
        aircraftPerformance = AircraftJsonPerformance(ICAOcode, badaPerformanceFilePath)
        assert ( aircraftPerformance.read() == True )
        
        ''' initialize base class '''
        FlightEnvelope.__init__(self, aircraftPerformance, ICAOcode , atmosphere, earth)

        assert isinstance(atmosphere, Atmosphere) and not(atmosphere is None)
        self.atmosphere = atmosphere
        
        assert isinstance(earth, Earth) and not(earth is None)
        self.earth = earth

        self.aircraftMass = AircraftMass(aircraftPerformance)
        self.WakeTurbulenceCategory = aircraftPerformance.getWakeTurbulenceCategory()

        self.nbEngines = aircraftPerformance.getNumberOfEngines()
        self.groundMovement = GroundMovement(aircraftPerformance)
        self.engine = Engine(aircraftPerformance)

        logger.info ( self.className  + ' ===================================================' )
        self.aircraftCurrentConfiguration = 'departure-ground-run'
        self.flightPathAngleDegrees = 0.0
        logger.info ( self.className + ' default configuration= ' + self.aircraftCurrentConfiguration )
        logger.info ( self.className + ' ===================================================' )

        self.TakeOffMaxAltitudeThresholdReached = False
        self.InitialClimbMaxAltitudeThresholdReached = False
        
        self.cruiseLevelReached = False
        self.cruiseSpeedReached = False
        
        self.transitionAltitude = TransitionAltitude(self.engine)
        VCasMeterSecond = self.getMaxOpSpeedCasKnots() * Knots2MetersPerSecond
        Mach = self.getTargetCruiseMach()
        
        self.transitionAltitudeFeet = self.transitionAltitude.computeTransitionAltitudeFeet(VCasMeterSecond, Mach)
        logger.debug ( self.className + ' transition altitude= {0:.2f} feet'.format(self.transitionAltitudeFeet) )
        
        self.energyShareFactor = EnergyShareFactor()
        
    def __str__(self):
        return self.aircraftCurrentConfiguration

    def setAircraftMassKilograms(self, aircraftMassKilograms):
        self.aircraftMass.setAircraftMassKilograms(aircraftMassKilograms)
         
    def getAircraftMassKilograms(self):
        return self.aircraftMass.getCurrentMassKilograms()
    
    def getAircraftCurrentMassKilograms(self):
        return self.aircraftMass.getCurrentMassKilograms()

    def getAircraftInitialMassKilograms(self):
        return self.aircraftMass.getInitialMassKilograms() 
        
    def getMinimumMassKilograms(self):
        return self.aircraftMass.getMinimumMassKilograms()
    
    def getMaximumMassKilograms(self):
        return self.aircraftMass.getMaximumMassKilograms()
    
    def computeAircraftMassKilograms(self, flightPathRangeMeters):
        return self.aircraftMass.referenceMassKilograms

    def showConfigurationChange(self, newConfiguration, elapsedTimeSeconds):
        assert isinstance(newConfiguration, str)
        altitudeMeanSeaLevelMeters = self.getCurrentAltitudeSeaLevelMeters()
        currentDistanceFlownMeters = self.getCurrentDistanceFlownMeters()
        tas = self.getCurrentTrueAirSpeedMetersSecond()
        #cas = self.atmosphere.tas2cas(tas = tas, altitude = altitudeMeanSeaLevelMeters,alt_units='m', speed_units='m/s',)
        cas = tas2cas(tas = tas, altitude = altitudeMeanSeaLevelMeters, temp='std', speed_units='m/s', alt_units='m')
        #mach = self.atmosphere.tas2mach(tas = tas, altitude = altitudeMeanSeaLevelMeters, alt_units='m', speed_units='m/s')
        mach = tas2mach(tas = tas , temp='std', altitude = altitudeMeanSeaLevelMeters, temp_units= 'C',speed_units='m/s')
        mach = tas2mach(tas = tas , temp='std', altitude = altitudeMeanSeaLevelMeters, temp_units = default_temp_units, alt_units = 'm' , speed_units='m/s')

        logger.info ( self.className + ' ====================================' )
        logger.info ( self.className + ' entering {0} configuration - flown {1:.2f} meters - distance flown {2:.2f} Nm'.format(newConfiguration, currentDistanceFlownMeters, currentDistanceFlownMeters*Meter2NauticalMiles) )
        logger.info ( self.className + ' alt= {0:.2f} meters alt= {1:.2f} feet'.format(altitudeMeanSeaLevelMeters, (altitudeMeanSeaLevelMeters*Meter2Feet)) ) 
        logger.info ( self.className + ' TAS= {0:.2f} m/s - TAS= {1:.2f} knots - CAS= {2:.2f} m/s - CAS= {3:.2f} knots - Mach= {4:.2f}'.format(tas, (tas*MeterSecond2Knots), cas, (cas*MeterSecond2Knots), mach) )
        logElapsedRealTime( self.className , elapsedTimeSeconds )

    def setDepartureGroundRunConfiguration(self, elapsedTimeSeconds):
        ''' configuration no lifting devices used - rolling friction '''
        newConfiguration = 'departure-ground-run'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration
            
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

    def setClimbConfiguration(self, elapsedTimeSeconds):
        newConfiguration = 'climb'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration
    
    def setCruiseConfiguration(self, elapsedTimeSeconds):
        newConfiguration = 'cruise'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration
 
    def setDescentConfiguration(self, elapsedTimeSeconds):
        newConfiguration = 'descent'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration

    def setApproachConfiguration(self, elapsedTimeSeconds):
        ''' approach starts 4-5 nautics when the ILS 3-degrees descent slope is captured '''
        ''' aircraft speed is reduced using flaps until Approach stall speed => move to landing and extract landing-gear '''
        newConfiguration = 'approach'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration
    
    def setLandingConfiguration(self, elapsedTimeSeconds):
        ''' landing configuration - landing-gear down - starts as soon as speed < Approach stall speed 
        and altitude above airport field > xxx feet '''
        newConfiguration = 'landing'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration
        
    def setArrivalGroundRunConfiguration(self, elapsedTimeSeconds):
        newConfiguration = 'arrival-ground-run'
        if self.aircraftCurrentConfiguration != newConfiguration:
            self.showConfigurationChange(newConfiguration, elapsedTimeSeconds)
            self.aircraftCurrentConfiguration = newConfiguration        
            
    def isDepartureGroundRun(self):
        return (self.aircraftCurrentConfiguration=='departure-ground-run')
    
    def isArrivalGroundRun(self):
        return (self.aircraftCurrentConfiguration=='arrival-ground-run')
    
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
    
    def isLanding(self):
        return (self.aircraftCurrentConfiguration=='landing')
    
    def isApproach(self):
        return (self.aircraftCurrentConfiguration=='approach')

            
    def computeDragNewtons(self, 
                           aircraftMassKilograms, 
                           altitudeMeters,
                           TrueAirSpeedMetersSecond,
                           latitudeDegrees):
        '''
        In the landing configuration (as defined in Section 3.5) a different flap setting is used, 
        and formula 3.6-4 should be applied:

        The value of CD0, DLDG represents drag increase due to the landing gear. The values of CD0, LD in
        the OPF files were all determined for the landing flap setting mentioned in the OPF file.
        The drag force (in Newtons) is then determined from the drag coefficient in the standard manner:
    
        '''
        
        #logger.info 'to be fixed... aircraft mass ... depends upon flight path range in Kilometers + reserve'
        liftCoeff = self.computeLiftCoeff(  aircraftMassKilograms, 
                                            altitudeMeters, 
                                            TrueAirSpeedMetersSecond,
                                            latitudeDegrees)
        #logger.info liftCoeff
        if self.isDepartureGroundRun() or self.isTakeOff():
            CD0 , CD2 = self.getDragCoeff('TO')
            
        elif self.isInitialClimb():
            CD0 , CD2 = self.getDragCoeff('IC')

        elif self.isClimb() or self.isCruise() or self.isDescent():
            ''' if cruise or descent then same drag configuration '''
            ''' first phase of descent occurs at constant Mach Number '''
            CD0 , CD2 = self.getDragCoeff('CR')
            
        elif self.isApproach():
            CD0 , CD2 = self.getDragCoeff('AP')

        elif self.isLanding() or self.isArrivalGroundRun():
            CD0 , CD2 = self.getDragCoeff('LD')

        else:
            raise ValueError (self.className + 'configuration not in take-off, climb, cruise, approach or landing' )           

        if self.isLanding():
            '''
            In the landing configuration (as defined in Section 3.5) a different flap setting is used, and formula
            3.6-4 should be applied:

            The value of CD0, DLDG represents drag increase due to the landing gear.
            '''
            dragCoeff = CD0 + self.LandingGearDragCoeff + ( CD2 * liftCoeff * liftCoeff )
            
        else:       
            dragCoeff = CD0 + ( CD2 * liftCoeff * liftCoeff )
            
        # compute drag
        dragNewtons = dragCoeff * self.atmosphere.getAirDensityKilogramsPerCubicMeters(altitudeMeters)
        dragNewtons = dragNewtons * TrueAirSpeedMetersSecond * TrueAirSpeedMetersSecond
        dragNewtons = dragNewtons * self.getWingAreaSurfaceSquareMeters()
        dragNewtons = 0.5 * dragNewtons
        return dragNewtons
    
    
    def computeLiftNewtons(self,
                           aircraftMassKilograms,
                           altitudeMeanSeaLevelMeters, 
                           TrueAirSpeedMetersSecond, 
                           latitudeDegrees):
        '''  Qinf = 0.5 * rho * (aircraftSpeed ** 2) '''
        '''  Lift = Qinf * aircraft.WingPlanformAreaSquareMeters * CL '''
        ''' @todo '''
        #@TODO logger.info 'to be fixed... aircraft mass ... depends upon flight path range in Kilometers + reserve'
        liftCoeff = self.computeLiftCoeff(  aircraftMassKilograms, 
                                                       altitudeMeanSeaLevelMeters, 
                                                       TrueAirSpeedMetersSecond,
                                                       latitudeDegrees)
        liftNewtons = 0.5 * self.atmosphere.getAirDensityKilogramsPerCubicMeters(altitudeMeanSeaLevelMeters)
        liftNewtons = liftNewtons * TrueAirSpeedMetersSecond * TrueAirSpeedMetersSecond
        liftNewtons = liftNewtons * self.WingAreaSurfaceSquareMeters * liftCoeff
        return liftNewtons
    
    def setReducedClimbPowerCoeff(self, reducedClimbPowerCoef):
        self.reducedClimbPowerCoef = reducedClimbPowerCoef
        
    def getReducedClimbPowerCoeff(self):
        return self.reducedClimbPowerCoef
    
    def computeBaseThrustNewtons(self, geopotentialPressureAltitudeFeet):
        ''' following computation is true only for a jet aircraft '''
        thrustNewtons = (1 - (geopotentialPressureAltitudeFeet / self.engine.getMaxClimbThrustCoeff(1) ))
        thrustNewtons += (self.engine.getMaxClimbThrustCoeff(2) * geopotentialPressureAltitudeFeet * geopotentialPressureAltitudeFeet)
        thrustNewtons = self.engine.getMaxClimbThrustCoeff(0) * thrustNewtons
        return thrustNewtons
        
    def computeClimbPowerReductionCoeff(self):
        ''' 23rd July - reduced climb power see BADA manual 3.10 '''
        powerReducedCoeff = ( self.aircraftMass.getMaximumMassKilograms() - self.aircraftMass.getCurrentMassKilograms()  )
        powerReducedCoeff = powerReducedCoeff / ( self.aircraftMass.getMaximumMassKilograms() - self.aircraftMass.getMinimumMassKilograms() )
        ''' the coefficient is provided in % by the user '''
        if self.getReducedClimbPowerCoeff() >= 0.0:
            # in percentage example 15%
            powerReducedCoeff = 1 - ( ( self.getReducedClimbPowerCoeff() / 100.0 ) * powerReducedCoeff )
        else:
            # in value example 0,15
            powerReducedCoeff = 1 - ( self.getReducedClimbPowerCoeff() * powerReducedCoeff )
        if powerReducedCoeff==1:
            pass
            #print(powerReducedCoeff)
        return powerReducedCoeff
    
    def computeThrustNewtons(self, geopotentialPressureAltitudeFeet ):

        ''' sanity check '''
        assert isinstance(geopotentialPressureAltitudeFeet, float)
                
        thrustNewtons = 0.0
        if self.engine.isJet():
            if self.isDepartureGroundRun() or self.isTakeOff() or self.isInitialClimb() :
                
                ''' following computation is true only for a jet aircraft '''
                thrustNewtons = self.computeBaseThrustNewtons(geopotentialPressureAltitudeFeet)
                #print ( "departure / takeoff / initial Climb thrust = {} newtons".format( thrustNewtons ) )
                
            
            elif self.isClimb() or self.isCruise():
                ''' @TODO reduce thrust in proportion to altitude difference '''
            
                '''
                In cruise at cruise level - The normal cruise thrust is by definition set equal to drag (THR = D).
                However, the maximum amount of thrust available in cruise situation is limited. 
                The maximum cruise thrust is calculated as a ratio of the maximum climb thrust given by expression 3.7-4, 
                that is: 
                Thrust Cruise MAX  = Coeff Tcr * Max climb Thurst 
                The coefficient CTcr is currently uniformly set for all aircraft (see Global Aircraft Parameters section 5.5).
                '''
            
                ''' following computation is true only for a jet aircraft '''
                thrustNewtons = self.computeBaseThrustNewtons(geopotentialPressureAltitudeFeet)
                                
                ''' correction due to altitude difference '''
                #altitudeDifferenceMeters = self.getTargetCruiseFlightLevelMeters() - ( geopotentialPressureAltitudeFeet * feet2Meters)
                #percent = altitudeDifferenceMeters / self.getTargetCruiseFlightLevelMeters()
                #reducedThrustNewtons = ( thrustNewtons / 100. ) * percent
                #print ("initial thrust {0:0.1f} = reduced thrust = {1:1f}".format (thrustNewtons , reducedThrustNewtons))
                #thrustNewtons = thrustNewtons - reducedThrustNewtons
                
                ''' apply cruise factor '''
                if self.isCruiseSpeedReached():
                    thrustNewtons = 0.95 * thrustNewtons
                    
                #print ( "climb / cruise thrust = {} newtons".format( thrustNewtons ) )

                
            elif self.isDescent():
                '''
                first descent phase is performed at constant Mach until transition altitude 
                second descent phase is performed at constant CAS until approach configuration '''
                thrustNewtons = self.computeBaseThrustNewtons(geopotentialPressureAltitudeFeet)

                ''' apply high descent factor '''
                ''' transition altitude for calculation of descent thrust '''
                index = 2
                HpDescentHighToLow = self.engine.getDescentThrustCoeff(index)
                if geopotentialPressureAltitudeFeet > HpDescentHighToLow:
                    ''' high altitude descent thrust coefficient '''
                    index = 1
                    thrustNewtons = self.engine.getDescentThrustCoeff(index) * thrustNewtons
                else:
                    ''' low altitude descent thrust coefficient '''
                    index = 0 
                    thrustNewtons = self.engine.getDescentThrustCoeff(index) * thrustNewtons
            
            elif self.isApproach():
                '''
                Note that the CTdes, app and CTdes, landing coefficients are determined in order to obtain a 3° descent
                gradient during approach and landing
                '''
                thrustNewtons = self.computeBaseThrustNewtons(geopotentialPressureAltitudeFeet)
                ''' apply approach factor '''
                thrustNewtons = self.engine.getDescentThrustCoeff(3) * thrustNewtons
                
                
            elif self.isLanding():
                '''
                In the landing configuration (as defined in Section 3.5) a different flap setting is used, and formula
                3.6-4 should be applied:

                The value of CD0, DLDG represents drag increase due to the landing gear. The values of CD0, LD in
                the OPF files were all determined for the landing flap setting mentioned in the OPF file.
                '''
                thrustNewtons = self.computeBaseThrustNewtons(geopotentialPressureAltitudeFeet)

                ''' apply landing factor '''
                thrustNewtons = self.engine.getDescentThrustCoeff(4) * thrustNewtons

            elif self.isArrivalGroundRun():
                # @TODO use idle thrust here
                thrustNewtons = self.computeBaseThrustNewtons(geopotentialPressureAltitudeFeet)
                thrustNewtons = 0.1 * thrustNewtons

            else:
                raise ValueError ('not yet implemented {0}'.format(self.getAircraftConfiguration()))
            
        elif self.engine.isTurboProp():
            raise ValueError ('not yet implemented')
        
        elif self.engine.isPiston():
            raise ValueError ('not yet implemented')
        else:
            raise ValueError ('not yet implemented')
        return thrustNewtons
    
    def computeLiftCoeff(self,  
                         aircraftMassKilograms, 
                         altitudeMeters, 
                         TrueAirSpeedMetersSecond, 
                         latitudeDegrees):
        '''
        lift coeff = ( 2 * aircraft-mass * gravity ) / ( rho * TAS * TAS * WingSurface ) 
        '''
        if self.isDepartureGroundRun():
            liftCoeff = 0.1
        else:
            gravityCenterMetersPerSquaredSeconds = self.earth.gravity(self.earth.getRadiusMeters(), math.radians(latitudeDegrees))[0]
            airDensity = self.atmosphere.getAirDensityKilogramsPerCubicMeters(altitudeMeters)
            liftCoeff = 2 * aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds
            if TrueAirSpeedMetersSecond > 0.0:
                wingAreaSurfaceSquareMeters = self.getWingAreaSurfaceSquareMeters()
                liftCoeff = liftCoeff / ( airDensity * TrueAirSpeedMetersSecond * TrueAirSpeedMetersSecond * wingAreaSurfaceSquareMeters)
            else:
                liftCoeff = 0.0
        return liftCoeff
        
    def computeApproachStallSpeedCasKnots(self):
        ''' leave Approach as soon as Landing stall speed reached '''
        VstallKcas = self.getVstallKcas('LD')

        ''' theoretical air speed corrected by mass differences '''        
        aircraftReferenceMassKilograms = self.aircraftMass.getReferenceMassKilograms()
        aircraftMassKilograms = self.aircraftMass.getCurrentMassKilograms()
        Vstall = VstallKcas * math.sqrt ( aircraftMassKilograms / aircraftReferenceMassKilograms )
        return Vstall
        
    def computeLandingStallSpeedCasKnots(self):
        ''' leave Descent as soon as Approach stall speed reached '''
        VstallKcas = self.getVstallKcas('AP')

        ''' theoretical air speed corrected by mass differences '''        
        aircraftReferenceMassKilograms = self.aircraftMass.getReferenceMassKilograms()
        aircraftMassKilograms = self.aircraftMass.getCurrentMassKilograms()
        Vstall = VstallKcas * math.sqrt ( aircraftMassKilograms / aircraftReferenceMassKilograms )
        return Vstall

    def computeStallSpeedCasKnots(self):
        '''
        Aircraft operating speeds vary with the aircraft mass. 
        This variation is calculated according to the formula below:
        V = V ref * square root ( mass / mass ref )

        In this formula, the aircraft reference speed Vref is given for the reference mass mref. 
        The speed at another mass, m, is then calculated as V.
        An example of an aircraft speed, which can be calculated via this formula is the stall speed, Vstall
        
        stall speed depends upon aircraft Mass and air density at the airport according to its altitude
        
        Weight:
        ======
        A change in weight will not change the angle of attack with which the wing will stall (CLmax is fixed for a given wing configuration), 
        but it changes the speed where the stall will occur. 
        We know that for any level flight (not climbing) the amount of lift must be equal to the weight of the aircraft, 
        thus if all up weight is lower then the amount of lift required is less too. 
        To calculate the new stall speed: Vs new = Vs old weight x √(new weight / old weight).
        
        Altitude:
        ========
        Given the lift formula: L = 1/2 ρ V2 x S x CL, the amount of lift generated by a given wing 
        depends on Angle Of Attack (CL) and airspeed, altitude is set by 1/2 ρ. 
        So when the aircraft climbs the factor '1/2 ρ' decreases and as CL remains the same, 
        true airspeed must increase to obtain the same indicated airspeed (IAS). 
        And as stall speed is directly related to AOA it also remains the same, 
        but the TAS where the stall occurs increases with altitude because of the lower air density (1/2 ρ).
        
        '''
        VstallKcas = 0.0
        if self.isDepartureGroundRun() or self.isArrivalGroundRun():
            ''' leave ground run as soon as Take Off stall speed is reached '''
            VstallKcas = self.getVstallKcas('TO')
            
        elif self.isTakeOff():
            ''' leave take off as soon as Initial Climb stall speed is reached '''
            VstallKcas = self.getVstallKcas('IC')
            
        elif self.isClimb():
            ''' leave climb as soon as Cruise clean stall stall speed is reached '''
            VstallKcas = self.getVstallKcas('CR')

        elif self.isCruise():
            raise ValueError ('should not be called !!!')

        elif self.isDescent():
            ''' leave Descent as soon as Approach stall speed reached '''
            VstallKcas = self.getVstallKcas('AP')

        elif self.isApproach():
            ''' leave approach for landing as soon as Landing stall speed is reached '''
            VstallKcas = self.getVstallKcas('LD')
            
        elif self.isLanding():
            ''' leave landing for ground run as soon as Landing stall speed is reached '''
            VstallKcas = self.getVstallKcas('LD')

        else:
            raise ValueError (self.className + 'configuration: - not in take-off, climb, cruise, approach or landing')       
        
        aircraftReferenceMassKilograms = self.aircraftMass.getReferenceMassKilograms()
        aircraftMassKilograms = self.aircraftMass.getCurrentMassKilograms()
        Vstall = VstallKcas * math.sqrt ( aircraftMassKilograms / aircraftReferenceMassKilograms )
        return Vstall
        
    def updateAircraftConfiguration(self, newConfiguration):
        if newConfiguration in self.aircraftConfigurationList:
            
            self.aircraftCurrentConfiguration = newConfiguration
            logger.info ( self.className + ' ============= configuration changes ================' )
            logger.info ( self.className + ' new configuration is= ' + self.aircraftCurrentConfiguration )
            logger.info ( self.className + ' ============= configuration changes ================' )

        else:
            raise ValueError (self.className + ' unknown aircraft configuration')

    def getAircraftConfiguration(self):
        return self.aircraftCurrentConfiguration

    def setCurrentAltitudeSeaLevelMeters(self, 
                                         elapsedTimeSeconds, 
                                         altitudeMeanSeaLevelMeters,
                                         lastAltitudeMeanSeaLevelMeters,
                                         targetCruiseAltitudeMslMeters):
        '''
        CONFIGURATION ALTITUDE THRESHOLD
        For 4 configurations, altitude thresholds have been specified in BADA: take-off (TO), initial climb
        (IC), approach (AP) and landing (LD).
        
        Note that the selection of the take-off and initial climb configurations is defined only with the altitude. 
        
        The selection of the approach and landing configurations is done through the use of air speed and altitude (see Section 3.5), while the
        altitudes at which the configuration change takes place should not be higher than the ones given
        below. The altitude values are expressed in terms of geo-potential pressure altitude.
        
        Name: Description: Value [ ft ]:
        Hmax, TO Maximum altitude threshold for take-off 400 feet
        Hmax, IC Maximum altitude threshold for initial climb 2,000 feet
        Hmax, AP Maximum altitude threshold for approach 8,000 feet
        Hmax, LD Maximum altitude threshold for landing 3,000 feet
        '''
        if (lastAltitudeMeanSeaLevelMeters * Meter2Feet <= 400.0) and (altitudeMeanSeaLevelMeters * Meter2Feet > 400.0):
                if self.TakeOffMaxAltitudeThresholdReached == False:
                    logger.debug ( self.className + ' Take-Off max altitude threshold reached' )
                    self.TakeOffMaxAltitudeThresholdReached = True
                
        if (lastAltitudeMeanSeaLevelMeters * Meter2Feet <= 2000) and (altitudeMeanSeaLevelMeters * Meter2Feet > 400.0):
                if self.InitialClimbMaxAltitudeThresholdReached == False:
                    logger.debug ( self.className + ' Initial-Climb max altitude threshold reached' )
                    self.InitialClimbMaxAltitudeThresholdReached = True

        if (lastAltitudeMeanSeaLevelMeters * Meter2Feet >= 8000.0) and (altitudeMeanSeaLevelMeters * Meter2Feet < 8000.0):
            
                logger.debug ( self.className + ' Approach max altitude threshold reached' )

        if (lastAltitudeMeanSeaLevelMeters * Meter2Feet >= 3000.0) and (altitudeMeanSeaLevelMeters * Meter2Feet < 3000.0):
                logger.debug ( self.className + ' Landing max altitude threshold reached' )

        ''' need to check an altitude change versus its history '''
#         if (altitudeMeanSeaLevelMeters > (targetCruiseAltitudeMslMeters-100.0)):
#             ''' if target cruise altitude reached '''
#             self.setCruiseConfiguration(elapsedTimeSeconds)

    def computeDescentDecelerationMeterPerSquareSeconds(self,
                                                        trueAirSpeedMetersSecond,
                                                         currentPosition,
                                                         distanceStillToFlyMeters,
                                                         distanceToLastFixMeters):
        ''' deceleration from current speed to approach speed '''
        approachStallSpeedCasKnots = self.computeApproachStallSpeedCasKnots()
        approachStallSpeedCasMeterPerSeconds = approachStallSpeedCasKnots * Knots2MetersPerSecond
        
        approachStallSpeedTasMeterPerSeconds = self.atmosphere.cas2tas(cas = approachStallSpeedCasMeterPerSeconds,
                                                                       altitudeMeters = currentPosition.getAltitudeMeanSeaLevelMeters(), 
                                                                       speed_units = 'm/s', altitude_units = 'm')
        ''' bug : if flight is passing near by approach point but turning ahead then next distance is false because too direct '''
        distanceToApproachFixMeters = currentPosition.getDistanceMetersTo(self.approachWayPoint)
        ''' patch 17th May 2015 '''
        distanceToApproachFixMeters = distanceToLastFixMeters
        timeToFlySeconds = (distanceToApproachFixMeters) / (trueAirSpeedMetersSecond)
        ''' need to substract a threshold here 10.0 m/S to be sure to avoid tangenting '''
        descentDecelerationMeterPerSquareSeconds = -0.01
        if timeToFlySeconds > 0.0:
            descentDecelerationMeterPerSquareSeconds = (approachStallSpeedTasMeterPerSeconds - 20.0 - trueAirSpeedMetersSecond) / timeToFlySeconds
        return  descentDecelerationMeterPerSquareSeconds


    def computeApproachDecelerationMeterPerSquareSeconds(self, 
                                                         trueAirSpeedMetersSecond,
                                                         currentPosition,
                                                         distanceStillToFlyMeters,
                                                         distanceToLastFixMeters):
        ''' deceleration from current speed (assume it is approach) to landing speed '''
        landingStallSpeedCasKnots = self.computeLandingStallSpeedCasKnots()
        landingStallSpeedCasMeterPerSeconds = landingStallSpeedCasKnots * Knots2MetersPerSecond
        
        landingStallSpeedTasMeterPerSeconds = self.atmosphere.cas2tas(cas = landingStallSpeedCasMeterPerSeconds,
                                                                      altitudeMeters = currentPosition.getAltitudeMeanSeaLevelMeters() , 
                                                                      speed_units = 'm/s', 
                                                                      altitude_units = 'm')
        ''' distance from current to touch-down '''
        distanceToTouchDownMeters = currentPosition.getDistanceMetersTo(self.arrivalRunWayTouchDownWayPoint)
        distanceToTouchDownMeters = distanceToLastFixMeters
        ''' patch 17th May 2015 '''
        timeToFlySeconds = (distanceToTouchDownMeters) / (trueAirSpeedMetersSecond)
        ''' need to substract a threshold here 10.0 m/S to be sure to avoid tangenting '''
        approachDecelerationMeterPerSquareSeconds = (landingStallSpeedTasMeterPerSeconds - 10.0 - trueAirSpeedMetersSecond) / timeToFlySeconds
        if (approachDecelerationMeterPerSquareSeconds > 0.0):
            approachDecelerationMeterPerSquareSeconds = -0.1
        return  approachDecelerationMeterPerSquareSeconds
    
    
    def computeLandingDecelerationMeterPerSquareSeconds(self, 
                                                         trueAirSpeedMetersSecond,
                                                         currentPosition,
                                                         distanceStillToFlyMeters,
                                                         distanceToLastFixMeters):
        ''' deceleration from current speed (assume it is approach) to landing speed '''
        landingStallSpeedCasKnots = self.computeLandingStallSpeedCasKnots()
        landingStallSpeedCasMeterPerSeconds = landingStallSpeedCasKnots * Knots2MetersPerSecond
        
        landingStallSpeedTasMeterPerSeconds = self.atmosphere.cas2tas(cas = landingStallSpeedCasMeterPerSeconds,
                                                                      altitudeMeters = currentPosition.getAltitudeMeanSeaLevelMeters() , 
                                                                      speed_units = 'm/s', 
                                                                      altitude_units = 'm')
        ''' distance from current to touch-down '''
        distanceToTouchDownMeters = currentPosition.getDistanceMetersTo(self.arrivalRunWayTouchDownWayPoint)
        ''' patch 17th May 2015 '''
        timeToFlySeconds = (distanceToTouchDownMeters) / (trueAirSpeedMetersSecond)
        ''' need to substract a threshold here 10.0 m/S to be sure to avoid tangenting '''
        approachDecelerationMeterPerSquareSeconds = (landingStallSpeedTasMeterPerSeconds - 10.0 - trueAirSpeedMetersSecond) / timeToFlySeconds
        if (approachDecelerationMeterPerSquareSeconds > 0.0):
            approachDecelerationMeterPerSquareSeconds = -0.1
        return  approachDecelerationMeterPerSquareSeconds

    def isCruiseSpeedReached(self):
        return self.cruiseSpeedReached
    
    ''' ROCD is expressed in meters per seconds '''
    def computeROCD(self, deltaTimeSeconds, thrustNewtons, dragNewtons, trueAirSpeedMetersSecond, aircraftMassKilograms, gravityCenterMetersPerSquaredSeconds, ESF):
        if self.isInitialClimb() or self.isClimb():
            ''' 23rd July 2023 - see BADA 3.10 manual - reduced Climb Power Coefficient '''
            coeff = self.computeClimbPowerReductionCoeff()
            ROCD  = ( ( (thrustNewtons - dragNewtons) * trueAirSpeedMetersSecond * self.computeClimbPowerReductionCoeff()) / ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds ) ) * ESF 
        else:
            ROCD  = ( ( (thrustNewtons - dragNewtons) * trueAirSpeedMetersSecond) / ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds ) ) * ESF 

        if ( ROCD > 0.0 ):
            ''' compute feet per minutes '''
            if  ( ( ( ( ROCD / deltaTimeSeconds ) * 60.0 ) * Meter2Feet ) > MaxRateOfClimbFeetPerMinutes ):
                pass
                #ROCD = ( MaxRateOfClimbFeetPerMinutes * Feet2Meter ) / 60.0
                
        if ( ROCD < 0.0 ):
            if ( ( ( ( ROCD / deltaTimeSeconds) * 60.0 ) * Meter2Feet ) < MaxRateOfDescentFeetPerMinutes ):
                ROCD = ( MaxRateOfDescentFeetPerMinutes * Feet2Meter ) / 60.0
                
        return ROCD
    
    def applySpeedRestrictionsDuringClimb(self, trueAirSpeedMetersSecond, altitudeMeanSeaLevelMeters):
        
        ''' during climb apply speed restriction below 10.000 feet -> speed not higher than 250 knots '''
        if self.isInitialClimb() or self.isClimb():
            altitudeMeanSeaLevelFeet = altitudeMeanSeaLevelMeters * Meter2Feet
            trueAirSpeedKnots = trueAirSpeedMetersSecond * MeterSecond2Knots
            
            if (trueAirSpeedKnots >= MaxSpeedNoiseRestrictionsKnots) and altitudeMeanSeaLevelFeet <= MaxSpeedNoiseRestrictionMeanSeaLevelFeet:
                return MaxSpeedNoiseRestrictionsKnots * Knots2MetersPerSecond
            else:
                return trueAirSpeedMetersSecond
        else:
            return trueAirSpeedMetersSecond
        
    def applySpeedRestrictionsDuringDescent(self, trueAirSpeedMetersSecond, deltaAltitudeMeters, altitudeMeanSeaLevelMeters):
        if self.isDescent():
            altitudeMeanSeaLevelFeet = altitudeMeanSeaLevelMeters * Meter2Feet
            ''' wait until speed is lower than 250 knots before descending below 10.000 feet '''
            trueAirSpeedKnots = trueAirSpeedMetersSecond * MeterSecond2Knots
            if (trueAirSpeedKnots >= MaxSpeedNoiseRestrictionsKnots) and altitudeMeanSeaLevelFeet <= MaxSpeedNoiseRestrictionMeanSeaLevelFeet:
                ''' do not descend more, wait until speed is reduced '''
                return 0.0
            else:
                return deltaAltitudeMeters
        else:
            return deltaAltitudeMeters
            

    def fly(self, 
            elapsedTimeSeconds, 
            deltaTimeSeconds, 
            aircraftMassKilograms, 
            distanceStillToFlyMeters,
            currentPosition ,
            distanceToLastFixMeters ):
        
        endOfSimulation = False
        '''
        main aircraft vertical altitude and speed change management
        '''
        latitudeDegrees = currentPosition.getLatitudeDegrees()
        altitudeMeanSeaLevelMeters = self.getCurrentAltitudeSeaLevelMeters()
        trueAirSpeedMetersSecond = self.getCurrentTrueAirSpeedMetersSecond()
        currentDistanceFlownMeters = self.getCurrentDistanceFlownMeters()
        flightPathAngleDegrees = self.getFlightPathAngleDegrees()
        
        thrustNewtons = self.computeThrustNewtons(altitudeMeanSeaLevelMeters * Meter2Feet)
        dragNewtons = self.computeDragNewtons(aircraftMassKilograms,
                                              altitudeMeanSeaLevelMeters,
                                              trueAirSpeedMetersSecond,
                                              latitudeDegrees )
        ''' 26th December 2022 '''
        liftNewtons = self.computeLiftNewtons(aircraftMassKilograms,
                           altitudeMeanSeaLevelMeters, 
                           trueAirSpeedMetersSecond, 
                           latitudeDegrees)
        
        gravityCenterMetersPerSquaredSeconds = self.earth.gravity(self.earth.getRadiusMeters()+altitudeMeanSeaLevelMeters, math.radians(latitudeDegrees))[0]
        
        if self.isDepartureGroundRun():
            #liftNewtons = 0.0
            ''' 
            Rate of climb is null => all energy is used to increase True Air Speed
            leave ground-run as soon as Take-Off stall speed is reached
            ''' 
            #casKnots = self.atmosphere.tas2cas(tas = trueAirSpeedMetersSecond ,  altitude = altitudeMeanSeaLevelMeters,  temp='std', speed_units = 'm/s', alt_units = 'm') * MeterSecond2Knots
            casKnots = tas2cas( tas = trueAirSpeedMetersSecond, altitude = altitudeMeanSeaLevelMeters,temp = 'std' , speed_units = 'm/s', alt_units = 'm')* MeterSecond2Knots
            ''' apply rolling friction '''
            aircraftAcceleration = thrustNewtons - dragNewtons - self.rollingFrictionCoefficient * ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds - liftNewtons)
            aircraftAcceleration = aircraftAcceleration / aircraftMassKilograms
            trueAirSpeedMetersSecond += aircraftAcceleration * deltaTimeSeconds
            
            VStallSpeedCASKnots = self.computeStallSpeedCasKnots()
            ''' move to Take-Off as soon as 1.2 * Stall CAS reached '''
            if ( ( tas2cas(tas = trueAirSpeedMetersSecond , altitude = altitudeMeanSeaLevelMeters,temp='std', speed_units = 'm/s', alt_units = 'm') * MeterSecond2Knots ) >= (1.2 * VStallSpeedCASKnots)):
                ''' departure ground run stall speed reached '''
                cas = tas2cas(tas = trueAirSpeedMetersSecond ,  altitude = altitudeMeanSeaLevelMeters,
                        temp='std',   speed_units = 'm/s',    alt_units = 'm')
                logger.debug ( self.className + ' TAS= {0:.2f} knots - CAS= {1:.2f} knots > (1.2 * V CAS stall)= {2:.2f} knots'.format(trueAirSpeedMetersSecond*MeterSecond2Knots ,cas*MeterSecond2Knots, (1.2*VStallSpeedCASKnots)) )
                ''' update aircraft configuration '''
                self.setTakeOffConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
            
            ''' distance flown '''
            deltaDistanceMeters = trueAirSpeedMetersSecond * deltaTimeSeconds
            deltaAltitudeMeters = 0.0

        elif self.isTakeOff():
            ''' move to Climb as soon as Initial Climb stall speed reached '''
            ''' climb at constant CAS => increasing TAS '''

            mach = self.atmosphere.tas2mach(tas = trueAirSpeedMetersSecond ,
                       altitude = altitudeMeanSeaLevelMeters,
                     speed_units = 'm/s', alt_units = 'm')
            ESF = self.energyShareFactor.computeEnergyShareFactor(mach)
            
            ''' compute Altitude change '''
            #ROCD  = ( ((thrustNewtons - dragNewtons) * trueAirSpeedMetersSecond) / ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds ) ) * ESF 
            ROCD = self.computeROCD(deltaTimeSeconds, thrustNewtons, dragNewtons, trueAirSpeedMetersSecond, aircraftMassKilograms, gravityCenterMetersPerSquaredSeconds, ESF)

            deltaAltitudeMeters = ROCD * deltaTimeSeconds
            altitudeMeanSeaLevelMeters += deltaAltitudeMeters
            
            ''' compute new True Air Speed '''
            aircraftAcceleration = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * ROCD )/ trueAirSpeedMetersSecond ) 
            trueAirSpeedMetersSecond += aircraftAcceleration * deltaTimeSeconds

            ''' is it time to move from TakeOff to Climb configuration '''
            initialClimbStallSpeedCasKnots = self.computeStallSpeedCasKnots()  
            #casKnots = self.atmosphere.tas2cas(tas = trueAirSpeedMetersSecond ,  altitude = altitudeMeanSeaLevelMeters ,  temp='std',    speed_units = 'm/s',  alt_units = 'm') * MeterSecond2Knots 
            casKnots = tas2cas( tas = trueAirSpeedMetersSecond, altitude = altitudeMeanSeaLevelMeters , temp = 'std' , speed_units = 'm/s', alt_units = 'm')* MeterSecond2Knots

            if ((casKnots >= initialClimbStallSpeedCasKnots) 
                and (altitudeMeanSeaLevelMeters >= (self.departureAirportAltitudeMSLmeters + 50.0))):
                logger.debug ( self.className + ' CAS= {0:.2f} knots >= Initial Climb Stall Speed= {1:.2f} knots'.format(casKnots, initialClimbStallSpeedCasKnots) )
                self.setInitialClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
                
            ''' distance flown '''
            deltaDistanceMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            
        elif self.isInitialClimb():
            ''' climb at constant CAS '''
            mach = self.atmosphere.tas2mach(tas = trueAirSpeedMetersSecond,
                                  altitude = altitudeMeanSeaLevelMeters,
                                  alt_units = 'm',
                                  speed_units = 'm/s')
            
            ESF = self.energyShareFactor.computeEnergyShareFactor(mach)
            ''' compute Altitude change '''
            #ROCD  = ( ((thrustNewtons - dragNewtons) * trueAirSpeedMetersSecond) / ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds ) ) * ESF 
            ROCD = self.computeROCD(deltaTimeSeconds, thrustNewtons, dragNewtons, trueAirSpeedMetersSecond, aircraftMassKilograms, gravityCenterMetersPerSquaredSeconds, ESF)

            deltaAltitudeMeters = ROCD * deltaTimeSeconds
            altitudeMeanSeaLevelMeters += deltaAltitudeMeters
            
            ''' compute new True Air Speed '''
            aircraftAcceleration = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * ROCD) / trueAirSpeedMetersSecond) 
            trueAirSpeedMetersSecond += aircraftAcceleration * deltaTimeSeconds
            ''' 14th November 2023 - apply speed restriction below 10.000 feets '''
            trueAirSpeedMetersSecond = self.applySpeedRestrictionsDuringClimb(trueAirSpeedMetersSecond , altitudeMeanSeaLevelMeters)
            
            ''' distance flown '''
            deltaDistanceMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees))* deltaTimeSeconds
           
            casKnots = tas2cas(tas      = trueAirSpeedMetersSecond , altitude = altitudeMeanSeaLevelMeters ,
                                               temp ='std', speed_units = 'm/s', alt_units   = 'm') * MeterSecond2Knots 
                                                  
            ''' move from initial climb to climb as soon as speed over 250 knots and altitude above 10.000 feet '''
            # 24th July 2022 - condition upon casKnots never reached or depending upon aircraft performances
            #if ((casKnots >= 250.0) or ((altitudeMeanSeaLevelMeters * Meter2Feet) >= 10000.0)):
            #    self.setClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
           
            ''' check if target cruise altitude is reached -> 10.000 feet '''
            if ( ( altitudeMeanSeaLevelMeters * Meter2Feet ) >= 10000.0 ):
                ''' target cruise altitude reached '''
                self.setClimbConfiguration(elapsedTimeSeconds + deltaTimeSeconds)

        elif self.isClimb():     
            ''' climb at constant Mach '''
            mach = self.atmosphere.tas2mach(tas = trueAirSpeedMetersSecond,
                                  altitude = altitudeMeanSeaLevelMeters,
                                  alt_units = 'm',
                                  speed_units = 'm/s')
            
            if (mach >= (self.getTargetCruiseMach() - 0.01)) and (self.cruiseSpeedReached == False) :
                self.cruiseSpeedReached = True
                self.energyShareFactor.setConstantMachbelowTropopause()

            ESF = self.energyShareFactor.computeEnergyShareFactor(mach)
            
            ''' compute Altitude change '''
            #ROCD  = ( ((thrustNewtons - dragNewtons) * trueAirSpeedMetersSecond) / ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds ) ) * ESF 
            ROCD = self.computeROCD(deltaTimeSeconds, thrustNewtons, dragNewtons, trueAirSpeedMetersSecond, aircraftMassKilograms, gravityCenterMetersPerSquaredSeconds, ESF)
            
            ''' last xxx feet before reaching target cruise level '''
            LevelMetersThreshold = 500.0
            ROCDsmoothing = 0.05
            ''' below target cruise level but also near threshold level '''
            if ( altitudeMeanSeaLevelMeters < self.getTargetCruiseFlightLevelMeters() ) and ( altitudeMeanSeaLevelMeters > ( self.getTargetCruiseFlightLevelMeters() - LevelMetersThreshold ) ) :
                ''' compute feet difference in one minute '''
                deltaMetersToCruiseLevel  =  ( self.getTargetCruiseFlightLevelMeters() - altitudeMeanSeaLevelMeters ) 
                ''' ROCD is expressed in meters per seconds '''
                #if ( ROCD / deltaMetersToCruiseLevel ) < ( 1 * 60 ):
                
                #if ( ( deltaMetersToCruiseLevel * Meter2Feet ) > 100. )   :
                pass
                if self.ROCDsmoothingStarted == False:
                    self.ROCDsmoothingStarted = True
                    self.ROCDbeforeSmoothingtarted = ROCD
                    #print ( "Rate Of Climb smoothing started - altitude MSL meters = {0} - initial ROCD = {1} ".format(altitudeMeanSeaLevelMeters, ROCD) )
                else:
                    self.ROCDbeforeSmoothingtarted = self.ROCDbeforeSmoothingtarted - ROCDsmoothing
                    #ROCD = self.ROCDbeforeSmoothingtarted
                    #if ( ROCD < ROCDsmoothing ):
                    #    ROCD =  ROCDsmoothing
                    #print ( "Rate Of Climb smoothing - altitude MSL meters = {0} - ROCD smoothed = {1}".format(altitudeMeanSeaLevelMeters, ROCD) )

            else:
                if self.ROCDsmoothingStarted:
                    self.ROCDbeforeSmoothingtarted = self.ROCDbeforeSmoothingtarted - ROCDsmoothing
                    #ROCD = self.ROCDbeforeSmoothingtarted
                    #if ( ROCD < ROCDsmoothing ):
                    #    ROCD =  ROCDsmoothing
                    #print ( "Aircraft is near = {0} - to Cruise Level = {1} - ROCD before = {2}".format( altitudeMeanSeaLevelMeters , self.getTargetCruiseFlightLevelMeters() , ROCD))
                    #ROCD = ROCD - ( ( ( LevelMetersThreshold - deltaMetersToCruiseLevel ) / LevelMetersThreshold ) * ROCD )
                    #print ( "Aircraft is near = {0} - to Cruise Level = {1} - ROCD after = {2}".format( altitudeMeanSeaLevelMeters , self.getTargetCruiseFlightLevelMeters() , ROCD))

            deltaAltitudeMeters = ROCD * deltaTimeSeconds
            altitudeMeanSeaLevelMeters += deltaAltitudeMeters
            
            ''' compute new True Air Speed '''
            aircraftAcceleration = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * ROCD) / trueAirSpeedMetersSecond) 
            trueAirSpeedMetersSecond += aircraftAcceleration * deltaTimeSeconds
           
            if (((ROCD * 3600 ) / Meter2Feet ) < 10.0 ):
                ''' ROCD lower than 100.0 feet per minute => cruise '''
                self.setCruiseConfiguration(elapsedTimeSeconds + deltaTimeSeconds)

            ''' check if target cruise altitude is reached '''
            if ( altitudeMeanSeaLevelMeters > (self.getTargetCruiseFlightLevelMeters() - 100.0)):
                ''' target cruise altitude reached '''
                if self.cruiseLevelReached == False:
                    logger.debug ( self.className + ' cruise level reached= {0:.2f} meters = {1:.2f} feet'.format(altitudeMeanSeaLevelMeters, altitudeMeanSeaLevelMeters * Meter2Feet) )
                    self.cruiseLevelReached = True
                self.setCruiseConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
                
            ''' distance flown '''
            deltaDistanceMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees))* deltaTimeSeconds
            
            ''' compute distance to top of descent '''
            if (self.computeDescentDistanceMeters(trueAirSpeedMetersSecond) >= distanceStillToFlyMeters):
                self.setDescentConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
                ''' this is used to modify the integration step => 10 sec in Cruise and 1s in Descent '''
                self.cruiseSpeedReached = False
        
        elif self.isCruise():
            ''' cruise altitude is reached '''
            ''' all energy is used to reach or maintain Mach '''
            mach = tas2mach(tas = trueAirSpeedMetersSecond, temp = 'std' , altitude = altitudeMeanSeaLevelMeters,  alt_units = 'm',   speed_units = 'm/s')
            
            if mach > ( self.getTargetCruiseMach() - 0.001):
                self.cruiseSpeedReached = True
                self.energyShareFactor.setConstantMachbelowTropopause()
                
            ESF = self.energyShareFactor.computeEnergyShareFactor(mach)
            
            ''' compute Altitude change '''
            if ( altitudeMeanSeaLevelMeters < (self.getTargetCruiseFlightLevelMeters() + 100.0) ) \
                and ( altitudeMeanSeaLevelMeters > (self.getTargetCruiseFlightLevelMeters() - 100.0) ):
                ''' cruise '''
                ROCD = 0.0
                deltaAltitudeMeters = 0.0
            else:
                ''' continue climbing '''
                #ROCD  = ( ((thrustNewtons - dragNewtons) * trueAirSpeedMetersSecond) / ( aircraftMassKilograms * gravityCenterMetersPerSquaredSeconds ) ) * ESF 
                ROCD = self.computeROCD(deltaTimeSeconds, thrustNewtons, dragNewtons, trueAirSpeedMetersSecond, aircraftMassKilograms, gravityCenterMetersPerSquaredSeconds, ESF)

                deltaAltitudeMeters = ROCD * deltaTimeSeconds
                altitudeMeanSeaLevelMeters += deltaAltitudeMeters
                
            ''' compute new True Air Speed '''
            if (mach < (self.getTargetCruiseMach() - (self.getTargetCruiseMach() * 0.001))):
                ''' if target mach not reached => accelerate '''
                aircraftAcceleration = ((thrustNewtons - dragNewtons) / aircraftMassKilograms) - ((gravityCenterMetersPerSquaredSeconds * ROCD) / trueAirSpeedMetersSecond) 
                trueAirSpeedMetersSecond += aircraftAcceleration * deltaTimeSeconds
            else:
                ''' correct thrust in order to reduce fuel flow '''
                thrustNewtons = dragNewtons
                    
            ''' delta distance flown '''
            deltaDistanceMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees)) * deltaTimeSeconds
            ''' compute distance to top of descent '''
            if (self.computeDescentDistanceMeters(trueAirSpeedMetersSecond) > distanceStillToFlyMeters):
                ''' enter descent configuration '''
                self.setDescentConfiguration(elapsedTimeSeconds + deltaTimeSeconds)
                self.cruiseSpeedReached = False
            
        elif self.isDescent():
            
            ''' descent at constant Mach '''
            ''' as aircraft configuration is clean , this phase transforms potential energy in kinetic energy to maintain a Mach '''
            ''' energy is negative as thrust lower to drag '''
            ESF = 0.8
            ''' compute new True Air Speed '''
            aircraftAcceleration = self.computeDescentDecelerationMeterPerSquareSeconds(trueAirSpeedMetersSecond = trueAirSpeedMetersSecond, 
                                                                                        currentPosition = currentPosition,
                                                                                        distanceStillToFlyMeters = distanceStillToFlyMeters,
                                                                                        distanceToLastFixMeters = distanceToLastFixMeters)
            trueAirSpeedMetersSecond += aircraftAcceleration * deltaTimeSeconds
            deltaDistanceMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees))* deltaTimeSeconds
            #logger.debug 'acceleration= {0:.2f} - speed= {1:.2f} - distance= {2:.2f}'.format(aircraftAcceleration, trueAirSpeedMetersSecond, deltaDistanceMeters)

            ''' check altitude versus approach altitude '''
            if altitudeMeanSeaLevelMeters <= self.approachWayPoint.getAltitudeMeanSeaLevelMeters():
                ROCD = 0.0
                deltaAltitudeMeters = 0.0
            else:
                ''' compute Altitude change '''
                distanceToTargetApproachFixMeters = currentPosition.getDistanceMetersTo(self.approachWayPoint)
                ''' patch Robert : 17th May 2015 '''
                distanceToTargetApproachFixMeters = distanceToLastFixMeters
                deltaAltitudeToTargetApproachFixMeters = self.approachWayPoint.getAltitudeMeanSeaLevelMeters() - 20.0 - altitudeMeanSeaLevelMeters
                approachGlideSlopeDegrees = -3.0
                if distanceToTargetApproachFixMeters > 0.0:
                    approachGlideSlopeDegrees = math.degrees(math.atan(deltaAltitudeToTargetApproachFixMeters / distanceToTargetApproachFixMeters))
                else:
                    endOfSimulation = True
                deltaAltitudeMeters = math.tan(math.radians(approachGlideSlopeDegrees)) * deltaDistanceMeters           
                ''' 15th November 2023 - apply speed restrictions - wait at 10.000 feet until speed is lower to 250 knots '''
                deltaAltitudeMeters = self.applySpeedRestrictionsDuringDescent(trueAirSpeedMetersSecond, deltaAltitudeMeters, altitudeMeanSeaLevelMeters)
                ''' compute ROCD Rate Of Climb Descent '''
                ROCD = deltaAltitudeMeters / deltaTimeSeconds
                ''' compute new altitude '''
                altitudeMeanSeaLevelMeters += deltaAltitudeMeters
                            
            ''' compute stall speed to change configuration to approach '''
            VStallSpeedCASKnots = self.computeStallSpeedCasKnots()
            ''' move to Approach as soon as Approach Stall CAS speed reached '''
            if  (( tas2cas(tas = trueAirSpeedMetersSecond ,  altitude = altitudeMeanSeaLevelMeters, 
                           temp = 'std' , speed_units = 'm/s', alt_units = 'm') * MeterSecond2Knots ) <= (VStallSpeedCASKnots)):
                ''' as soon as speed decrease to approach configuration => change aircraft configuration '''
                self.setApproachConfiguration(elapsedTimeSeconds + deltaTimeSeconds )
                
        elif self.isApproach():
            ''' configuration is changed to reduce air speed '''
            ''' ensure that descent slope is 3 degrees '''
            ''' from Ground Speed get the delta distance => here use Ground Speed '''
                
            ''' compute new True Air Speed '''
            aircraftDeceleration = self.computeApproachDecelerationMeterPerSquareSeconds(trueAirSpeedMetersSecond = trueAirSpeedMetersSecond, 
                                                                                         currentPosition          = currentPosition,
                                                                                         distanceStillToFlyMeters = distanceStillToFlyMeters,
                                                                                         distanceToLastFixMeters  = distanceToLastFixMeters)
            trueAirSpeedMetersSecond += aircraftDeceleration * deltaTimeSeconds
            deltaDistanceMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees))* deltaTimeSeconds
            
            distanceToTargetApproachFixMeters = currentPosition.getDistanceMetersTo(self.approachWayPoint)
            ''' patch 17th May 2015 '''
            distanceToTargetApproachFixMeters = distanceToLastFixMeters
            deltaAltitudeToTargetApproachFixMeters = self.approachWayPoint.getAltitudeMeanSeaLevelMeters() - 10.0 - altitudeMeanSeaLevelMeters

            ''' check altitude versus approach altitude '''
            if altitudeMeanSeaLevelMeters <= self.approachWayPoint.getAltitudeMeanSeaLevelMeters():
                ''' altitude remains unchanged '''
                deltaAltitudeMeters = 0.0
                ROCD = 0.0
            else:
                approachGlideSlopeDegrees = math.degrees(math.atan(deltaAltitudeToTargetApproachFixMeters / distanceToTargetApproachFixMeters))
                deltaAltitudeMeters = math.tan(math.radians(approachGlideSlopeDegrees)) * deltaDistanceMeters           
                ''' compute ROCD '''
                ROCD = deltaAltitudeMeters / deltaTimeSeconds
                ''' compute Altitude change '''
                altitudeMeanSeaLevelMeters += deltaAltitudeMeters
                        
            ''' compute stall speed to change configuration to landing '''
            VStallSpeedCASKnots = self.computeStallSpeedCasKnots()
            ''' move to Landing as soon as Stall CAS reached '''
            if ( ( tas2cas(tas = trueAirSpeedMetersSecond , altitude = altitudeMeanSeaLevelMeters, temp = 'std',
                     speed_units = 'm/s', alt_units = 'm') * MeterSecond2Knots ) <= (VStallSpeedCASKnots)):
                ''' as soon as speed decrease to approach configuration => change aircraft configuration '''
                logger.debug ( self.className +' distance to approach fix= {0:.2f} meters - delta altitude to approach fix= {1:.2f} meters'.format(distanceToTargetApproachFixMeters, deltaAltitudeToTargetApproachFixMeters) )
                self.setLandingConfiguration(elapsedTimeSeconds + deltaTimeSeconds )

        elif self.isLanding():
            ''' landing gear is extracted '''
            ''' compute new True Air Speed '''
            aircraftDeceleration = self.computeLandingDecelerationMeterPerSquareSeconds(trueAirSpeedMetersSecond = trueAirSpeedMetersSecond, 
                                                                                         currentPosition = currentPosition,
                                                                                         distanceStillToFlyMeters = distanceStillToFlyMeters,
                                                                                         distanceToLastFixMeters = distanceToLastFixMeters)
            trueAirSpeedMetersSecond += aircraftDeceleration * deltaTimeSeconds
            deltaDistanceMeters = trueAirSpeedMetersSecond * math.cos(math.radians(flightPathAngleDegrees))* deltaTimeSeconds

            distanceToRunWayTouchDownMeters = currentPosition.getDistanceMetersTo(self.arrivalRunWayTouchDownWayPoint)
            deltaAltitudeToRunWayTouchDownMeters = self.arrivalRunWayTouchDownWayPoint.getAltitudeMeanSeaLevelMeters() - 10.0 - altitudeMeanSeaLevelMeters
            approachGlideSlopeDegrees = math.degrees(math.atan(deltaAltitudeToRunWayTouchDownMeters / distanceToRunWayTouchDownMeters))
            deltaAltitudeMeters = math.tan(math.radians(approachGlideSlopeDegrees)) * deltaDistanceMeters
            
            ROCD = deltaAltitudeMeters / deltaTimeSeconds
            ''' compute Altitude change '''
            altitudeMeanSeaLevelMeters += deltaAltitudeMeters
                
            arrivalRunwayTouchDownAltitudeMSLmeters = self.getArrivalRunwayTouchDownWayPoint().getAltitudeMeanSeaLevelMeters()
            if (altitudeMeanSeaLevelMeters <= arrivalRunwayTouchDownAltitudeMSLmeters):
                ''' if altitude is lower than airport elevation then correct it - cap size '''
                altitudeMeanSeaLevelMeters = arrivalRunwayTouchDownAltitudeMSLmeters
                logger.debug ( self.className +' distance to runway touch-down= {0:.2f} meters - delta altitude to runway touch-down= {1:.2f} meters'.format(distanceToRunWayTouchDownMeters, deltaAltitudeToRunWayTouchDownMeters) )

                self.setArrivalGroundRunConfiguration(elapsedTimeSeconds + deltaTimeSeconds)

        elif self.isArrivalGroundRun():
            ''' altitude stays unchanged '''
            deltaAltitudeMeters = 0.0
            ''' all energy is used to decrease the speed until taxi speed '''
            #logger.info self.className + ' speed lower to landing speed => time to touch-down !!!'
            '''
            deceleration rate between 3 and 6 knots per second => 4 knots considered
            '''
            trueAirSpeedMetersSecond = trueAirSpeedMetersSecond - (( 3.0 * Knots2MetersPerSecond )* deltaTimeSeconds )
            ''' distance flown '''
            deltaDistanceMeters = trueAirSpeedMetersSecond * deltaTimeSeconds
            if ( ( tas2cas(tas = trueAirSpeedMetersSecond , altitude = altitudeMeanSeaLevelMeters, temp = 'std' ,
                     speed_units = 'm/s', alt_units = 'm') * MeterSecond2Knots ) <= (ConstantTaxiSpeedCasKnots)):
                logger.info ( self.className +' - taxi speed reached => end of simulation' )
                endOfSimulation = True
            
        else:
            logger.info("Error - phase is not yet implemented")
            raise ValueError('not yet implemented')
            
        ''' aircraft mass decreases according to fuel flow '''
        fuelFlowKilograms = self.engine.computeNominalFuelFlowKilograms(trueAirSpeedMetersSecond, 
                                                                        thrustNewtons, 
                                                                        deltaTimeSeconds)
        
        try:
            aircraftMassKilograms = self.aircraftMass.updateAircraftMassKilograms(fuelFlowKilograms)
        except Exception as ex:
            logger.info ( self.className + '-' + str(ex) + ' - no more fuel !!!!' )
            endOfSimulation = True
            raise ValueError ( self.className + ' - no more fuel !!!! ' )

        ''' store updated speed '''
        currentDistanceFlownMeters += deltaDistanceMeters
        flightPathAngleDegrees = 0.0
        if deltaDistanceMeters > 0.0:
            flightPathAngleDegrees = math.degrees(math.atan(deltaAltitudeMeters / deltaDistanceMeters))
        
        ''' 13th September 2023 - log the flight phase or the last characteristic point '''
        characteristicPoint = self.aircraftCurrentConfiguration
        
        #if not endOfSimulation:
        endOfSimulation = self.updateAircraftStateVector(elapsedTimeSeconds + deltaTimeSeconds, 
                                                    characteristicPoint,
                                                    trueAirSpeedMetersSecond      , 
                                                    altitudeMeanSeaLevelMeters    ,
                                                    currentDistanceFlownMeters    ,
                                                    distanceStillToFlyMeters      ,
                                                    aircraftMassKilograms         ,
                                                    flightPathAngleDegrees        ,
                                                    thrustNewtons                 ,
                                                    dragNewtons                   ,
                                                    liftNewtons                   ,
                                                    currentPosition               ,
                                                    endOfSimulation)

        ''' return delta distance and altitude changes '''
        return endOfSimulation, deltaDistanceMeters, altitudeMeanSeaLevelMeters

    def computeDescentDistanceMeters(self, trueAirSpeedMetersSeconds):
        '''
        Descent Information: Airbus A320
        
        To calculate Top Of Descent point 
        =================================
        (the point at which you need to begin your descent to reach the desired altitude at the desired time):
        
        Use 6.5 miles per minute (at Mach .65 in descent) as the basis. If you are cruising
        at 33,000 ft. and wish to descend to 5,000 ft. at the next waypoint, at a descent rate of 1,800 ft./min., you need to
        figure the time to descend 28,000 ft. (33,000 - 5,000). 
        Divide 28,000 ft. by 1,800 ft./min. and you will get 15.56 minutes. 
        
        At 6.5 miles per minute, you need to begin your descent at 101 miles from the next waypoint (15.56
        minutes multiplied by 6.5 miles per minute).
        
        This is a "No Wind" calculation. 
        If you have a tail-wind, the miles per minute will be greater; 
        if you have a head-wind, the miles per minute will be lower.
        
        Descend with throttles at idle at initial descent.
        =================================================
        Set auto throttle to hold descent airspeed of Mach .65 to 16,000 ft. and 250 KIAS below 16,000 ft.
        Set descent rate to 1,800 ft./min
        '''

#         logger.info "aircraft current altitude Above Sea Level= ", altitudeAboveSeaLevelMeters, " meters - altitude in feet= ", altitudeAboveSeaLevelMeters * Meter2Feet ," feet"
#         logger.info "aircraft current speed= ", speedMetersPerSecond, " Meters / Second"
#         logger.info "aircraft descent rate = ", self.DescentRateMetersPerSecond, " Meters / Second"
#         logger.info "destination airport field elevation Sea Level Meters= ", arrivalAirport.fieldElevationAboveSeaLevelMeters, " meters"

        altitudeMeanSeaLevelMeters = self.getCurrentAltitudeSeaLevelMeters()
        if self.getTargetApproachWayPoint() is None:
            ''' flight is out bound => no approach way point '''
            ''' simulated approach fix altitude => cruise level '''
            approachFixAltitudeMSLmeters = self.getTargetCruiseFlightLevelMeters()
        else:
            approachFixAltitudeMSLmeters = self.getTargetApproachWayPoint().getAltitudeMeanSeaLevelMeters()
            
        deltaAltitudeMeters = altitudeMeanSeaLevelMeters - approachFixAltitudeMSLmeters
        durationDescentSeconds = ((deltaAltitudeMeters * Meter2Feet) / self.computeDescentRateFeetPerMinute()) * 60.0
        descentDistanceMeters = (0.5 * trueAirSpeedMetersSeconds) * durationDescentSeconds
        
        if self.getArrivalRunwayTouchDownWayPoint() is None:
            ''' flight is out bound => no arrival touch down defined '''
            arrivalAirportFieldElevationMeters = self.getTargetCruiseFlightLevelMeters()
        else:
            arrivalAirportFieldElevationMeters = self.getArrivalRunwayTouchDownWayPoint().getAltitudeMeanSeaLevelMeters()
        ''' delta height to descent '''
        deltaAltitudeMeters = altitudeMeanSeaLevelMeters - arrivalAirportFieldElevationMeters
        durationDescentSeconds = ((deltaAltitudeMeters * Meter2Feet) / self.computeDescentRateFeetPerMinute()) * 60.0
        #logger.info "descent duration Seconds= ", durationDescentSeconds, " duration in minutes= ", durationDescentSeconds/60.
        descentDistanceMeters = trueAirSpeedMetersSeconds * durationDescentSeconds
        return descentDistanceMeters

    def computeDescentRateFeetPerMinute(self):
        ''' use descent thrust '''
        
        altitudeMeanSeaLevelMeters = self.getCurrentAltitudeSeaLevelMeters()
        #descentThrust = self.computeDescentThrustNewtons(altitudeMeanSeaLevelMeters*Meter2Feet)
        '''
        Descent thrust is calculated as a ratio of the maximum climb thrust given by expression 3.7-4, with
        different correction factors used for high and low altitudes, and approach and landing
        configurations (see Section 3.5), that is:
        if Hp > Hp,des:
            des,high Tdes,high max climb T = C ´ T (3.7-9)
        if Hp > Hp,des:
            Cruise configuration: des,low Tdes,low max climb T = C ´ T (3.7-10)
        '''
        # 1800 feet per minute
        DescentRateFeetPerMinutes = 2200.0
        #DescentRateFeetPerMinutes = 3000.0
        return DescentRateFeetPerMinutes

    def createStateVectorOutputFile(self, abortedFlight, aircraftICAOcode, AdepICAOcode, AdesICAOcode):
        assert ( type(abortedFlight) == bool )
        filePrefix = ""
        if abortedFlight:
            filePrefix = "Aborted"
        filePrefix += "-" + aircraftICAOcode + "-" + AdepICAOcode + "-" + AdesICAOcode
        self.StateVector.createStateVectorHistoryFile(filePrefix)

    def createStateVectorOutputSheet(self, workbook, abortedFlight, aircraftICAOcode, AdepICAOcode, AdesICAOcode):
        assert ( type(abortedFlight) == bool )
        filePrefix = ""
        if abortedFlight:
            filePrefix = "Aborted"
        filePrefix += "-" + aircraftICAOcode + "-" + AdepICAOcode + "-" + AdesICAOcode
        self.StateVector.createStateVectorHistorySheet(workbook)
