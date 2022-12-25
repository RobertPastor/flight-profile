'''
Created on 13 déc. 2022

@author: robert
'''

import os
import pandas as pd

HeaderNames = ["order" , "wayPoint", "latitude" , "longitude"]

class AirlineOneRouteReaderXlsx(object):

    def __init__(self):
        
        self.className = self.__class__.__name__
        self.FileNamePrefix = "AirlineRoute"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.sheetName = "WayPoints"
        
        
    def read(self, departureAirportICAO , arrivalAirportICAO ):
        
        self.fileName = self.FileNamePrefix + "-" + departureAirportICAO + "-" + arrivalAirportICAO + ".xlsx"
        print ( self.fileName )
        self.filePath = os.path.join( self.FilesFolder , self.fileName)
        if os.path.exists(self.filePath):
            print ( "file exists")
            df_source = pd.DataFrame(pd.read_excel(self.filePath, sheet_name=self.sheetName , engine="openpyxl"))
            for index, row in df_source.iterrows():
                print('Index is: {}'.format(index))
                print ("order is {0}".format(row["order"]))
                print ("wayPoint name is {0}".format(row["wayPoint"]))
                print ("latitude is {0}".format(row["latitude"]))
                print ("longitude is {0}".format(row["longitude"]))
                print ("----------- {0} -----------".format(row["order"]))
                
            return df_source
                
        else:
            print ("file does not exist")
            return None
            
        
        
if __name__ == '__main__':
    
    airlineOneRoute = AirlineOneRouteReaderXlsx()
    Adep = "KATL"
    Ades = "KBOS"
    airlineOneRoute.read(Adep,Ades)
    