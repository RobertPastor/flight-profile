'''
Created on 20 oct. 2024

@author: robert

'''

import os
import pandas as pd
from pathlib import Path

from trajectory.AdsBtrajectories.utils import readChallengeSet
from trajectory.AdsBtrajectories.utils import readSubmissionSet
from sqlalchemy.sql._elements_constructors import true


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
                print ( df_MTOW_lb['MTOW_lb'] )
                mass = df_MTOW_lb.iloc[0]['MTOW_lb'] 
                print ( mass )
                return mass
        return 0.0 
    
    def getMALW_lb(self, ICAOcode = ""):
        for aircraft_type in self.df_aircrafts['ICAO_Code']:
            if ( str(aircraft_type) == ICAOcode ):
                
                df_MALW_lb  = self.df_aircrafts.loc[self.df_aircrafts['ICAO_Code'] == ICAOcode]
                print ( df_MALW_lb['MALW_lb'] )
                mass = df_MALW_lb.iloc[0]['MALW_lb']
                print ( mass )
                return mass
        return 0.0 
               

if __name__ == '__main__':
    print ( "--- read aircraft database ---")
    
    inputFileName = "FAA-Aircraft-Char-DB-AC-150-5300-13B-App-2023-09-07.xlsx"
    inputFolder = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\Aircrafts"
      
    faaAircraftDatabase = FaaAircraftDatabase()
    if ( faaAircraftDatabase.read()):
        
        print(''' ---------- read the challenge train dataset with True TOW values ''')
        df_challenge = readChallengeSet()
        print ( type ( df_challenge))
        print ( list ( df_challenge ) )
        print( df_challenge.shape )
        
        unique_aircrafts_challenge = pd.DataFrame( df_challenge['aircraft_type'].unique() , columns=['aircraft_type'])
        print("unique aircarfts  = {0}".format(unique_aircrafts_challenge))
        
            
        print (''' ------------- read the submission dataset with empty TOW values ----''')
        fileName = "final_submission_set.csv"
        df_submission = readSubmissionSet(fileName)
        print ( list ( df_submission ) )
        print( df_submission.shape )
        
        unique_aircrafts_submission = pd.DataFrame( df_submission['aircraft_type'].unique() , columns=['aircraft_type'])
        print("unique aircarfts  = {0}".format(unique_aircrafts_submission))


        unique_aircrafts = pd.concat([unique_aircrafts_challenge,unique_aircrafts_submission], ignore_index=True)  
        
        unique_aircrafts = pd.DataFrame ( unique_aircrafts['aircraft_type'].unique() , columns= ['aircraft_type'])
        print ( unique_aircrafts.shape )
        print ( list ( unique_aircrafts ))
        
        lbToKilograms = 0.45359237
        
        for aircraft in unique_aircrafts['aircraft_type']:
            print ("--------------")
            print ( str ( aircraft ))
            massMTOW = faaAircraftDatabase.getMTOW_lb(aircraft)
            massMLAW = faaAircraftDatabase.getMALW_lb(aircraft)
            print ( "MTOW {0} lb --- MLAW {1} lb ".format( massMTOW , massMLAW) )
            print ( "MTOW {0} kilograms --- MLAW {1} kilograms ".format( massMTOW * lbToKilograms , massMLAW * lbToKilograms) )
            if ( faaAircraftDatabase.isICAOcodeExisting(str ( aircraft ) ) == False ):
                print ( aircraft + " -not in FAA database")
 
        