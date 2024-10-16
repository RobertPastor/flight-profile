'''
Created on 14 oct. 2024

@author: robert
'''

import os
from pathlib import Path
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

from trajectory.AdsBtrajectories.utils import readSubmissionSet

''' https://ansperformance.eu/study/data-challenge/ '''

if __name__ == '__main__':
    
    df = readSubmissionSet()
    if ( not df is None ):

        print ( list ( df ) )
        print ( "number of rows = {0}".format ( len(df.index) ) )
        
        unique_flight_ids = df['flight_id'].nunique()
        print("number of unique flight ids = {0}".format(unique_flight_ids))
        
        unique_aircraft_types = df['aircraft_type'].unique()
        print("number of unique aircraft types = {0}".format(unique_aircraft_types))
        
        print ( df.value_counts(subset=['aircraft_type']) )
        df_aircraft_type = df.value_counts(subset=['aircraft_type'])
        
        df_aircraft_type = df.value_counts(subset=['aircraft_type'])
        print ( df_aircraft_type )
        
        df_a320 = df.loc[df['aircraft_type'] == "A320"]

        # Using iterrows to iterate over DataFrame rows
        for index, row in df_a320.iterrows():
            if ( index < 10 ):
                print(index , row)
            else:
                break
            
        print (''' encoding aircraft type ''')
        columnNameList = ['aircraft_type','wtc']
        oheAircraftType = OneHotEncoder(handle_unknown='ignore')
    
        df_encoded_aircraft_type = pd.DataFrame( oheAircraftType.fit_transform( df[['aircraft_type']] ).toarray() )
        
        print ( list ( df_encoded_aircraft_type ))
        print(df_encoded_aircraft_type.head(10))
        
        final_df = df.join( df_encoded_aircraft_type )
        print ( final_df.head ())
        
        print ( list ( final_df ))
        print(final_df.head(10))
        
        final_df = final_df.rename(columns=lambda x: str('aircraft_type_') + str(x) if str(x).isdigit() else x)
                
        final_df = final_df.drop(columns=['aircraft_type'])
        print ( list ( final_df ))
        print(final_df.head(10))
        
        
        print('--- inverse transform ---- ')
        
       
            
        print ( "it's finished")
