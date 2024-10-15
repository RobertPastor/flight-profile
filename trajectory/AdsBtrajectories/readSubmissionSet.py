'''
Created on 14 oct. 2024

@author: robert
'''

import os
from pathlib import Path
import pandas as pd

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
            
        print ( "it's finished")
