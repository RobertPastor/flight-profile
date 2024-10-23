'''
Created on 20 oct. 2024

@author: robert
'''

import os
from trajectory.AdsBtrajectories.utils import readSubmissionSet
from pathlib import Path

import pandas as pd

if __name__ == '__main__':
    
    fileName = "final_submission_set.csv"
    df_submission = readSubmissionSet(fileName)
    print ( list ( df_submission ) )
    print( df_submission.shape )
    print ( df_submission.head())
    
    df_submission.drop(columns=['tow'], inplace=True)
    print ( df_submission.head())
    
    print ( "number of rows = {0}".format ( len(df_submission.index) ) )
    df_final_submission_nb_rows = len(df_submission.index)
    
    inputFileName = "final_team_submission_21-Oct-2024-11h28m52.csv"
    inputFileName = "final_team_submission_21-Oct-2024-17h00m15.csv"
    inputFileName = "final_team_submission_21-Oct-2024-18h19m57.csv"
    inputFileName = "final_team_submission_21-Oct-2024-22h33m22.csv"
    inputFileName = "final_team_submission_22-Oct-2024-22h20m05.csv"

    outputResultsFolder = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\Results"
    directoryPath = Path(outputResultsFolder)
    if directoryPath.is_dir():
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directoryPath, inputFileName)
        df_Tow = pd.read_csv ( filePath , sep = "," )
        
        df_Tow.rename(columns={'0': 'tow'}, inplace=True)
        
        print ( list ( df_Tow ) )
        print( df_Tow.shape )
        print ( df_Tow.head())
        
        print ( "number of rows = {0}".format ( len(df_Tow.index) ) )
        Team_Submission_nb_rows = len(df_Tow.index)
        
    assert ( df_final_submission_nb_rows == Team_Submission_nb_rows)

    final_submission_with_TOW_df = pd.merge( df_submission, df_Tow, left_index=True, right_index=True)
    
    for column in ['date', 'callsign', 'adep', 'name_adep', 'country_code_adep', 'ades', 'name_ades', 'country_code_ades', 'actual_offblock_time', 'arrival_time', 'aircraft_type', 'wtc', 'airline', 'flight_duration', 'taxiout_time', 'flown_distance']:
        final_submission_with_TOW_df.drop(columns=[column], inplace=True)
        
    final_submission_with_TOW_df = final_submission_with_TOW_df.dropna()
    
    print ( list ( final_submission_with_TOW_df ) )
    print( final_submission_with_TOW_df.shape )
    print ( final_submission_with_TOW_df.head())
    
    teamId = "f8afb85a-8f3f-4270-b0bd-10f9ba83adf4"
    teamName = "team_exuberant_hippo"
    version = "v7"
    outputFileName = teamName + "_" + version + "_" + teamId + ".csv"
    
    outputResultsFolder = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\Results"
    directoryPath = Path(outputResultsFolder)
    if directoryPath.is_dir():
        print ( "it is a directory - {0}".format(directoryPath))
        filePath = os.path.join(directoryPath, outputFileName)
        print ( filePath )
        final_submission_with_TOW_df.to_csv(filePath, sep="," , header=True, index=False)
    
    

        
        
        
    
    