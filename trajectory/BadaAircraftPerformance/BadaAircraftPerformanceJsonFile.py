'''
Created on 1 juil. 2023

@author: robert
'''

import json
import os
from jsonschema import validate , exceptions

from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.Bada381DataFiles import getBadaFilePath

class AircraftJsonPerformance(AircraftPerformance):
    
    className = ''
    filePath = ''
    schemaFilePath = ''
    
    def __init__(self, aircraftPerformanceFilePath):
        self.className = self.__class__.__name__

        self.filePath = aircraftPerformanceFilePath
        super().__init__(self.filePath)
        
        self.schemaFilePath = getBadaFilePath() 
        self.schemaFilePath = os.path.join( self.schemaFilePath , "schema.json" )
        self.schemaFilePath = os.path.abspath( self.schemaFilePath )
            
            
    def read(self):
        
        try:
            if os.path.isfile(self.filePath) and os.path.isfile(self.schemaFilePath):
                
                #print ( "both file are existing ")
                
                fData = open(self.filePath)
                #print ( self.schemaFilePath )
                performanceJsonData = json.load(fData)
                print ( performanceJsonData )
                
                fSchema = open(self.schemaFilePath)
                schema = json.load(fSchema)
                print ( schema )
                
                validate(instance = performanceJsonData , schema = schema )
                print("File = {0} is validated against schema = {1}".format( self.filePath , self.schemaFilePath))
                
                return True
            
            else:
                print (" one file is not existing - {0} - {1}".format( self.filePath , self.schemaFilePath))
                return False

        except exceptions.ValidationError as e:
            print("Invalid JSON:", e)
        
