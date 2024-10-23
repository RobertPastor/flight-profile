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
        print ( list ( df ) )
        
        flight_id = "258064118"
        ''' keep data for one flight id '''
        #df = df[df['flight_id'] == int ( flight_id ) ]
        print ( df['flight_id'].dtype )
        print ( list ( df ))
        #print ( df.head(10) )
        
        print ( df['flight_id'].nunique())
        #print ( df['altitude'].max(numeric_only=True))
        
        df_filtered = df.filter( items = ['flight_id'] ).drop_duplicates()
        
        '''
        print ("--- avg climb rate feet minutes---")
        df_avgClimbRate = df [ ( df['vertical_rate'] >= 0.0 ) ]
        print ( list ( df_avgClimbRate))
        df_avgClimbRate['avgClimbRateFeetMinutes'] = df_avgClimbRate.groupby ( ['flight_id'] , as_index=False ) ['vertical_rate'].transform('mean')
        df_avgClimbRate = df_avgClimbRate.filter( items = ['flight_id','avgClimbRateFeetMinutes'] ).drop_duplicates()
        print ( df_avgClimbRate.shape )
        print ( df_avgClimbRate.head( 10 ) )
        print ( df_avgClimbRate['flight_id'].nunique())
        
        print ("--- avg descent rate feet minutes---")
        df_avgDescentRate = df [ ( df['vertical_rate'] <= 0.0 ) ]
        print ( list ( df_avgDescentRate))
        df_avgDescentRate['avgDescentRateFeetMinutes'] = df_avgDescentRate.groupby ( ['flight_id'] , as_index=False ) ['vertical_rate'].transform('mean')
        df_avgDescentRate = df_avgDescentRate.filter( items = ['flight_id','avgDescentRateFeetMinutes'] ).drop_duplicates()
        print ( df_avgDescentRate.shape )
        print ( df_avgDescentRate.head( 10 ) )
        print ( df_avgDescentRate['flight_id'].nunique())
        '''
        
        print ("--- max Altitude feet ---")
    
        print(''' compute high and low outliers ''')
        df['altitude_high']  = df.groupby('flight_id' , as_index=False )['altitude'] .transform(q_high)
        df['altitude_low']  = df.groupby('flight_id' , as_index=False )['altitude'] .transform(q_low)
        
        print ( "--- filter outliers ---")
        df = df.loc[ (df['altitude'] < df['altitude_high']) ]
        df = df.loc[ (df['altitude'] > df['altitude_low']) ]
        print ( list ( df ))
        
        print ("--- compute max altitude ---")
            
        df['maxAltitudeFeet'] = df.groupby ( ['flight_id'] ) ['altitude']. transform('max')
        df_maxAltitude = df.filter( items = ['flight_id', 'maxAltitudeFeet' ] ).drop_duplicates()
        print ( df_maxAltitude.shape )
        print ( df_maxAltitude.head( 10 ))
            
        print ("--- merge in main dataframe ---")

        df_extended = df_filtered.merge ( df_maxAltitude  , how="left" , on="flight_id")
        print ( df_extended.shape )
        print ( list( df_extended ))
        print ( df_extended.head(10))
        
        print ("--- timestamp start ---")
        df['timestampStart'] = df.groupby ( ['flight_id'] ) ['timestamp']. transform('min')
        df_timeStampStart = df.filter( items = ['flight_id' , 'timestampStart']).drop_duplicates()

        print ( list ( df_timeStampStart ))
        print ( df_timeStampStart.head(10))

        print ("--- top of climb - delta time and position ---")
        ''' all records where altitude is near to the max altitude feet '''
        df_top_of_climb_descent = df.loc [ ( df['altitude'] > ( df['maxAltitudeFeet'] - 1000.0 ) ) & ( df['altitude'] < ( df['maxAltitudeFeet'] + 1000.0 ) ) ].sort_values(['timestamp'])
        print ( df_top_of_climb_descent.head(10) )
        
        #df_top_of_climb = df_top_of_climb.groupby ( ['flight_id'] )
        df_top_of_climb_descent = df_top_of_climb_descent.filter ( items = ['flight_id','timestamp','altitude'] ).drop_duplicates()
        print ( df_top_of_climb_descent.head(10) )
        
        print ( "--- get min of the timestamp - Top of Climb ---")
        
        df_top_of_climb_descent['topOfClimb'] = df_top_of_climb_descent.groupby(['flight_id'])['timestamp'].transform('min')
        print ( df_top_of_climb_descent )
        print ( list ( df_top_of_climb_descent))
        
        print ( "--- get max of the timestamp - Top of Descent ---")

        df_top_of_climb_descent['topOfDescent'] = df_top_of_climb_descent.groupby(['flight_id'])['timestamp'].transform('max')

        print (  df_top_of_climb_descent )
        print ( list ( df_top_of_climb_descent))
        print ( df_top_of_climb_descent.head(10))
        
        print ("--- filter the top of climb and top of descent timestamp ---")
        df_top_of_climb_descent = df_top_of_climb_descent.filter ( items = ['flight_id','topOfClimb','topOfDescent']).drop_duplicates()
        print ( list ( df_top_of_climb_descent ))
        print ( df_top_of_climb_descent.head(10))
        
        df_timeStampStart = df_timeStampStart.merge ( df_top_of_climb_descent, how='left' , on='flight_id')
        print ( list ( df_timeStampStart))
        print ( df_timeStampStart.head(10))
        
        print ("--- compute duration of climb ---")
        df_timeStampStart['timeToTopOfClimb'] = df_timeStampStart.apply(lambda row: ((row['topOfClimb']-row['timestampStart'])/pd.Timedelta(minutes=1)), axis=1)
        df_timeStampStart['timeTopOfClimbtoTopOfDescent'] = df_timeStampStart.apply(lambda row: ((row['topOfDescent']-row['topOfClimb'])/pd.Timedelta(minutes=1)), axis=1)
        
        print ( df_timeStampStart.head(10))
        print ("--- compute duration of cruise ---")

        
      
                
    