'''
Created on 24 déc. 2022

@author: robert
'''

import os

from trajectory.models import AirlineWayPoint
import pandas as pd


fieldNames = ['WayPoint', 'Country' , 'Type', 'Latitude', 'Longitude' , 'Name']

def convertDegreeMinuteSecondToDecimal(DegreeMinuteSecond='43-40-51.00-N'):
    '''
        convert from Decimal Degrees = Degrees + minutes/60 + seconds/3600
        to float
        mays start or end with NE SW
    '''
    DecimalValue = 0.0
    coeff = 0.0
    assert isinstance(DegreeMinuteSecond, str) 
        
    if ( str(DegreeMinuteSecond).endswith("N") or 
         str(DegreeMinuteSecond).endswith("E") or 
         str(DegreeMinuteSecond).startswith("N") or 
         str(DegreeMinuteSecond).startswith("E") ):
        ''' transform into decimal value '''
        coeff = 1.0
        
    elif ( str(DegreeMinuteSecond).endswith("S") or 
           str(DegreeMinuteSecond).endswith("W") or
           str(DegreeMinuteSecond).startswith("S") or 
           str(DegreeMinuteSecond).startswith("W") ):
        ''' transform into decimal value '''
        coeff = -1.0
    
    else :
        raise ValueError ('Degrees Minutes Seconds string should be starting or ending by N-E-S-W')
    
    if  ( str(DegreeMinuteSecond).endswith("N") or 
          str(DegreeMinuteSecond).endswith("E") or 
          str(DegreeMinuteSecond).endswith("S") or 
          str(DegreeMinuteSecond).endswith("W") ):
        ''' suppress last char and split '''
        strSplitList = str(DegreeMinuteSecond[:-1]).split('-')
    else:
        ''' suppress first char and split '''
        strSplitList = str(DegreeMinuteSecond[1:]).split('-')

    #print strSplitList[0]
    if str(strSplitList[0]).isdigit() and str(strSplitList[1]).isdigit():
        DecimalDegreeValue = int(strSplitList[0])
        DecimalMinutesValue = int(strSplitList[1])
        #print strSplitList[1]
        strSplitList2 = str(strSplitList[2]).split(".")
        #print strSplitList2[0]
        if (len(strSplitList2)==2 and str(strSplitList2[0]).isdigit() and str(strSplitList2[1]).isdigit()):
                
            DecimalSecondsValue = int(strSplitList2[0])
            TenthOfSecondsValue = int(strSplitList2[1])
            
            DecimalValue = DecimalDegreeValue + float(DecimalMinutesValue)/float(60.0)
            DecimalValue += float(DecimalSecondsValue)/float(3600.0)
            if TenthOfSecondsValue < 10.0:
                DecimalValue += (float(TenthOfSecondsValue)/float(3600.0)) / 10.0
            else:
                ''' two digits of millis seconds '''
                DecimalValue += (float(TenthOfSecondsValue)/float(3600.0)) / 100.0
                    
            DecimalValue = coeff * DecimalValue
        else:
            raise ValueError ('unexpected Degrees Minutes Seconds format')
    else:
        raise ValueError ('unexpected Degrees Minutes Seconds format')

    #print "DegreeMinuteSecond= ", DegreeMinuteSecond, " DecimalValue= ", DecimalValue
    return DecimalValue


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
                    
                    
                    strLatitude = (row['Latitude']).strip()
                    strLongitude = (row['Longitude']).strip()
                    
                    wayPointDict = {}
                    wayPointDict["WayPoint"] = WayPointName
                    
                    if '°' in strLatitude:
                        strLatitude = (strLatitude).replace('°','-')
        
                        strLatitude = str(strLatitude).strip().replace("'", '-').replace(' ','').replace('"','')
                        wayPointDict["Latitude"] = convertDegreeMinuteSecondToDecimal(strLatitude)
                        
                    if '°' in strLongitude:
                        strLongitude = (strLongitude).replace('°','-')
        
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
                    
