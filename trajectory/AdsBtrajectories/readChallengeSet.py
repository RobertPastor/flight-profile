'''
Created on 14 oct. 2024

@author: robert
'''

import os
from pathlib import Path
import pandas as pd
from trajectory.AdsBtrajectories.Airports.AirportDatabaseFile import AirportsDatabase

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

''' https://ansperformance.eu/study/data-challenge/ '''

from trajectory.AdsBtrajectories.utils import readChallengeSet, extendDataSetWithDates

if __name__ == '__main__':
    
    print ( "Read airports database ")
    
    airportsDatabase = AirportsDatabase()
    airportsDBOk = airportsDatabase.read()
    print ( airportsDBOk )
    
    print("Read challenge set file")
    
    df = readChallengeSet()
    if ( not df is None ) and ( airportsDBOk == True):

        print ( list ( df ) )
        print ( "number of rows = {0}".format ( len(df.index) ) )
        
        df = extendDataSetWithDates (df)
        print ( list ( df ))
        
        unique_flight_ids = df['flight_id'].nunique()
        print("number of unique flight ids = {0}".format(unique_flight_ids))
        
        unique_aircraft_types = df['aircraft_type'].unique()
        print("number of unique aircraft types = {0}".format(unique_aircraft_types))
        
        print ( df.value_counts(subset=['aircraft_type']) )
        df_aircraft_type = df.value_counts(subset=['aircraft_type'])
        
        print ("---------- begin add adep ades elevation meters ---")
        
        ''' create a new column '''
        #df["adep_elevation_meters"] = df.apply(lambda row: airportsDatabase.getAirportElevationMeters(row['adep']), axis=1)
        #df["ades_elevation_meters"] = df.apply(lambda row: airportsDatabase.getAirportElevationMeters(row['ades']), axis=1)
        
        #print ( df_aircraft_type )
        
        df_a320 = df.loc[df['aircraft_type'] == "A320"]
        print ( list ( df_a320 ))


        # Using iterrows to iterate over DataFrame rows
        for index, row in df_a320.iterrows():
            if ( index < 100 ):
                print(index ,row['flight_id'], row['aircraft_type'] , row['flight_duration'] , row['flown_distance'], row['tow'])
            else:
                break

        #for index, row in df_a320.iterrows():
        #    print ( index , row['flight_id'], row['adep'], row['ades'] )
        #    print ( index , airportsDatabase.getAirportFromICAOCode( row['adep'] ) , airportsDatabase.getAirportFromICAOCode( row['ades'] ))
            
        for uniqueAdep in df_a320['adep'].unique():
            if airportsDatabase.getAirportFromICAOCode( str(uniqueAdep) ):
                pass
                #print ( uniqueAdep )
            else:
                print ( "not found - {0}".format( uniqueAdep ))
            
        for uniqueAdes in df_a320['ades'].unique():
            if airportsDatabase.getAirportFromICAOCode( str(uniqueAdes) ):
                pass
                #print ( uniqueAdes )
            else:
                print ( "not found - {0}".format( uniqueAdes ))
            
        #for index, row in df_a320.iterrows():
        #    print ("----------------")
        #    print ( index , row['flight_id'], row['adep'], row['adep_elevation_meters'] )
        #    print ( index , row['flight_id'], row['ades'], row['ades_elevation_meters'] )
        
        ''' encoding aircraft type wtc and airline '''
        columnNameList = ['aircraft_type','wtc']
        transformer = make_column_transformer( (OneHotEncoder(), columnNameList ), remainder='passthrough')
        
        transformed = transformer.fit_transform(df)
        #print ( transformer.get_feature_names_out() )
    
        #transformed_df = pd.DataFrame(transformed, columns=columnNameList)
        transformed_df = pd.DataFrame(transformed, columns=transformer.get_feature_names_out())
        
        print ( list ( transformed_df ))
        print(transformed_df.head(10))
    

        
    
    

            
        print ( "--- it's finished ---")
