'''
Created on 16 juil. 2022

@author: robert
'''
from whitenoise.storage import CompressedManifestStaticFilesStorage

class MyWhiteNoiseStaticFilesStorage(CompressedManifestStaticFilesStorage):
    manifest_strict = False