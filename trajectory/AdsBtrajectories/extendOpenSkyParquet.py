'''
Created on 13 oct. 2024

@author: robert

'''
import os
from pathlib import Path
import pandas as pd
from calendar import Calendar, monthrange
from pickle import TRUE, FALSE
from sqlalchemy.sql._elements_constructors import false

''' https://ansperformance.eu/study/data-challenge/ '''

from trajectory.AdsBtrajectories.utils import readParquet
from datetime import date

def date_iter(calendar, year, month):
    for i in range(1, monthrange(year, month)[1]  + 1):
        yield date(year, month, i)


def extendedOneMonthParquet(df):
    
            print ( list ( df ) )
            print ( "number of rows = {0}".format ( len(df.index) ) )
            print ( df.shape )
            
            unique_flight_ids = df['flight_id'].nunique()
            print("number of unique flight ids = {0}".format(unique_flight_ids))
            
            df_extended = df.filter ( items = ['flight_id'] ).drop_duplicates()
            print ( df_extended.shape )
            print ( df_extended.head(10))
    
     
            df['maxAltitudeFeet'] = df.groupby ( ['flight_id'] ) ['altitude'] . transform('max')
            df_filtered = df.filter( items = ['flight_id','maxAltitudeFeet'] ).drop_duplicates()
            print ( df_filtered.shape )
            print ( df_filtered.head( 10 ))
            
            df_extended = df_extended.merge ( df_filtered  , how="left" , on="flight_id")
            print ( df_extended.shape )
            print ( list( df_extended ))
            print ( df_extended.head(10))
            
            df['maxClimbRateFeetMinutes'] = df.groupby ( ['flight_id'] ) ['vertical_rate'] . transform('max')
            df_filtered = df.filter( items = ['flight_id','maxClimbRateFeetMinutes'] ).drop_duplicates()
            print ( df_filtered.shape )
            print ( df_filtered.head( 10 ))
            
            df_extended = df_extended.merge( df_filtered , how='left' , on='flight_id')
            print ( df_extended.shape )
            print ( list( df_extended ))
            print ( df_extended.head(10))
            
            df['maxDescentRateFeetMinutes'] = df.groupby( ['flight_id'] ) ['vertical_rate'].transform('min')
            df_filtered = df.filter( items = ['flight_id','maxDescentRateFeetMinutes'] ).drop_duplicates()
            print ( df_filtered.shape )
            print ( df_filtered.head( 10 ))
            
            df_extended = df_extended.merge( df_filtered , how='left' , on='flight_id')
            print ( df_extended.shape )
            print ( list( df_extended ))
            print ( df_extended.head(10))
            
            df['avgGroundSpeedKnots'] = df.groupby( ['flight_id'] ) ['groundspeed'].transform('mean')
            df_filtered = df.filter(items=['flight_id','avgGroundSpeedKnots']).drop_duplicates()
            print ( df_filtered.head( 10 ))
            
            df_extended = df_extended.merge( df_filtered , how='left' , on='flight_id')
            print ( df_extended.shape )
            print ( list( df_extended ))
            print ( df_extended.head(10))           
        
            return df_extended
        

if __name__ == '__main__':
    
    calendar = Calendar()
    first = True
    df_final = None
    
    for d in date_iter(calendar , 2022, 1):
        print(str( d ))
        fileName = str(d) + "." + "parquet"
    
        df = readParquet(fileName)
        if not df is None:
            if first == True:
                df_final = extendedOneMonthParquet(df)
                first = false
            else:
                df_extended = extendedOneMonthParquet(df)
                df_final = pd.concat ( [df_final , df_extended] , ignore_index=True)
                                        
    print("--- its all finished ---")
    print ( df_final.shape )
    print ( list ( df_final ))
    print ( df_final.head(100))

