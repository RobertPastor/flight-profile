

import time

from trajectory.Environment.Atmosphere import Atmosphere
from trajectory.Environment.Earth import Earth
from trajectory.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from trajectory.BadaAircraftPerformance.BadaAircraftFile import BadaAircraft
from trajectory.Environment.AirportDatabaseFile import AirportsDatabase
from trajectory.Environment.RunWaysDatabaseFile import RunWayDataBase

from trajectory.Guidance.GroundRunLegFile import GroundRunLeg

if __name__ == '__main__':

    atmosphere = Atmosphere()
    earth = Earth()
    
    print ( '==================== Ground run ==================== '+ time.strftime("%c") )
    acBd = BadaAircraftDatabase()
    aircraftICAOcode = 'A320'
    if acBd.read():
        if ( acBd.aircraftExists(aircraftICAOcode) 
             and acBd.aircraftPerformanceFileExists(acBd.getAircraftPerformanceFile(aircraftICAOcode))):
            
            print ( '==================== aircraft found  ==================== '+ time.strftime("%c") )
            aircraft = BadaAircraft(aircraftICAOcode, 
                                  acBd.getAircraftPerformanceFile(aircraftICAOcode),
                                  atmosphere,
                                  earth)
            aircraft.dump()
    
    print ( '==================== Ground run ==================== '+ time.strftime("%c") )
    airportsDB = AirportsDatabase()
    assert airportsDB.read()
    
    CharlesDeGaulle = airportsDB.getAirportFromICAOCode('LFPG')
    print ( CharlesDeGaulle )
    
    print ( '==================== Ground run - read runway database ==================== '+ time.strftime("%c") )
    runWaysDatabase = RunWayDataBase()
    assert runWaysDatabase.read()
    
    print ( '==================== Ground run ==================== '+ time.strftime("%c") )
    runway = runWaysDatabase.getFilteredRunWays('LFPG', aircraft.WakeTurbulenceCategory)
    print ( runway )
    
    print ( '==================== departure Ground run ==================== '+ time.strftime("%c") )
    groundRun = GroundRunLeg(runway=runway, 
                             aircraft=aircraft,
                             airport=CharlesDeGaulle)
    groundRun.buildDepartureGroundRun(deltaTimeSeconds = 0.1,
                                elapsedTimeSeconds = 0.0,
                                distanceStillToFlyMeters = 100000.0)
    groundRun.createKmlOutputFile()
    groundRun.createXlsxOutputFile()
        
    print ( '==================== Get Arrival Airport ==================== '+ time.strftime("%c") )
    arrivalAirportIcaoCode = 'LFML'
    arrivalAirport = airportsDB.getAirportFromICAOCode(arrivalAirportIcaoCode)
    print ( arrivalAirport )
    
    print ( '====================  arrival run-way ==================== '+ time.strftime("%c") )
    arrivalRunway = runWaysDatabase.getFilteredRunWays(arrivalAirportIcaoCode,
                                                        aircraft.WakeTurbulenceCategory)
    print ( arrivalRunway )
    print ( '==================== arrival Ground run ==================== '+ time.strftime("%c") )
#     aircraft.setLandingConfiguration(elapsedTimeSeconds = 0.0)
#     
#     aircraft.initStateVector(elapsedTimeSeconds = 0.0,
#                           trueAirSpeedMetersSecond = 101.0 * Knots2MetersPerSecond, 
#                           airportFieldElevationAboveSeaLevelMeters = arrivalAirport.getFieldElevationAboveSeaLevelMeters())
# 
#     groundRun = GroundRunLeg(runway = runway, 
#                              aircraft = aircraft,
#                              airport = CharlesDeGaulle)
#     groundRun.buildArrivalGroundRun(deltaTimeSeconds = 0.1,
#                               elapsedTimeSeconds = 0.0,
#                               initialWayPoint)
#     groundRun.createXlsxOutputFile()
#     groundRun.createKmlOutputFile()
