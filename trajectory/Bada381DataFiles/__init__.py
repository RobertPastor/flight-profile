
import os

def getBadaFilePath():
    
    filePath = os.path.dirname(__file__)
    filePath = os.path.join( filePath , "."  )
    filePath = os.path.abspath( filePath )
    return filePath