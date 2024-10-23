'''
Created on 19 oct. 2024

@author: robert
'''

import warnings
import os
from tqdm import TqdmExperimentalWarning
from pathlib import Path

import matplotlib.pyplot as plt
from traffic.core import Traffic
from trajectory.AdsBtrajectories.utils import readParquet
import pandas as pd

def q_low(x):
    return x.quantile(0.25)

def q_high(x):
    return x.quantile(0.75)

if __name__ == '__main__':
    
    warnings.filterwarnings("ignore", category=TqdmExperimentalWarning)
    warnings.filterwarnings("ignore", category=FutureWarning)
    
    fileName =  "2022-01-01" + ".parquet"
    fileName = "2022-12-31" + ".parquet"
    flight_id = "258064118"
    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge"
    directory = Path(directoryPath)
    if directory.is_dir():
        
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directory, fileName)
        print ( filePath )
        
        df = readParquet(fileName)
        #df = extendedOneDayParquet(df)
        print ( list ( df ))
        
        flight_id = "258064118"
        ''' keep data for one flight id '''
        df = df[df['flight_id'] == int ( flight_id ) ]
        print ( df['flight_id'].dtype )
        print ( list ( df ))
        print ( df.head(10) )
        
        print ( df['flight_id'].nunique())
        print ( df['altitude'].max(numeric_only=True))
        
        df = df.filter( items = ['flight_id' , 'altitude']).reset_index()
        print ( list ( df ) )
        
        #f = {'altitude': [ 'median', 'std' , q_low, q_high ]}
        df['q_high']  = df.groupby('flight_id' , as_index=False )['altitude'] .transform(q_high)
        df['q_low']  = df.groupby('flight_id' , as_index=False )['altitude'] .transform(q_low)
        
        print ( list ( df ))
        print ( df.head() )
        
        print ( "--- try to filter ---")
        df = df.loc[ df['altitude'] < df['q_high'] ]
        df = df.loc[ df['altitude'] > df['q_low'] ]
        #df = df[(df['altitude'] < df['q_high']) & (df['altitude'] > df['q_low'])]
        
        df['maxAltitudeFeet'] = df.groupby ( ['flight_id'] ) ['altitude']. transform('max')
        print ( list ( df ))
        print ( df.head(10) )
        
        print ("--- write the profile ---")
        fileName = "vertical_profile.csv"
        directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\Results"
        directory = Path(directoryPath)
        if directory.is_dir():
            print ( "it is a directory - {0}".format(directoryPath))
            filePath = os.path.join(directory, fileName)
            df.to_csv(filePath)
    
        print("--- written to vertical profile ---")
        
      
                
    