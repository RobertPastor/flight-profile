'''
Created on 24 déc. 2022

@author: robert
'''

import os

from trajectory.models import AirlineWayPoint
import pandas as pd
from trajectory.views.utils import convertDegreeMinuteSecondToDecimal

fieldNames = ['WayPoint', 'Country' , 'Type', 'Latitude', 'Longitude' , 'Name']




class WayPointsDatabaseXlsx(object):
    WayPointsDict = {}
    ColumnNames = []
    className = ''
    
    def __init__(self):
        self.className = self.__class__.__name__
        
        self.FilePath = 'WayPoints.xlsx'  
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder + os.path.sep + self.FilePath)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )

        self.WayPointsDict = {}
        self.ColumnNames = {}
        
        self.sheetName = "WayPoints"

    def exists(self):
        return os.path.exists(self.FilesFolder) and os.path.isfile(self.FilePath)
    
    
    def read(self):
        assert len(self.FilePath)>0
        
        if self.exists():
            df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName , engine="openpyxl"))
            
            for index, row in df_source.iterrows():
                print('Index is: {}'.format(index))
                print('ID is: {} - WayPoint is: {} - Latitude = {} - Longitude = {}'.format(index, row['WayPoint'], row['Latitude'], row['Longitude']))
                
                WayPointName = str(row['WayPoint']).strip().upper()
                if not(WayPointName in self.WayPointsDict.keys()):
                    
                    strLatitude = str(row['Latitude']).strip()
                    strLongitude = str(row['Longitude']).strip()
                    
                    wayPointDict = {}
                    wayPointDict["WayPoint"] = WayPointName
                    
                    if '°' in strLatitude:
                        strLatitude = str(strLatitude).replace('°','-')
        
                        strLatitude = str(strLatitude).strip().replace("'", '-').replace(' ','').replace('"','')
                        wayPointDict["Latitude"] = convertDegreeMinuteSecondToDecimal(strLatitude)
                        
                    if '°' in strLongitude:
                        strLongitude = str(strLongitude).replace('°','-')
        
                        strLongitude = str(strLongitude).strip().replace("'", '-').replace(' ','').replace('"','')
                        wayPointDict["Longitude"] = convertDegreeMinuteSecondToDecimal(strLongitude)
    
                    self.WayPointsDict[WayPointName] = self.WayPointsDict
                    
                    ''' create a way point '''    
                    Continent = 'unknown'
                    if (wayPointDict['Latitude'] >= 20. and wayPointDict['Longitude'] >= -170. and wayPointDict['Longitude'] < -50.):
                        Continent = 'North America'
                    if (wayPointDict['Latitude'] >= 35. and wayPointDict['Longitude'] >= -50. and wayPointDict['Longitude'] < 50.):
                        Continent = 'Europe'
                    if (wayPointDict['Latitude'] >= 5. and wayPointDict['Longitude'] >= 50. and wayPointDict['Longitude'] < 90.):
                        Continent = 'India'
                    wayPoint = AirlineWayPoint(WayPointName = wayPointDict['WayPoint'],
                                            Type = 'WayPoint',
                                            Continent = Continent,
                                            Latitude = wayPointDict['Latitude'],
                                            Longitude = wayPointDict['Longitude'])
                    print ( str ( wayPoint ))
                    wayPoint.save()
                
                else:
                    print ("duplicates found in Way Points database - way Point= {0}".format(WayPointName))
                    return False
            
            return True
        else:
            return False
                    
