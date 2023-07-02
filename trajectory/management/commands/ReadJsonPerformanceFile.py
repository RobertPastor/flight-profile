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
        
        acList = ["A320.json", "A330.json", "B738.json"]
        #acList = ["AXXX.json"]
        for ac in acList:
            
            filePath = getBadaFilePath()
    
            filePath = os.path.join( filePath , ac )
            filePath = os.path.abspath( filePath )
            #print ( filePath )
        
            aircraftJsonPerformance = AircraftJsonPerformance(filePath)
            #print( "Aircraft Performance file = {0} - is existing = {1}".format( filePath, aircraftJsonPerformance.exists() ) )
            
            ret = aircraftJsonPerformance.read()
            print( "Aircraft Performance read = {0} ".format( ret ) )


