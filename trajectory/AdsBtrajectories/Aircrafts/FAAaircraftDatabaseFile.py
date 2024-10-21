'''
Created on 20 oct. 2024

@author: robert

'''

import os
import pandas as pd
from pathlib import Path


class FaaAircraftDatabase(object):
    
    inputFileName = "FAA-Aircraft-Char-DB-AC-150-5300-13B-App-2023-09-07.xlsx"
    inputFolder = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\Aircrafts"
    directoryPath = ""

    dataframe = None
    
    def __init__(self):
        pass
        self.directoryPath = Path(self.inputFolder)
        
        if self.directoryPath.is_dir():
            print ( "it is a directory - {0}".format(self.directoryPath))
            filePath = os.path.join(self.directoryPath, self.inputFileName)
            
            print ( filePath )
            
    def read(self):
        pass
        if self.directoryPath.is_dir():
            filePath = os.path.join(self.directoryPath, self.inputFileName)

            self.df_aircrafts = pd.read_excel( filePath )
            print ( self.df_aircrafts.shape )
            print ( list ( self.df_aircrafts ) )
            print ( self.df_aircrafts.head() )
            
            return True
        return False
    
    def isICAOcodeExisting(self, ICAOcode = ""):
        for aircraft_type in self.df_aircrafts['ICAO_Code']:
            if ( str(aircraft_type) == ICAOcode ):
                return True
        return False

    def getMTOW_lb(self, ICAOcode = ""):
        for aircraft_type in self.df_aircrafts['ICAO_Code']:
            if ( str(aircraft_type) == ICAOcode ):
                
                df_MTOW_lb  = self.df_aircrafts.loc[self.df_aircrafts['ICAO_Code'] == ICAOcode]
                #print ( df_MTOW_lb['MTOW_lb'] )
                mass = df_MTOW_lb.iloc[0]['MTOW_lb'] 
                #print ( mass )
                return mass
        return 0.0 
    
    def getMALW_lb(self, ICAOcode = ""):
        for aircraft_type in self.df_aircrafts['ICAO_Code']:
            if ( str(aircraft_type) == ICAOcode ):
                
                df_MALW_lb  = self.df_aircrafts.loc[self.df_aircrafts['ICAO_Code'] == ICAOcode]
                #print ( df_MALW_lb['MALW_lb'] )
                mass = df_MALW_lb.iloc[0]['MALW_lb']
                #print ( mass )
                return mass
        return 0.0 
               
    def getPhysicalClassEngine(self, ICAOcode = ""):
        for aircraft_type in self.df_aircrafts['ICAO_Code']:
            if ( str(aircraft_type) == ICAOcode ):
                
                engineClass  = self.df_aircrafts.loc[self.df_aircrafts['ICAO_Code'] == ICAOcode]
                #print ( df_MALW_lb['MALW_lb'] )
                physicalEngineClass = engineClass.iloc[0]['Physical_Class_Engine']
                #print ( mass )
                return physicalEngineClass
        return "Jet"

    def getNumberOfEngines(self, ICAOcode = ""):
        for aircraft_type in self.df_aircrafts['ICAO_Code']:
            if ( str(aircraft_type) == ICAOcode ):
                
                numberOfEngines  = self.df_aircrafts.loc[self.df_aircrafts['ICAO_Code'] == ICAOcode]
                #print ( df_MALW_lb['MALW_lb'] )
                nbEngines = numberOfEngines.iloc[0]['Num_Engines']
                #print ( mass )
                return nbEngines
        return 2.0
    
    def getApproachSpeedKnots(self, ICAOcode = ""):
        for aircraft_type in self.df_aircrafts['ICAO_Code']:
            if ( str(aircraft_type) == ICAOcode ):
                
                approachSpeedKnots  = self.df_aircrafts.loc[self.df_aircrafts['ICAO_Code'] == ICAOcode]
                #print ( df_MALW_lb['MALW_lb'] )
                approachSpeedKnots = approachSpeedKnots.iloc[0]['Approach_Speed_knot']
                #print ( mass )
                return approachSpeedKnots
        return 0.0
 
 
 
        