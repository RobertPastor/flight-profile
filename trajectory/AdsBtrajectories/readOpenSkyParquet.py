'''
Created on 13 oct. 2024

@author: robert

'''
import os
from pathlib import Path
import pandas as pd

''' https://ansperformance.eu/study/data-challenge/ '''

def readParquet():
    df = None
    print("Read parquet file")
    
    fileName = "2022-01-01.parquet"
    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge"
    directory = Path(directoryPath)
    if directory.is_dir():
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directory, fileName)
        print ( filePath )
        
        df = pd.read_parquet ( filePath )
    return df

if __name__ == '__main__':
    
    df = readParquet()
    if not df is None:
    
        print ( list ( df ) )
        print ( "number of rows = {0}".format ( len(df.index) ) )
        
        unique_flight_ids = df['flight_id'].nunique()
        print("number of unique flight ids = {0}".format(unique_flight_ids))
 
        # show the list
        #print(icao_24_list)
        ''' flight_id and icao_24 yield the same values '''
        count = 0
        for maxAltitudeFeet in df.groupby(['flight_id'])['altitude'].max():
            count = count + 1
            if count < 10:
                print (" max altitude feet = {0}".format(maxAltitudeFeet))
            
        count = 0
        ''' vertical_rate [ft/min]) '''
        for maxClimbRate in df.groupby( ['flight_id'] ) ['vertical_rate'].max():
            count = count + 1
            if count < 10:
                print (" max climb rate feet/min = {0}".format(maxClimbRate))
                
        count = 0
        for maxDescentRate in df.groupby( ['flight_id'] ) ['vertical_rate'].min():
            count = count + 1
            if count < 10:
                print (" max descent rate feet/min = {0}".format(maxDescentRate))

            
    
