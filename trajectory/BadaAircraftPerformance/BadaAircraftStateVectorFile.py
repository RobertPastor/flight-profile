'''
@since: Created on 21 mars 2015

@author: PASTOR Robert

        Written By:
                Robert PASTOR 
                @Email: < robert [--DOT--] pastor0691 (--AT--) gmail [--DOT--] com >

        @http://trajectoire-predict.monsite-orange.fr/ 
        @copyright: Copyright 2015 Robert PASTOR 

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

from trajectory.Environment.Constants import MeterSecond2Knots , Meter2Feet, Meter2NauticalMiles

from trajectory.OutputFiles.XlsxOutputFile import XlsxOutput
from trajectory.Environment.Atmosphere import Atmosphere

from trajectory.aerocalc.airspeed import tas2cas


class StateVector(object):
    
    className = ''
    aircraftStateHistory = []
    atmosphere = None
    flightEnvelope = None
    
    nearestNoaaWeatherStation = ""
    latestInterpolatedTemperature = 0.0
    latestInterpolatedWindDirection = 0.0
    latestInterpolatedWindSpeed = 0.0

    def __init__(self, aircraftICAOcode, atmosphere , flightEnvelope):
        
        self.className = self.__class__.__name__

        assert isinstance(atmosphere, Atmosphere)
        self.atmosphere = atmosphere
        self.flightEnvelope = flightEnvelope
        
        self.nearestNoaaWeatherStation = ""
        self.latestInterpolatedTemperature = 0.0
        self.latestInterpolatedWindDirection = 0.0
        self.latestInterpolatedWindSpeed = 0.0
        
        self.aircraftICAOcode = str(aircraftICAOcode).upper()
        self.aircraftStateHistory = []

    def initStateVector(self,
                        elapsedTimeSeconds, 
                        characteristicPoint,
                        trueAirSpeedMetersSecond, 
                        altitudeMeanSeaLevelMeters,
                        aircraftMassKilograms,
                        totalDistanceFlownMeters = 0.0,
                        distanceStillToFlyMeters = 0.0):
 
        flightPathAngleDegrees = 0.0
        ''' 9th September 2023 - add characteristic point to state vector '''
        self.updateAircraftStateVector(elapsedTimeSeconds, 
                                    characteristicPoint,
                                    trueAirSpeedMetersSecond  , 
                                    altitudeMeanSeaLevelMeters,
                                    totalDistanceFlownMeters  ,
                                    distanceStillToFlyMeters  ,
                                    aircraftMassKilograms     ,
                                    flightPathAngleDegrees    ,
                                    thrustNewtons = 0.0       ,
                                    dragNewtons   = 0.0       ,
                                    liftNewtons   = 0.0       ,
                                    currentPosition = "None"  ,
                                    endOfSimulation = False)
        
    
    ''' 15th September 2024 - currentPosition used to retrieve the nearest weather station '''
    def updateAircraftStateVector(self, 
                                    elapsedTimeSeconds, 
                                    characteristicPoint,
                                    trueAirSpeedMetersPerSecond,
                                    altitudeMeanSeaLevelMeters,
                                    totalDistanceFlownMeters,
                                    distanceStillToFlyMeters,
                                    aircraftMassKilograms,
                                    flightPathAngleDegrees,
                                    thrustNewtons,
                                    dragNewtons,
                                    liftNewtons,
                                    currentPosition,
                                    endOfSimulation):

        ''' need to store both TAS and altitude => compute CAS '''
        aircraftStateDict = {}
        ''' 28th September 2024 '''
        self.nearestNoaaWeatherStation = self.flightEnvelope.computeNearestNoaaWeatherStationFAAname(currentPosition, totalDistanceFlownMeters)
        ''' 28th September 2024 '''
        self.latestInterpolatedTemperature = self.flightEnvelope.computeTemperatureDegreesCelsiusAtStationLevel(self.nearestNoaaWeatherStation , altitudeMeanSeaLevelMeters)
        ''' 10th october 2024 '''
        self.latestInterpolatedWindDirection = self.flightEnvelope.computeTrueNorthWindDirectionAtStationLevel(self.nearestNoaaWeatherStation , altitudeMeanSeaLevelMeters)
        self.latestInterpolatedWindSpeed = self.flightEnvelope.computeWindSpeedKnotsAtStationLevel(self.nearestNoaaWeatherStation , altitudeMeanSeaLevelMeters)
                
        ''' 9th September 2023 - add characteristic point '''
        aircraftStateDict[elapsedTimeSeconds] = [characteristicPoint,
                                                 altitudeMeanSeaLevelMeters, 
                                                 trueAirSpeedMetersPerSecond, 
                                                 totalDistanceFlownMeters,
                                                 distanceStillToFlyMeters,
                                                 aircraftMassKilograms,
                                                 flightPathAngleDegrees,
                                                 thrustNewtons,
                                                 dragNewtons,
                                                 liftNewtons ,
                                                 self.nearestNoaaWeatherStation,
                                                 self.latestInterpolatedTemperature,
                                                 self.latestInterpolatedWindDirection,
                                                 self.latestInterpolatedWindSpeed,
                                                 endOfSimulation]
        self.aircraftStateHistory.append(aircraftStateDict)
        
    ''' 13th September 2023 - get last characteristic point '''
    def getLastCharacteristicPoint(self):
        if len(self.aircraftStateHistory) > 0:
            ''' values returns a list whose first element is the expected value '''
            lastDict = self.aircraftStateHistory[-1]
            values = lastDict.values()
            characteristicPoint = list(values)[0][0]
            return characteristicPoint
        else:
            return 0.0

    ''' 9th September 2023 - characteristic point 1st in stack '''
    def getCurrentAltitudeSeaLevelMeters(self):
        if len(self.aircraftStateHistory) > 0:
            ''' values returns a list whose first element is the expected value '''
            lastDict = self.aircraftStateHistory[-1]
            values = lastDict.values()
            altitudeMSLmeters = list(values)[0][1]
            return altitudeMSLmeters
        else:
            return 0.0
        
    def getCurrentTrueAirSpeedMetersSecond(self):
        if len(self.aircraftStateHistory) > 0:
            ''' each recorded value is a dictionary '''
            ''' values() retrieves a list with one element - take the one with index = 0 '''
            lastDict = self.aircraftStateHistory[-1]
            values = lastDict.values()
            trueAirSpeedMetersSecond =  list(values)[0][2]
            return trueAirSpeedMetersSecond
        else:
            raise ValueError(self.className + ': speed history is empty')

    def getCurrentDistanceFlownMeters(self):
        if len(self.aircraftStateHistory) > 0:
            lastDict = self.aircraftStateHistory[-1]
            values = lastDict.values()
            currentDistanceMeters = list(values)[0][3]
            return currentDistanceMeters
        else:
            return 0.0
        
    def getFlightPathAngleDegrees(self):
        if len(self.aircraftStateHistory) > 0:
            lastDict = self.aircraftStateHistory[-1]
            values = lastDict.values()
            flightPathAngleDegrees = list(values)[0][6]
            return flightPathAngleDegrees
        else:
            return 0.0        

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
                loadFactor = liftNewtons / aircraftMassKilograms

                calibratedAirSpeedMetersSecond = tas2cas(tas = trueAirSpeedMetersSecond, altitude = altitudeMeanSeaLevelMeters,
                                                temp = 'std' , speed_units = 'm/s', alt_units='m' )
                calibratesAirSpeedKnots = calibratedAirSpeedMetersSecond * MeterSecond2Knots
                mach = self.atmosphere.tas2mach(tas = trueAirSpeedMetersSecond,
                                altitude = altitudeMeanSeaLevelMeters,
                                speed_units='m/s', 
                                alt_units='m')

                if (elapsedTimeSeconds-previousElapsedTimeSeconds)>0.0:
                    rateOfClimbDescentFeetMinute = (altitudeMeanSeaLevelFeet-previousAltitudeMeanSeaLevelFeet)/ ((elapsedTimeSeconds-previousElapsedTimeSeconds)/60.)
                else:
                    rateOfClimbDescentFeetMinute = 0.0
                previousAltitudeMeanSeaLevelFeet = altitudeMeanSeaLevelFeet
                
                previousElapsedTimeSeconds = elapsedTimeSeconds
                
                ''' 15th September 024 - nearest NOAA Weather Station '''
                nearestWeatherStation = valueList[10]
                
                ''' 28th September 2024 - temperature at weather station level '''
                temperatureAtWeatherStationDegreesCelsius = valueList[11]
                windDirectionTrueNorthDegrees = valueList[12]
                windSpeedKnots = valueList[13]
                
                ''' 5th September 2021 - write endOfSimulation '''
                endOfSimulation = valueList[14]
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
                    
    def writeHeaders(self, ws, style, headers):
        row = 0
        col = 0
        for header in headers:
            ws.write(row, col , header , style)
            col = col + 1
            
    def writeValues(self, ws, row, elapsedTimeSeconds, characteristicPoint,
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
                                                 endOfSimulation):

        ColumnIndex = 0
        ws.write(row, ColumnIndex, elapsedTimeSeconds)
        ColumnIndex += 1
        ws.write(row, ColumnIndex, characteristicPoint)    
        ColumnIndex += 1
        ws.write(row, ColumnIndex, altitudeMeanSeaLevelMeters)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, altitudeMeanSeaLevelFeet)                
        ColumnIndex += 1
        ws.write(row, ColumnIndex, trueAirSpeedMetersSecond)                
        ColumnIndex += 1
        ws.write(row, ColumnIndex, trueAirSpeedKnots)                
        ColumnIndex += 1
        ws.write(row, ColumnIndex, calibratesAirSpeedKnots)                
        ColumnIndex += 1
        ws.write(row, ColumnIndex, mach)
        ColumnIndex += 1
        ws.write(row, ColumnIndex, rateOfClimbDescentFeetMinute)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, cumulatedDistanceFlownNautics)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, distanceStillToFlyNautics)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, aircraftMassKilograms)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, flightPathAngleDegrees)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, thrustNewtons)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, dragNewtons)        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, liftNewtons)
        ColumnIndex += 1
        ws.write(row, ColumnIndex, loadFactor)    
        ColumnIndex += 1
        ws.write(row, ColumnIndex, nearestWeatherStation)  
        ColumnIndex += 1
        ws.write(row, ColumnIndex, temperatureAtWeatherStationDegreesCelsius)
        
        ColumnIndex += 1
        ws.write(row, ColumnIndex, windDirectionTrueNorthDegrees)
        ColumnIndex += 1
        ws.write(row, ColumnIndex, windSpeedKnots)
        ColumnIndex += 1
        ws.write(row, ColumnIndex, str(endOfSimulation))     
        row += 1    
        return row
        
                    
    def createStateVectorHistorySheet(self, workbook):
        
        ws = workbook.add_worksheet("StateVector")
        #styleEntete = workbook.add_format({'bold': False, 'border':True})
        styleLavender = workbook.add_format({'bold': True, 'border':True, 'bg_color': 'yellow'})
        ''' 9th September 2023 add characteristic point '''
        self.writeHeaders(ws, styleLavender, ['elapsed-time-seconds', 
                                              
                                'characteristic-point',
                                
                                'altitude-MSL-meters',
                                 'altitude-MSL-feet',

                                 'true-air-speed-meters-second',
                                 'true-air-speed-knots',
                                 
                                 'calibrated-air-speed-knots',
                                 'mach',
                                 'rate-of-climb-descent-feet-minute',
                                 
                                 'distance-flown-nautical-miles',
                                 'distance-to-fly-nautical-miles',
                                 
                                 'aircraft-mass-kilograms'      ,
                                 'flight-path-angle-degrees'    ,
                                 
                                 'thrust-newtons'               ,
                                 'drag-newtons'                 ,
                                 'lift-newtons'                 ,
                                 
                                 'load-factor-g'                ,
                                 'nearest-weather-station'      ,
                                 'temperature-degrees-celsius'  ,
                                 'wind-direction-true-north-degrees',
                                 'wind-speed-knots',
                                 'end of simulation'
                                 ])

        previousAltitudeMeanSeaLevelFeet = 0.0
        previousElapsedTimeSeconds = 0.0
        cumulatedDistanceFlownNautics = 0.0
        
        row = 1
        
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
                if aircraftMassKilograms > 0.0: 
                    loadFactor = liftNewtons / aircraftMassKilograms
                else:
                    loadFactor = 0.0

                calibratedAirSpeedMetersSecond = tas2cas(tas = trueAirSpeedMetersSecond,  altitude = altitudeMeanSeaLevelMeters,
                                                  temp = 'std' , speed_units = 'm/s', alt_units='m' )
                calibratesAirSpeedKnots = calibratedAirSpeedMetersSecond * MeterSecond2Knots
                if trueAirSpeedMetersSecond > 0.0:
                    mach = self.atmosphere.tas2mach(tas         = trueAirSpeedMetersSecond,
                                                altitude    = altitudeMeanSeaLevelMeters,
                                                speed_units = 'm/s', 
                                                alt_units   = 'm')
                else:
                    mach = 0.0

                if (elapsedTimeSeconds-previousElapsedTimeSeconds)>0.0:
                    rateOfClimbDescentFeetMinute = (altitudeMeanSeaLevelFeet-previousAltitudeMeanSeaLevelFeet)/ ((elapsedTimeSeconds-previousElapsedTimeSeconds)/60.)
                else:
                    rateOfClimbDescentFeetMinute = 0.0
                previousAltitudeMeanSeaLevelFeet = altitudeMeanSeaLevelFeet
                
                previousElapsedTimeSeconds = elapsedTimeSeconds
                ''' 15th September 2024 - nearest weather station '''
                nearestWeatherStation = valueList[10]
                
                ''' 28th September 2024 - interpolated temperature forecasts at weather station '''
                temperatureDegreesCelsius = valueList[11]
                windDirectionTrueNorthDegree = valueList[12]
                windSpeedKnots = valueList[13]
                
                ''' 5th September 2021 - write endOfSimulation '''
                endOfSimulation = valueList[14]
                ''' 9th September 2023 - add characteristic point '''
                row = self.writeValues(ws, row, elapsedTimeSeconds, 
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
                                                temperatureDegreesCelsius ,
                                                windDirectionTrueNorthDegree ,
                                                windSpeedKnots,
                                                endOfSimulation)
        
