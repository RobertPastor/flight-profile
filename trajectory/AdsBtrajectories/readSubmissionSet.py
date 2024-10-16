'''
Created on 14 oct. 2024

@author: robert
'''

import os
from pathlib import Path
import pandas as pd

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

from trajectory.AdsBtrajectories.utils import readSubmissionSet, encodeCategoryColumn

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
            
        print ('--- encoding aircraft type ---')
        oheAircraftType , df_encoded_aircraft_type, final_df = encodeCategoryColumn(df , 'aircraft_type')
            
        print ("---- encoding wtc ---")
        oheWTC , df_encoded_wtc , final_df = encodeCategoryColumn(final_df  , 'wtc')
        
        print('--- inverse transform ---- ')
        #final_df = final_df.rename(columns=lambda x: str(x).split("_")[-1]  if str(x).startswith("wtc") else x)
        #print ( list ( final_df ))
        numpy_df = oheWTC.inverse_transform( df_encoded_wtc )
        print ( type ( numpy_df ))
        
        df = pd.DataFrame( numpy_df , columns= ['wtc'] )
        print ( list ( df ))
        print ( df.head())
        
        print ("--- encode airline ---")
        unique_airlines_keys = final_df['airline'].unique()
        print("unique airlines = {0}".format((unique_airlines_keys)))
        print("number of unique airlines = {0}".format(len(unique_airlines_keys)))
        
        def convert_airlines_keys(unique_airlines_values , rowValue):
            order = 0
            for unique_airline in unique_airlines_values:
                if ( unique_airline == rowValue ):
                    return "airline" + "_" + str(order)
                order = order + 1
            return 0
            

        final_df['airline'] = final_df['airline'].apply( lambda x : convert_airlines_keys(unique_airlines_keys, x) )
        
        unique_airlines = final_df['airline'].unique()
        
        print("unique airlines = {0}".format((unique_airlines)))
        print("number of unique airlines = {0}".format(len(unique_airlines)))
        


            
        print ( "it's finished")
