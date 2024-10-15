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
    first = False

    for obj in s3.s3client.list_objects("competition-data", recursive=True):
        #print(f"{obj.bucket_name=}, {obj.object_name=}")
        #s3.download_object(obj)
        if str(obj.object_name).endswith("parquet") and first == True:
            print ( f"{obj.object_name=}" )
            first = False
            file = Path("C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge")
            #s3.download_object(obj=obj, filename=file)
            
        else:
            if str(obj.object_name).endswith("csv"):
                print ( f"{obj.object_name=}" )
                file = Path("C:\\Users\\rober\\git\\flight-profile\\trajectory\\AdsBtrajectories\\AnsPerformanceChallenge")
                s3.download_object(obj=obj, filename=file)

            
        