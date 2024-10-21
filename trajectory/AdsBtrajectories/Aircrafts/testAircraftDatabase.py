'''
Created on 21 oct. 2024

@author: rober
'''

from trajectory.AdsBtrajectories.Aircrafts.FAAaircraftDatabaseFile import FaaAircraftDatabase
from trajectory.AdsBtrajectories.utils import readChallengeSet
from trajectory.AdsBtrajectories.utils import readSubmissionSet

import pandas as pd

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