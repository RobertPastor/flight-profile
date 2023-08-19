'''
Created on 9 oct. 2021

@author: robert

Read all AirlineRoute XLS files starting with AirlineRoute prefix

'''
import os
import pandas as pd


class AirlineRoutesReader(object):

    def __init__(self):
        
        self.className = self.__class__.__name__
        self.FileNamePrefix = "WayPoints"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )

    def read(self , Adep, Ades):
        pass
        self.sheetName = "WayPoints"
        self.FileName = self.FileNamePrefix + "-" + str(Adep).upper() + "-" + str(Ades).upper() + ".xlsx"
        print ( self.FileName )
        self.FilePath = os.path.abspath(self.FilesFolder + os.path.sep + self.FileName)
        
        ''' order wayPoint latitude longitude '''

        self.headers = []
        self.headers.append( "order" )
        self.headers.append( "wayPoint" )
        self.headers.append( "latitude" )
        self.headers.append( "longitude" )
        
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName, names=self.headers))
            
            npArray = df.to_numpy()
            for index, value in enumerate(npArray):
                print ( index, value )
            
            return npArray
        else:
            print ( "file is not existing = {0}".format(self.FilePath) )
        return None
    
    
    