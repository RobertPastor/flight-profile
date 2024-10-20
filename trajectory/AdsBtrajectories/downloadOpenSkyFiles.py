'''
Created on 13 oct. 2024

@author: robert
'''

import os
from pyopensky.config import opensky_config_dir
from pyopensky.s3 import S3Client
from pathlib import Path
from calendar import Calendar, monthrange
from datetime import date

from sqlalchemy.sql._elements_constructors import true, false
from test.test_decimal import directory

''' https://ansperformance.eu/study/data-challenge/ '''

def date_iter( year, month):
    for i in range(1, monthrange(year, month)[1]  + 1):
        yield date(year, month, i)
        

def isParquetFileNameToDownloadOld( yearInt, monthInt, s3FileName):
    
    found = False
    for i in range(1, monthrange(yearInt, monthInt)[1]  + 1):
        d = date(yearInt, monthInt, i)
        #print(str( d ))
        fileName = str(d) + "." + "parquet"
        if ( fileName == s3FileName):
            return True
    return found

def isParquetFileNameToDownload( yearInt, s3FileName ):
    found = False
    for monthInt in range(2,5):
        for dayInt in range(1 , 8):
            d = date(yearInt, monthInt, dayInt)
            fileName = str(d) + "." + "parquet"
            if ( fileName == s3FileName):
                return True
    return found
        
    

if __name__ == '__main__':
    #['01','02','03','04','05','06','07'] 
    
    print(opensky_config_dir)
    calendar = Calendar()

    s3 = S3Client()
    yearInt = 2022
    
    for obj in s3.s3client.list_objects("competition-data", recursive=True):
            #print(f"{obj.bucket_name=}, {obj.object_name=}")
            #s3.download_object(obj)
            if str(obj.object_name).endswith("parquet") :
                print ( f"{obj.object_name=}" )
                '''
                if ( isParquetFileNameToDownload( yearInt, str(obj.object_name) ) ):
                
                    print ( "--- start downloading - {0}".format( str(obj.object_name) ))
                    directoryPath = "C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge"
                    directory = Path(directoryPath)
                    if directory.is_dir():
                        #print ( "it is a directory - {0}".format(directoryPath))
                        filePath = os.path.join(directoryPath, str(obj.object_name) )
                        print ("download "+str(obj.object_name))
    
                        #s3.download_object(obj=obj, filename=directory)
                '''
            else:
                if str(obj.object_name).endswith("csv"):
                    print ( f"{obj.object_name=}" )
                    file = Path("C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge")
                    s3.download_object(obj=obj, filename=file)

            
        