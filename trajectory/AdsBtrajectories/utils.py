'''
Created on 15 oct. 2024

@author: robert
'''

import os
from pathlib import Path
import pandas as pd
from trajectory.AdsBtrajectories.Airports.AirportDatabaseFile import AirportsDatabase
from datetime import datetime
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer


DateFormatWithSlashes = '%d/%m/%Y'
DateFormatWithDashes = "%Y-%m-%d"

def readParquet(fileName):
    df = None
    print("Read parquet file")
    
    #fileName = "2022-01-01.parquet"
    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge"
    directory = Path(directoryPath)
    if directory.is_dir():
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directory, fileName)
        print ( filePath )
        df = pd.read_parquet ( filePath )
    return df


def readChallengeSet():
    df = None
    fileName = "challenge_set.csv"
    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge"
    directory = Path(directoryPath)
    if directory.is_dir():
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directory, fileName)
        print ( filePath )
        
        df = pd.read_csv ( filePath , sep = "," )
    return df


def readSubmissionSet():
    df = None
    print("Read submission set file")
    
    fileName = "submission_set.csv"
    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge"
    directory = Path(directoryPath)
    if directory.is_dir():
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directory, fileName)
        print ( filePath )
        
        df = pd.read_csv ( filePath , sep = "," )
    
    return df

def extractISOYear(dateStr):
    ''' 01/01/2024 '''
    if str(dateStr).find("-")>0:
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes)
    iso_year, iso_week, iso_weekday = date.isocalendar()
    return iso_year

def extractISOWeek(dateStr):
    ''' 01/01/2024 '''
    if str(dateStr).find("-")>0:
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes)
 
    iso_year, iso_week, iso_weekday = date.isocalendar()
    return iso_week

def extractISOWeekDay(dateStr):
    if str(dateStr).find("-")>0:
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes )
 
    iso_year, iso_week, iso_weekday = date.isocalendar()
    return iso_weekday

def extractMonth(dateStr):
    if str(dateStr).find("-")>0:
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes )
 
    return date.month

def oneHotEncoder(columnNameList):
    assert ( isinstance ( columnNameList , list ))
    transformer = make_column_transformer( (OneHotEncoder(), columnNameList ), remainder='passthrough')
    return transformer
    

def extendDataSetWithDates(df):
    
    if ( not df is None ) and ( isinstance(df , pd.DataFrame )):
        print ("--------- extend dataset with dates as integers -----")
        
        df['date_year'] = df.apply ( lambda row : extractISOYear( row['date']), axis=1)
        df['date_month'] = df.apply ( lambda row : extractMonth( row['date']), axis=1)
        df['date_week'] = df.apply ( lambda row : extractISOWeek( row['date']), axis=1)
        df['date_week_day'] = df.apply ( lambda row : extractISOWeekDay( row['date']), axis=1)
        ''' drop string date '''
        df = df.drop(columns=['date'])

    return df

def extendDataSetWithAirportData(df):
    if ( not df is None ) and ( isinstance(df , pd.DataFrame )):
        
        print ( "Read airports database ")
    
        airportsDatabase = AirportsDatabase()
        airportsDBOk = airportsDatabase.read()
        print ( airportsDBOk )
        if airportsDBOk:
        
            print ( "--- start adding adep ades informations ----")
            ''' create a new column '''
            df["adep_elevation_meters"] = df.apply(lambda row: airportsDatabase.getAirportElevationMeters(row['adep']), axis=1)
            df["ades_elevation_meters"] = df.apply(lambda row: airportsDatabase.getAirportElevationMeters(row['ades']), axis=1)
            
            df['adep_latitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLatitudeDegrees(row['adep']), axis=1)
            df['adep_longitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLongitudeDegrees(row['adep']), axis=1)
    
            df['ades_latitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLatitudeDegrees(row['ades']), axis=1)
            df['ades_longitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLongitudeDegrees(row['ades']), axis=1)
            
            #df['adep_ades_Nm'] = df.apply(lambda row: airportsDatabase.computeDistanceNm( row['adep'] , row['ades']), axis=1)
            
            print ("------- end adding adep ades informations ----------")
            columnsToDrop = ['ades', 'adep', 'name_adep', 'country_code_adep', 'name_ades' , 'country_code_ades']
            df = df.drop(columns=columnsToDrop)
            
            print ( list ( df ) )
        
    return df

def encodeCategoryColumn(df , columnNameToEncode):
    print ( "--- encode category column = {0}".format(columnNameToEncode))
    assert ( isinstance ( df , pd.DataFrame ))
    assert ( isinstance ( columnNameToEncode , str ))
    
    ohe = OneHotEncoder(handle_unknown='ignore')
    df_encoded = pd.DataFrame( ohe.fit_transform( df[[columnNameToEncode]] ).toarray() )
    print ( ohe.get_feature_names_out( ) )
    
    final_df = df.join( df_encoded )
    final_df = final_df.rename(columns=lambda x: columnNameToEncode + '_' + str(x) if str(x).isdigit() else x)
    
    final_df = final_df.drop(columns=[columnNameToEncode])
    print ( list ( final_df ) )

    print("---- encoding dataframe is finished ---")
    return ohe , df_encoded , final_df
