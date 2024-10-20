'''
Created on 13 oct. 2024

@author: robert

'''
import os
from pathlib import Path
import pandas as pd
from calendar import Calendar, monthrange

''' https://ansperformance.eu/study/data-challenge/ '''

from trajectory.AdsBtrajectories.utils import readParquet
from datetime import date

def q_low(x):
    return x.quantile(0.25)

def q_high(x):
    return x.quantile(0.75)

def date_iter( year, month):
    for i in range(1, monthrange(year, month)[1]  + 1):
        yield date(year, month, i)

def extendedOneDayParquet(df):
    
    print (list (df))
    print ("number of rows = {0}".format (len(df.index)))
    print (df.shape)
            
    unique_flight_ids = df['flight_id'].nunique()
    print("number of unique flight ids = {0}".format(unique_flight_ids))
    
    df_filtered = df.filter( items = ['flight_id'] ).drop_duplicates()
    print ("--- max Altitude feet ---")
    
    print(''' compute high an low outliers ''')
    df['altitude_high']  = df.groupby('flight_id' , as_index=False )['altitude'] .transform(q_high)
    df['altitude_low']  = df.groupby('flight_id' , as_index=False )['altitude'] .transform(q_low)
    
    print ( "--- filter outliers ---")
    df = df.loc[ df['altitude'] < df['altitude_high'] ]
    df = df.loc[ df['altitude'] > df['altitude_low'] ]
        
    df['maxAltitudeFeet'] = df.groupby ( ['flight_id'] ) ['altitude']. transform('max')
    df_maxAltitude = df.filter( items = ['flight_id', 'maxAltitudeFeet'] ).drop_duplicates()
    print ( df_maxAltitude.shape )
    print ( df_maxAltitude.head( 10 ))
            
    df_extended = df_filtered.merge ( df_maxAltitude  , how="left" , on="flight_id")
    print ( df_extended.shape )
    print ( list( df_extended ))
    print ( df_extended.head(10))
    
    print ("--- max Climb Rate Feet Minutes ---")
            
    df['maxClimbRateFeetMinutes'] = df.groupby ( ['flight_id'] , as_index=False ) ['vertical_rate'] . transform('max')
    df_maxClimbRate = df.filter( items = ['flight_id','maxClimbRateFeetMinutes'] ).drop_duplicates()
    print ( df_maxClimbRate.shape )
    print ( df_maxClimbRate.head( 10 ))
            
    df_extended = df_extended.merge( df_maxClimbRate , how='left' , on='flight_id')
    print ( df_extended.shape )
    print ( list( df_extended ))
    print ( df_extended.head(10))
            
    df['maxDescentRateFeetMinutes'] = df.groupby( ['flight_id'] , as_index=False ) ['vertical_rate'].transform('min')
    df_maxDescentRate = df.filter( items = ['flight_id','maxDescentRateFeetMinutes'] ).drop_duplicates()
    print ( df_maxDescentRate.shape )
    print ( df_maxDescentRate.head( 10 ))
            
    df_extended = df_extended.merge( df_maxDescentRate , how='left' , on='flight_id')
    print ( df_extended.shape )
    print ( list( df_extended ))
    print ( df_extended.head(10))
            
    df['avgGroundSpeedKnots'] = df.groupby( ['flight_id'] , as_index=False ) ['groundspeed'].transform('mean')
    df_avgGroundSpeed = df.filter(items=['flight_id','avgGroundSpeedKnots']).drop_duplicates()
    print ( df_avgGroundSpeed.head( 10 ))
            
    df_extended = df_extended.merge( df_avgGroundSpeed , how='left' , on='flight_id')
    print ( df_extended.shape )
    print ( list( df_extended ))
    
    df['maxGroundSpeedKnots'] = df.groupby( ['flight_id'] , as_index=False ) ['groundspeed'].transform('max')
    df_maxGroundSpeed = df.filter(items=['flight_id','maxGroundSpeedKnots']).drop_duplicates()
    print ( df_maxGroundSpeed.head( 10 ))
            
    df_extended = df_extended.merge( df_maxGroundSpeed , how='left' , on='flight_id')
    print ( df_extended.shape )
    print ( list( df_extended ))
    
    print(''' --- filter not a number in final dataframe ''')
    df_extended.fillna(df_extended.mean(), inplace=True)
    print ( df_extended.head(10))
        
    return df_extended
        
def extendUsingParquets(testMode=False):
    
    calendar = Calendar()
    first = True
    df_final = None
    yearInt = 2022
    
    if ( testMode == True ):
        theDate = date(yearInt, 1, 1)
        fileName = str(theDate) + "." + "parquet"
        return extendedOneDayParquet(readParquet(fileName))
    
    for iMonth in range(1,13):
        for d in date_iter( yearInt, iMonth):
            print(str( d ))
            fileName = str(d) + "." + "parquet"
        
            df = readParquet(fileName)
            if not df is None:
                if first == True:
                    df_final = extendedOneDayParquet(df)
                    first = False
                else:
                    df_extended = extendedOneDayParquet(df)
                    ''' ignore_index = True auto generate a new index '''
                    df_final = pd.concat ( [df_final , df_extended] , ignore_index=True)

    return df_final


if __name__ == '__main__':
    
    testMode = False
    df_final = extendUsingParquets(testMode)
    
    fileName = 'extendedOpenSky.parquet'
    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\Results"
    directory = Path(directoryPath)
    if directory.is_dir():
            print ( "it is a directory - {0}".format(directoryPath))
            filePath = os.path.join(directory, fileName)
            df_final.to_parquet(filePath)
                                        
    print("--- its all finished ---")
    print ( df_final.shape )
    print ( list ( df_final ))
    print ( df_final.head(100))

