'''
Created on 1 juil. 2023

@author: robert
'''
import logging
logger = logging.getLogger(__name__)
import json
import os
from jsonschema import validate , exceptions

from trajectory.Bada381DataFiles import getBadaFilePath

class AircraftJsonPerformance(object):
    
    className = ''
    filePath = ''
    schemaFilePath = ''
    aircraftICAOcode = ''
    performanceJsonData = ''
    
    def __init__(self, aircraftICAOcode , aircraftPerformanceFilePath):
        
        self.className = self.__class__.__name__
        
        self.aircraftICAOcode = aircraftICAOcode

        self.filePath = aircraftPerformanceFilePath
        #super().__init__(self.filePath)
        
        self.schemaFilePath = getBadaFilePath() 
        self.schemaFilePath = os.path.join( self.schemaFilePath , "schema.json" )
        self.schemaFilePath = os.path.abspath( self.schemaFilePath )
        
    def exists(self):
        if os.path.isfile(self.filePath):
            #logging.info self.className + ' : Performance file= ' + self.filePath + " exists"
            return True
        else:
            raise ValueError(self.className + " : Json Performance File not found: " + self.filePath)
        return False
            
    def read(self):
        
        try:
            if os.path.isfile(self.filePath) and os.path.isfile(self.schemaFilePath):
                                
                fData = open(self.filePath)
                #print ( self.schemaFilePath )
                self.performanceJsonData = json.load(fData)
                
                fSchema = open(self.schemaFilePath)
                schema = json.load(fSchema)
                #print ( schema )
                
                validate(instance = self.performanceJsonData , schema = schema )
                #logging.info( self.className + "File = {0} is validated against schema = {1}".format( self.filePath , self.schemaFilePath))
                return True
            
            else:
                logging.error (self.className + " one file at least is not existing - {0} - {1}".format( self.filePath , self.schemaFilePath))
                return False

        except exceptions.ValidationError as e:
            print(self.className + " - Invalid JSON:", e)
            return False
        
    def getICAOcode(self):
        acICAO = self.performanceJsonData["aircraft"]["ICAO"]
        return acICAO.upper()
    
    def getNumberOfEngines(self):
        try:
            nbEngines = int ( self.performanceJsonData["aircraft"]["engines"]["number"])
            return nbEngines
        except:
            raise ValueError(self.className + ': error while reading number of engines')
        return 0
    
    def getEngineType(self):
        return self.performanceJsonData["aircraft"]["engines"]["type"]
    
    def getWakeTurbulenceCategory(self):
        return self.performanceJsonData["aircraft"]["wakeTurbulence"]
    
    def getReferenceMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["reference"]["value"]
    
    def getMinimumMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["minimum"]["value"]
    
    def getMinimumMassTons(self):
        return self.performanceJsonData["aircraft"]["mass"]["minimum"]["value"] / 1000.0

    def getMaximumMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["maximum"]["value"]

    def getMaximumPayLoadMassKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["maxPayload"]["value"]
    
    def getMaximumFuelCapacityKilograms(self):
        return self.performanceJsonData["aircraft"]["mass"]["maxFuelCapacity"]["value"]
    
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

    def getTakeOffLengthMeters(self):
        return self.performanceJsonData["aircraft"]["configuration"]["takeOff"]["takeOffLength"]["value"]
    
    def getLandingLengthMeters(self):
        return self.performanceJsonData["aircraft"]["configuration"]["landing"]["landingLength"]["value"]
    
    def getVstallKcasKnots(self, phase):
        assert (phase in ['CR', 'IC', 'TO', 'AP', 'LD'])
        if phase == "TO":
            phase = "takeOff"
        if phase == "IC":
            phase = "initialClimb"
        if phase == "CR":
            phase = "cruise"
        if phase == "AP":
            phase = "approach"
        if phase == "LD":
            phase = "landing"
        if phase in self.performanceJsonData["aircraft"]["configuration"]:
            return self.performanceJsonData["aircraft"]["configuration"][phase]["stallSpeed"]["value"]
        else:
            raise ValueError("Json Performance : getVstallKcasKnots - error - phase = {0} not in configuration".format(phase))
        
    def getMaxClimbThrustCoeff(self, index):
        #print ( "Aircraft Json Performance -> Max Climb Thrust Coeff -> index = " + str(index) )
        if index==0:
            return self.performanceJsonData["aircraft"]["engineThrust"]["maxClimbThrust"]["coeffOne"]["value"]
        if index==1:
            return self.performanceJsonData["aircraft"]["engineThrust"]["maxClimbThrust"]["coeffTwo"]["value"]
        if index==2:
            return self.performanceJsonData["aircraft"]["engineThrust"]["maxClimbThrust"]["coeffThree"]["value"]
        if index==3:
            return self.performanceJsonData["aircraft"]["engineThrust"]["thrustTemperature"]["coeffOne"]["value"]
        if index==4:
            return self.performanceJsonData["aircraft"]["engineThrust"]["thrustTemperature"]["coeffTwo"]["value"]
        return ValueError("Json Performance : getMaxClimbThrustCoeff - error - index = {0} not correct".format(index))
    
    def getDescentThrustCoeff(self, index):
        print ( "Aircraft Json Performance -> Descent Thrust Coeff -> index = " + str(index) )
        if index==0:
            return self.performanceJsonData["aircraft"]["engineThrust"]["descentThrust"]["coeffLow"]["value"]
        if index==1:
            return self.performanceJsonData["aircraft"]["engineThrust"]["descentThrust"]["coeffHigh"]["value"]
        if index==2:
            return self.performanceJsonData["aircraft"]["engineThrust"]["descentThrust"]["coeffLevel"]["value"]
        if index==3:
            return self.performanceJsonData["aircraft"]["engineThrust"]["descentThrust"]["coeffApproach"]["value"]
        if index==4:
            return self.performanceJsonData["aircraft"]["engineThrust"]["descentThrust"]["coeffLanding"]["value"]

        return 0.0
            
    def getDragCoeff(self, coeffType, phase):
        if phase in self.performanceJsonData["aircraft"]["configuration"]:
            #print ( "phase = {0} is in {1}".format(phase, self.performanceJsonData["aircraft"]["configuration"]))
            if coeffType in ["dragCD0","dragCD2"]:
                return self.performanceJsonData["aircraft"]["configuration"][phase][coeffType]["value"]
            else:
                raise ValueError("Json Performance : error - drag coeff type= {0} -- in phase= {1} not in configuration".format(coeffType, phase))
        else:
            raise ValueError("Json Performance : error - phase= {0} not in configuration".format(phase))
        
    def getLandingGearDragCoeff(self):
        raise ValueError("Json Performance : error - not yet implemented")
    
    def getFuelConsumptionCoeff(self):
        FuelConsumptionCoeff = {}
        FuelConsumptionCoeff[0] = self.performanceJsonData["aircraft"]["fuelConsumption"]["coeffOne"]["value"]
        FuelConsumptionCoeff[1] = self.performanceJsonData["aircraft"]["fuelConsumption"]["coeffTwo"]["value"]
        return FuelConsumptionCoeff

