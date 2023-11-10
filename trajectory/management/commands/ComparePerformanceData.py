'''
Created on 17 oct. 2023

@author: robert
'''
import os

from django.core.management.base import BaseCommand
from trajectory.Bada381DataFiles import getBadaFilePath
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance

class Command(BaseCommand):
    help = 'Load the Airports table'

    def handle(self, *args, **options):
        
        acList = ["A320", "A332", "B738"]
        #acList = ["AXXX.json"]
        for ac in acList:
            print("============ {0} =============".format(ac))
            
            filePath = getBadaFilePath()
    
            filePath = os.path.join( filePath , "{0}.json".format(ac) )
            filePath = os.path.abspath( filePath )
            print ( filePath )
            
            aircraftJsonPerformance = AircraftJsonPerformance(ac , filePath)
            print ( "aircraft performance file is existing = {0}".format(aircraftJsonPerformance.exists()) )
            print ( "aircraft performance file is read = {0}".format(aircraftJsonPerformance.read()) )
            
            filePath = getBadaFilePath()
            filePath = os.path.join( filePath , "{0}__.OPF".format(ac) )
            filePath = os.path.abspath( filePath )
            print ( filePath )
            
            aircraftPerformance = AircraftPerformance(filePath)
            print ( "aircraft performance file is existing = {0}".format(aircraftPerformance.exists()) )
            print ( "aircraft performance file is read = {0}".format(aircraftPerformance.read()) )
            
            print ( "------------- ICAO code ------------")
            print ( aircraftPerformance.getICAOcode())
            print ( aircraftJsonPerformance.getICAOcode())

            print ( "------------- number of engines ------------")
            print ( aircraftPerformance.getNumberOfEngines())
            print ( aircraftJsonPerformance.getNumberOfEngines())
            
            print ( "-------- engine type -----------------")
            print ( aircraftPerformance.getEngineType())
            print ( aircraftJsonPerformance.getEngineType())
            
            print ( "-----wake turbulence category ------" )
            print ( aircraftPerformance.getWakeTurbulenceCategory())
            print ( aircraftJsonPerformance.getWakeTurbulenceCategory())
            
            print ( "----- reference mass kg ------" )
            print ( aircraftPerformance.getReferenceMassKilograms())
            print ( aircraftJsonPerformance.getReferenceMassKilograms())
            
            print ( "----- minimum mass kg ------" )
            print ( aircraftPerformance.getMinimumMassKilograms())
            print ( aircraftJsonPerformance.getMinimumMassKilograms())
            
            print ( "---------- maximum mass kg -------------")
            print ( aircraftPerformance.getMaximumMassKilograms())
            print ( aircraftJsonPerformance.getMaximumMassKilograms())
            
            print ( "--------- max payload kg ---------------")
            print ( aircraftPerformance.getMaximumPayLoadMassKilograms())
            print ( aircraftJsonPerformance.getMaximumPayLoadMassKilograms())
            
            print ( "----------- Maximum Fuel Capacity Kilograms ")
            #print ( aircraftPerformance.getMaximumFuelCapacityKilograms() )
            print ( aircraftJsonPerformance.getMaximumFuelCapacityKilograms() )
            
            print ( "---------- max operating speed VmoCasKnots ------------")
            print ( aircraftPerformance.getVmoCasKnots() )
            print ( aircraftJsonPerformance.getVmoCasKnots() )
            print ( aircraftJsonPerformance.getMaxOpSpeedCasKnots() )
            
            print ( "-------------- getMaxOpMachNumber -----------------")
            print ( aircraftPerformance.getMaxOpMachNumber() )
            print ( aircraftJsonPerformance.getMaxOpMachNumber() )
            
            print ( "-------------- Wing surface meters -----------------")
            print ( aircraftPerformance.getWingAreaSurfaceSquareMeters() )
            print ( aircraftJsonPerformance.getWingAreaSurfaceSquareMeters() )
            
            print ( "-------------- TakeOff length meters -----------------")
            print ( aircraftPerformance.getTakeOffLengthMeters() )
            print ( aircraftJsonPerformance.getTakeOffLengthMeters() )
            
            print ( "-------------- Landing length meters -----------------")
            print ( aircraftPerformance.getLandingLengthMeters() )
            print ( aircraftJsonPerformance.getLandingLengthMeters() )
            
            print ( "-------------- V Stall Knots -----------------")
            print ( aircraftPerformance.getVstallKcasKnots() )
            for phase in [ 'CR', 'IC', 'TO', 'AP', 'LD']:
                print ( phase + " - " + str(aircraftJsonPerformance.getVstallKcasKnots(phase)) )

 
            print ( "-------------- Max Climb Thrust Coeff -----------------")
            for index in range(0,5):
                print ( "--- " + str(index) + " ---")
                print ( str(index) +  " - " + str( aircraftPerformance.getMaxClimbThrustCoeff(index) ) )
                print ( str(index) +  " - " + str ( aircraftJsonPerformance.getMaxClimbThrustCoeff(index) ) )
 