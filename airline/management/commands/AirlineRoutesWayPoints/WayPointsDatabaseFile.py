'''
Created on 13 sept. 2022

@author: robert
'''

import os
import pandas as pd
from numpy import isin


class WayPointsDatabase(object):
    WayPointsDict = {}
    ColumnNames = []
    className = ''
    sheetName = ""
    
    def __init__(self):
        self.className = self.__class__.__name__
        
        self.FileName = 'WayPoints.xlsx'  
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder + os.path.sep + self.FileName)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )

        self.WayPointsDict = {}
        self.ColumnNames = ["WayPoint", "Country", "Type", "Latitude", "Longitude" , "Name"]
        self.sheetName = "WayPoints"
        

    def getColumnNames(self):
        return self.ColumnNames


    def appendToDataFrame(self, df_source, wayPointName, Latitude, Longitude):
        ''' latitude and longitude are string here '''
        
        assert ( isinstance( df_source , pd.DataFrame) )
        assert isinstance(wayPointName, (str)) and len(wayPointName)>0
        assert isinstance(Latitude, (str)) and len(Latitude)>0
        assert isinstance(Longitude, (str)) and len(Longitude)>0
        
        wayPoint = {}
        wayPoint[self.ColumnNames[0]] = wayPointName
        wayPoint[self.ColumnNames[1]] = "Unknown"
        wayPoint[self.ColumnNames[2]] = "WayPoint"
        wayPoint[self.ColumnNames[3]] = Latitude
        wayPoint[self.ColumnNames[4]] = Longitude
        wayPoint[self.ColumnNames[5]] = "Unknown Name"
        df = pd.DataFrame(wayPoint, index=[0])
        
        return df_source.concat(df)
        

    def insertWayPoint(self, wayPointName, Latitude, Longitude):
        
        assert isinstance(wayPointName, (str)) and len(wayPointName)>0
        assert isinstance(Latitude, (str)) and len(Latitude)>0
        assert isinstance(Longitude, (str)) and len(Longitude)>0
        
        wayPoint = {}
        wayPoint[self.ColumnNames[0]] = wayPointName
        wayPoint[self.ColumnNames[1]] = "Unknown"
        wayPoint[self.ColumnNames[2]] = "WayPoint"
        wayPoint[self.ColumnNames[3]] = Latitude
        wayPoint[self.ColumnNames[4]] = Longitude
        wayPoint[self.ColumnNames[5]] = "Unknown Name"
        
        df = pd.DataFrame(wayPoint, index=[0])
        
        if os.path.exists(self.FilePath):
            df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName , engine="openpyxl"))
            if df_source is not None:
                df = df_source.append(df)
                
        df.to_excel(excel_writer=self.FilePath, sheet_name="WayPoints", index = False, columns=self.ColumnNames, engine="openpyxl")
        

    def exists(self):
        return os.path.exists(self.FilePath) and os.path.isfile(self.FilePath)
    
    
    def getDataFrame(self):
        df_source = None
        if os.path.exists(self.FilePath):
            df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName , engine="openpyxl"))
        return df_source
    
    
    def writeDataFrame(self, df_source):
        assert isinstance ( df_source , pd.DataFrame)
        df_source.to_excel(excel_writer=self.FilePath, sheet_name="WayPoints", index = False, columns=self.ColumnNames, engine="openpyxl")
        print ( "file = {0} created correctly".format( self.FilePath ))
    
    def writeDataFrameFromList(self, wayPointsList):
        df = pd.DataFrame(wayPointsList, columns=self.ColumnNames)
        df = df.drop_duplicates()
        self.writeDataFrame( df )
    
    
    def create(self):
        wayPoint = {}
        wayPoint[self.ColumnNames[0]] = "unknown"
        wayPoint[self.ColumnNames[1]] = "Unknown"
        wayPoint[self.ColumnNames[2]] = "WayPoint"
        wayPoint[self.ColumnNames[3]] = "0.0"
        wayPoint[self.ColumnNames[4]] = "0.0"
        wayPoint[self.ColumnNames[5]] = "Unknown Name"
        df = pd.DataFrame(wayPoint, index=[0])
        df.to_excel(excel_writer=self.FilePath, sheet_name="WayPoints", index = False, columns=self.ColumnNames, engine="openpyxl")

    
    def hasDuplicates(self):
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName))
            if df is not None:
                df_dupes = df.df.duplicated()
                if ( df_dupes is None ):
                    return False
                else:
                    return True
            else:
                return False
        else:
            return False
    
    
    def getNumberOfRows(self):
        if os.path.exists(self.FilePath):
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName, engine="openpyxl"))
            return df.shape[0]
        else:
            return 0
    
    
    def dropDuplicates(self):
        
        if self.exists():
            ''' get previous content '''
            df = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName, engine="openpyxl"))
            df = df.drop_duplicates()
            ''' delete old file '''
            os.remove(self.FilePath)
            ''' re create new file '''
            df.to_excel(excel_writer=self.FilePath, sheet_name=self.sheetName, index = False, columns=self.ColumnNames, engine="openpyxl")
            return True
        else:
            return False


