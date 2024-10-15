'''
Created on 14 oct. 2024

@author: robert
'''

from trajectory.AdsBtrajectories.readOpenSkyParquet import readParquet
from trajectory.AdsBtrajectories.readChallengeSet import readChallengeSet

import pandas as pd

''' columns to be computed '''
''' year of the flight '''
''' day of the week , monday, tuesday '''
''' month of the year '''
''' ISO week code '''
''' max climbing rate , min descent rate '''
''' cruise level '''
''' adep and ades number of runways -> influence the taxi time ''' 
''' ades and adep airport altitude '''


if __name__ == '__main__':
    
    df_parquet = readParquet()
    print ( "number of parquet rows = {0}".format ( len(df_parquet.index) ) )
    
    df_challenge = readChallengeSet()
    print ( "number of challenge set rows = {0}".format ( len(df_challenge.index) ) )
    
    ''' join the datasets using the flight_id '''
    df_join = pd.merge(df_challenge, df_parquet, how="inner", on=["flight_id", "flight_id"])

    print ( "number of joined dataset rows = {0}".format ( len(df_join.index) ) )
    
    unique_flight_ids = df_join['flight_id'].nunique()
    print("number of unique flight ids = {0}".format(unique_flight_ids))
    
    print ( list(df_join) )
    
    #for headerName in list(df_join.columns.values):
    #    print ( headerName )
    


