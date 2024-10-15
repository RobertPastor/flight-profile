'''
Created on 15 oct. 2024

@author: robert
'''

import os
from pathlib import Path
import pandas as pd
from trajectory.AdsBtrajectories.Airports.AirportDatabaseFile import AirportsDatabase
from datetime import datetime

DateFormatWithSlashes = '%d/%m/%Y'
DateFormatWithDashes = "%Y-%m-%d"

def readChallengeSet():
    
    df = None
    
    fileName = "challenge_set.csv"
    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge"
    directory = Path(directoryPath)
    if directory.is_dir():
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directory, fileName)
        print ( filePath )
        
        df = pd.read_csv ( filePath , sep = ";" )
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
    if str(dateStr).find("-"):
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes)
    iso_year, iso_week, iso_weekday = date.isocalendar()
    return iso_year

def extractISOWeek(dateStr):
    ''' 01/01/2024 '''
    if str(dateStr).find("-"):
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes)
 
    iso_year, iso_week, iso_weekday = date.isocalendar()
    return iso_week

def extractISOWeekDay(dateStr):
    if str(dateStr).find("-"):
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes )
 
    iso_year, iso_week, iso_weekday = date.isocalendar()
    return iso_weekday

def extractMonth(dateStr):
    if str(dateStr).find("-"):
        date = datetime.strptime(dateStr, DateFormatWithDashes )
    else:
        date = datetime.strptime(dateStr, DateFormatWithSlashes )
 
    return date.month

def encodeStringToASCIIdigits(inputStr):
    outputStr =  ''.join(str(ord(c)) for c in inputStr)
    if str(outputStr).isdigit():
        return int(outputStr)

def extendDataSetWithDates(df):
    if ( not df is None ) and ( isinstance(df , pd.DataFrame )):
        
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
            
            print ("------- end adding adep ades informations ----------")
            columnsToDrop = ['ades','adep', 'name_adep', 'country_code_adep', 'name_ades' , 'country_code_ades']
            df = df.drop(columns=columnsToDrop)
            
            print ( list ( df ) )
        
    return df