'''
Created on 12 nov. 2024

@author: robert
'''
import logging 
logger = logging.getLogger(__name__)

from openap import prop, WRAP

from trajectory.Environment.Constants import MeterSecond2Knots , Meter2Feet, Meter2NauticalMiles
from trajectory.OutputFiles.XlsxOutputFile import XlsxOutput
from trajectory.aerocalc.airspeed import tas2cas


class OpenapAircraftStateVector(object):
    aircraftICAOcode = ""
    aircraftStateHistory = []

    def __init__(self , aircraftICAOcode ):
        self.className = self.__class__.__name__
        self.aircraftICAOcode = aircraftICAOcode
        
        self.aircraft = prop.aircraft( ac=str(aircraftICAOcode).lower(), use_synonym=True )
        ''' ensure that there is only one unique access to the WRAP database '''
        self.wrap = WRAP(str(aircraftICAOcode).upper(), use_synonym=True)

        self.aircraftStateHistory = []
    
    def initStateVector(self,
                        elapsedTimeSeconds, 
                        flightPhase,
                        flightPathAngleDegrees=0.0,
                        trueAirSpeedMetersSecond=0.0, 
                        altitudeMeanSeaLevelMeters=0.0,
                        aircraftMassKilograms=0.0,
                        totalDistanceFlownMeters = 0.0,
                        distanceStillToFlyMeters = 0.0):
 
        #logger.info( self.className + " - initialize state vector")
        ''' 9th September 2023 - add flight phase point to state vector '''
        self.updateAircraftStateVector(elapsedTimeSeconds, 
                                    flightPhase,
                                    flightPathAngleDegrees    ,
                                    trueAirSpeedMetersSecond  , 
                                    altitudeMeanSeaLevelMeters,
                                    totalDistanceFlownMeters  ,
                                    distanceStillToFlyMeters  ,
                                    aircraftMassKilograms     ,
                                    thrustNewtons = 0.0       ,
                                    dragNewtons   = 0.0       ,
                                    liftNewtons   = 0.0       ,
                                    currentPosition = "None"  ,
                                    endOfSimulation = False)
        #logger.info( self.className + " - state vector initialized")

        
    ''' 15th September 2024 - currentPosition used to retrieve the nearest weather station '''
    def updateAircraftStateVector(self, 
                                    elapsedTimeSeconds, 
                                    flightPhase,
                                    flightPathAngleDegrees,
                                    trueAirSpeedMeterSecond,
                                    altitudeMSLmeters          = 0.0,
                                    totalDistanceFlownMeters   = 0.0,
                                    distanceStillToFlyMeters   = 0.0,
                                    aircraftMassKilograms      = 0.0,
                                    thrustNewtons              = 0.0,
                                    dragNewtons                = 0.0,
                                    liftNewtons                = 0.0,
                                    currentPosition            = "None",
                                    endOfSimulation            = False):
        
        ''' need to store both TAS and altitude => compute CAS '''
        aircraftStateDict = {}
        ''' 9th September 2023 - add flight phase point '''
        aircraftStateDict[elapsedTimeSeconds] = [flightPhase,
                                                 altitudeMSLmeters, 
                                                 trueAirSpeedMeterSecond, 
                                                 totalDistanceFlownMeters,
                                                 distanceStillToFlyMeters,
                                                 aircraftMassKilograms,
                                                 flightPathAngleDegrees,
                                                 thrustNewtons,
                                                 dragNewtons,
                                                 liftNewtons ,
                                                 endOfSimulation]
        self.aircraftStateHistory.append(aircraftStateDict)


    def createStateVectorHistoryFile(self, filePrefix):
        if isinstance(filePrefix, str) and len(filePrefix)>0:
            fileName =  filePrefix + '-Altitude-MSL-Speed-History'
        else:
            fileName = self.aircraftICAOcode + '-Altitude-MSL-Speed-History'

        xlsxOutput = XlsxOutput(fileName)
        ''' 9th September 2023 - add characteristic point '''
        xlsxOutput.writeHeaders(['elapsed-time-seconds', 
                                 
                                 'characteristic-point',
                                
                                 'altitude-MSL-meters',
                                 'altitude-MSL-feet',

                                 'true-air-speed-meters-second',
                                 'true-air-speed-knots',
                                 
                                 'calibrated-air-speed-knots',
                                 'mach',
                                 'rate-of-climb-descent-feet-minute',
                                 
                                 'distance-flown-Nm',
                                 'distance-to-fly-Nm',
                                 
                                 'aircraft-mass-kilograms'      ,
                                 'flight-path-angle-degrees'    ,
                                 
                                 'thrust-newtons'               ,
                                 'drag-newtons'                 ,
                                 'lift-newtons'                 ,
                                 
                                 'load-factor-g'                ,
                                 'nearest-Weather-Station'      ,
                                 'temperature-degrees-celsius'  ,
                                 'wind-direction-true-north-degrees',
                                 'wind-speed-knots',
                                 'end of simulation'
                                 ])

        previousAltitudeMeanSeaLevelFeet = 0.0
        previousElapsedTimeSeconds = 0.0
        cumulatedDistanceFlownNautics = 0.0
        
        for stateVectorHistory in self.aircraftStateHistory:
            for elapsedTimeSeconds, valueList in stateVectorHistory.items():

                ''' 9th September 2023 - characteristic point '''
                characteristic_point = valueList[0]

                ''' altitude '''
                altitudeMeanSeaLevelMeters = valueList[1]
                altitudeMeanSeaLevelFeet = altitudeMeanSeaLevelMeters * Meter2Feet

                ''' speeds '''
                trueAirSpeedMetersSecond = valueList[2]
                trueAirSpeedKnots = trueAirSpeedMetersSecond * MeterSecond2Knots 

                ''' total distance flown in Meters '''
                totalDistanceFlownMeters = valueList[3]
                cumulatedDistanceFlownNautics = totalDistanceFlownMeters * Meter2NauticalMiles
                
                distanceStillToFlyMeters = valueList[4]
                distanceStillToFlyNautics = distanceStillToFlyMeters * Meter2NauticalMiles
                
                ''' aircraft Mass History in Kilograms '''
                aircraftMassKilograms = valueList[5]
                flightPathAngleDegrees = valueList[6]

                thrustNewtons = valueList[7]
                dragNewtons = valueList[8]
                liftNewtons = valueList[9]
                if ( aircraftMassKilograms < 3e-7 ):
                    loadFactor = 0.0
                else:
                    loadFactor = liftNewtons / aircraftMassKilograms

                calibratedAirSpeedMetersSecond = tas2cas(tas = trueAirSpeedMetersSecond, altitude = altitudeMeanSeaLevelMeters,
                                                temp = 'std' , speed_units = 'm/s', alt_units='m' )
                calibratesAirSpeedKnots = calibratedAirSpeedMetersSecond * MeterSecond2Knots
                mach = self.atmosphere.tas2mach(tas = trueAirSpeedMetersSecond,
                                altitude            = altitudeMeanSeaLevelMeters,
                                speed_units         ='m/s', 
                                alt_units           ='m')

                if (elapsedTimeSeconds-previousElapsedTimeSeconds)>0.0:
                    rateOfClimbDescentFeetMinute = (altitudeMeanSeaLevelFeet-previousAltitudeMeanSeaLevelFeet)/ ((elapsedTimeSeconds-previousElapsedTimeSeconds)/60.)
                else:
                    rateOfClimbDescentFeetMinute = 0.0
                previousAltitudeMeanSeaLevelFeet = altitudeMeanSeaLevelFeet
                
                previousElapsedTimeSeconds = elapsedTimeSeconds
                
                ''' 15th September 024 - nearest NOAA Weather Station '''
                nearestWeatherStation = "None"
                
                ''' 28th September 2024 - temperature at weather station level '''
                temperatureAtWeatherStationDegreesCelsius = 0.0
                windDirectionTrueNorthDegrees = 0.0
                windSpeedKnots = 0.0
                
                ''' 5th September 2021 - write endOfSimulation '''
                endOfSimulation = valueList[10]
                ''' 9th September 2023 - add the characteristic point '''
                xlsxOutput.writeFifteenFloatCharPointValues(elapsedTimeSeconds,
                                                            
                                                characteristic_point,
                                                   
                                                altitudeMeanSeaLevelMeters,
                                                altitudeMeanSeaLevelFeet,
                                                 
                                                trueAirSpeedMetersSecond,
                                                trueAirSpeedKnots,
                                                calibratesAirSpeedKnots,
                                                mach,
                                                rateOfClimbDescentFeetMinute,
                                                 
                                                cumulatedDistanceFlownNautics,
                                                distanceStillToFlyNautics,
                                                 
                                                aircraftMassKilograms,
                                                flightPathAngleDegrees,    
                                                 
                                                thrustNewtons          ,
                                                dragNewtons            ,
                                                liftNewtons            ,
                                                
                                                loadFactor             ,
                                                
                                                nearestWeatherStation  ,
                                                
                                                temperatureAtWeatherStationDegreesCelsius ,
                                                windDirectionTrueNorthDegrees ,
                                                windSpeedKnots,
                                                
                                                endOfSimulation)
        xlsxOutput.close()
        return xlsxOutput