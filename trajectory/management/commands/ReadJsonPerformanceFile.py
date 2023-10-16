'''
Created on 1 juil. 2023

@author: robert
'''

import os
from django.core.management.base import BaseCommand
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceJsonFile import AircraftJsonPerformance
from trajectory.Bada381DataFiles import getBadaFilePath

class Command(BaseCommand):
    help = 'Load the Airports table'

    def handle(self, *args, **options):
        
        acList = ["A320", "A330", "B738"]
        #acList = ["AXXX.json"]
        for ac in acList:
            
            filePath = getBadaFilePath()
    
            filePath = os.path.join( filePath , "{0}.json".format(ac) )
            filePath = os.path.abspath( filePath )
            print ( filePath )
        
            aircraftJsonPerformance = AircraftJsonPerformance(ac , filePath)
            #print( "Aircraft Performance file = {0} - is existing = {1}".format( filePath, aircraftJsonPerformance.exists() ) )
            
            ret = aircraftJsonPerformance.read()
            print( "Aircraft Performance read = {0} ".format( ret ) )
            
            print (aircraftJsonPerformance.getICAOcode())

            print ("---- nomber of engines ----")

            print (aircraftJsonPerformance.getNumberOfEngines())
            
            print ("---- wake turbulence ----")

            print ( aircraftJsonPerformance.getWakeTurbulenceCategory())
            
            print ("---- mass (kg) ----")

            print ( aircraftJsonPerformance.getReferenceMassKilograms())
            print ( aircraftJsonPerformance.getMinimumMassKilograms())
            print ( aircraftJsonPerformance.getMaximumMassKilograms())
            
            print ( aircraftJsonPerformance.getMaximumPayLoadMassKilograms())
            
            print ( aircraftJsonPerformance.getMaximumFuelCapacityKilograms() )
        
            print ("---- envelope ----")
            
            print ( aircraftJsonPerformance.getMaxOpSpeedCasKnots())
            print ( aircraftJsonPerformance.getMaxOpMachNumber())

            print ( aircraftJsonPerformance.getMaxOpAltitudeFeet())
            
            print ("---- aerodynamics ----")
            print ( aircraftJsonPerformance.getWingAreaSurfaceSquareMeters())
            
            print ("---- stall speeds ---")
            for phase in ["takeOff","initialClimb","cruise","approach","landing"]:
                print ( "--- {0} ---".format(phase) )
                print ( aircraftJsonPerformance.getVstallKcasKnots(phase))
                
            print ("---- Drag Coeff ---")
            for coeffType in ["dragCD0", "dragCD2"]:
                for phase in ["takeOff","initialClimb","cruise","approach","landing"]:
                    print ( "--- {0} ---".format(phase) )
                    print ( aircraftJsonPerformance.getDragCoeff(coeffType, phase))