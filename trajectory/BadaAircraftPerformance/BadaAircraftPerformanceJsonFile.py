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
    aircraftICAOcode = ''
    performanceJsonData = ''
    
    def __init__(self, aircraftICAOcode , aircraftPerformanceFilePath):
        
        self.className = self.__class__.__name__
        
        self.aircraftICAOcode = aircraftICAOcode

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
                self.performanceJsonData = json.load(fData)
                print ( self.performanceJsonData )
                
                fSchema = open(self.schemaFilePath)
                schema = json.load(fSchema)
                print ( schema )
                
                validate(instance = self.performanceJsonData , schema = schema )
                print ("============================================")
                print("File = {0} is validated against schema = {1}".format( self.filePath , self.schemaFilePath))
                print ("============================================")

                assert(  ( self.aircraftICAOcode == self.performanceJsonData["aircraft"]["ICAO"] ) , True )
                return True
            
            else:
                print (" one file at least is not existing - {0} - {1}".format( self.filePath , self.schemaFilePath))
                return False

        except exceptions.ValidationError as e:
            print("Invalid JSON:", e)
            return False
        
        
    def getICAOcode(self):
        acICAO = self.performanceJsonData["aircraft"]["ICAO"]
        print ( acICAO.upper() )
        return acICAO.upper()
    
    def getNumberOfEngines(self):
        try:
            nbEngines = int ( self.performanceJsonData["aircraft"]["engines"]["number"])
            print ( "number of engines = {0}".format( nbEngines ) )
            return nbEngines
        except:
            raise ValueError(self.className + ': error while reading number of engines')
        return 0
    
    def getWakeTurbulenceCategory(self):
        return self.performanceJsonData["aircraft"]["wakeTurbulence"]
    
    def getReferenceMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["reference"]["value"]
    
    def getMinimumMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["minimum"]["value"]

    def getMaximumMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["maximum"]["value"]

    def getMaximumPayLoadMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["maxpayload"]["value"]
    
    def getVmoCasKnots(self):
        return self.performanceJsonData["aircraft"]["envelope"]["MaxOpSpeedCasKnots"]["value"]
    
    def getMaxOpSpeedCasKnots(self):
        return self.getVmoCasKnots()
    
    def getMaxOpMachNumber(self):
        return self.performanceJsonData["aircraft"]["envelope"]["MaxOpMachNumber"]["value"]
    
    def getMaxOpAltitudeFeet(self):
        return self.performanceJsonData["aircraft"]["envelope"]["MaxOpAltitudeFeet"]["value"]
    
    def getWingAreaSurfaceSquareMeters(self):
        return self.performanceJsonData["aircraft"]["aerodynamics"]["wingsurface"]["value"]



        