'''
Created on 19 oct. 2024

@author: robert
'''


from pyopensky.s3 import S3Client
 
 
if __name__ == '__main__':
 
    s3 = S3Client()
    for obj in s3.s3client.list_objects("submissions", recursive=True):
        print(f"{obj.bucket_name=}, {obj.object_name=}")
        
    