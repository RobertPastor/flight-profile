'''
Created on 20 oct. 2024

@author: robert
'''

from trajectory.AdsBtrajectories.utils import readChallengeSet
from trajectory.AdsBtrajectories.utils import readSubmissionSet
from trajectory.AdsBtrajectories.Airports.AirportDatabaseFile import AirportsDatabase

import pandas as pd

if __name__ == '__main__':
    
    print ( "Read airports database ")
    
    airportsDatabase = AirportsDatabase()
    airportsDBOk = airportsDatabase.read()
    print ( airportsDBOk )
    if airportsDBOk:
    
        print(''' ---------- read the challenge train dataset with True TOW values ''')
        df_challenge = readChallengeSet()
        print ( type ( df_challenge))
        print ( list ( df_challenge ) )
        print( df_challenge.shape )
        
        unique_adeps = pd.DataFrame( df_challenge['adep'].unique() , columns=['airport'])
        print("unique ADEPs  = {0}".format(unique_adeps))
        #print( type ( unique_adeps ))
        
        unique_adess = pd.DataFrame ( df_challenge['ades'].unique() , columns=['airport'])
        print("unique ADESs  = {0}".format(unique_adess))
        
        unique_airports_challenge = pd.concat([unique_adeps,unique_adess], ignore_index=True)
        print ( unique_airports_challenge )
        
        print (''' ------------- read the submission dataset with empty TOW values ----''')
        fileName = "final_submission_set.csv"
        df_submission = readSubmissionSet(fileName)
        print ( list ( df_submission ) )
        print( df_submission.shape )
        
        unique_adeps = pd.DataFrame( df_submission['adep'].unique() , columns=['airport'])
        print("unique ADEPs  = {0}".format(unique_adeps))
        
        unique_ades = pd.DataFrame ( df_submission['ades'].unique() , columns=['airport'])
        print("unique ADESs  = {0}".format(unique_adeps))
        
        unique_airports_submission = pd.concat([unique_adeps,unique_adess], ignore_index=True)
        print ( unique_airports_submission )
        
        print (''' ------------ all unique airports -----------''')
        
        unique_airports = pd.concat ( [ unique_airports_challenge , unique_airports_submission ] , ignore_index=True)
        print ( unique_airports.shape )
        print ( list ( unique_airports ))
        
        unique_airports = pd.DataFrame ( unique_airports['airport'].unique() , columns= ['airport'])
        print ( unique_airports.shape )
        print ( list ( unique_airports ))
        
        for airport in unique_airports['airport']:
            #print ( type ( airport ))
            #print ( airport )
            
            if ( airportsDatabase.isAirportICAOcodeInDB ( str ( airport ) ) == False):
                print ( "{0}".format( str( airport ) ) )
