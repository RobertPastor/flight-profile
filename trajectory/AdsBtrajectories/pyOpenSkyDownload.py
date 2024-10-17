'''
Created on 13 oct. 2024

@author: robert
'''

from pyopensky.config import opensky_config_dir
from pyopensky.s3 import S3Client
from pathlib import Path

''' https://ansperformance.eu/study/data-challenge/ '''

if __name__ == '__main__':
    
    print(opensky_config_dir)

    s3 = S3Client()

    for obj in s3.s3client.list_objects("competition-data", recursive=True):
        #print(f"{obj.bucket_name=}, {obj.object_name=}")
        #s3.download_object(obj)
        if str(obj.object_name).endswith("parquet") :
            print ( f"{obj.object_name=}" )
            file = Path("C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge")
            strFileNameDay = str ( str(obj.object_name).split(".")[0] ).split("-")[2]
            print ( strFileNameDay )
            if not ( strFileNameDay in ['01','02','03','04','05','06','07'] ):
                print ( "--- start downloading - {0}".format( str(obj.object_name) ))
                s3.download_object(obj=obj, filename=file)
            
        else:
            if str(obj.object_name).endswith("csv"):
                print ( f"{obj.object_name=}" )
                file = Path("C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge")
                #s3.download_object(obj=obj, filename=file)

            
        