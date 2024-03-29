'''
Created on 8 avr. 2015

@author: PASTOR Robert

        Written By:
                Robert PASTOR 
                @Email: < robert [--DOT--] pastor0691 (--AT--) gmail [--DOT--] com >

        @http://trajectoire-predict.monsite-orange.fr/ 
        @copyright: Copyright 2015 Robert PASTOR 

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 3 of the License, or
        (at your option) any later version.
 
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
 
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.

@note: Read an XLSX file containing the runways

'''

import os
import json
import pandas as pd

from trajectory.models import AirlineRunWay, AirlineAirport


ColumnNames = ['id' , 'airport_ref', 'airport_ident' , 'length_ft' , 'width_ft' ,
              'surface' , 'lighted', 'closed', 
              'le_ident' , 'le_latitude_deg' , 'le_longitude_deg' , 
              'le_elevation_ft', 'le_heading_degT', 'le_displaced_threshold_ft' ,
              'he_ident' , 'he_latitude_deg' , 'he_longitude_deg' , 
              'he_elevation_ft' , 'he_heading_degT', 'he_displaced_threshold_ft' ]

FloatColumnNames = ['le_latitude_deg', 'le_longitude_deg', 'le_heading_degT', 
                                    'he_latitude_deg', 'he_longitude_deg', 'he_heading_degT' ,
                                    'length_ft']

IdentColumnNames = [ 'le_ident' , 'he_ident']
    
class RunWaysDatabase(object):
    FilePath = ''
    #runWaysDb = {}
    
    def __init__(self):
        self.className = self.__class__.__name__

        self.FilePath = "RunWays.xlsx"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        print ( self.className + ': file path= {0}'.format(self.FilePath) )

        #self.runWaysDb = {}
        self.sheetName = "RunWays"
        
        self.columnNames = ColumnNames
        self.floatColumnNames = FloatColumnNames
        self.identColumnNames = IdentColumnNames
        
    def exists(self):
        return os.path.exists(self.FilePath) and os.path.isfile(self.FilePath)
        
        
    def getInternalRunWays(self, rowValues):
        '''
        in one row there might be one or TWO run-ways
        '''
        #print ( 'id content= {0}'.format( rowValues[self.ColumnNames['id']] ) )
        #print ( type ( rowValues[self.ColumnNames['id']] ) )
        id_content = str( int ( rowValues['id'] ) )
        runwayDict = {}
        if len(id_content.strip())> 0:
                
            for column in self.columnNames:
                airportICAOcode = rowValues['airport_ident']
                #print ( airportICAOcode )
                if column == 'id':
                    runwayDict[column] = int(rowValues[column])
                        
                elif column in self.floatColumnNames:
                    ''' float values '''
                    if len(str(rowValues[column]).strip())>0:
                        runwayDict[column] = float(rowValues[column])
                    
                elif column in self.identColumnNames:
                    strRunwayName = str(rowValues[column]).strip().split('.')[0]
                    runwayDict[column] = strRunwayName
                    if str(strRunwayName).isdigit() and int(strRunwayName) < 10 and len(strRunwayName)==1:
                        runwayDict[column] = '0' + strRunwayName
                        
                else:
                    # string fields
                    runwayDict[column] = str(rowValues[column]).strip()
                    
            ''' we have transformed the row values into a Dictionary => now create the run-ways '''
            if (    len(str(rowValues['le_ident']).strip()) > 0 and
                    len(str(rowValues['airport_ident']).strip()) > 0 and
                    len(str(rowValues['length_ft']).strip()) > 0 and
                    len(str(rowValues['le_heading_degT']).strip()) > 0 and
                    len(str(rowValues['le_latitude_deg']).strip()) > 0 and
                    len(str(rowValues['le_longitude_deg']).strip()) > 0  and
                
                    len(str(rowValues['he_ident']).strip()) > 0 and
                    len(str(rowValues['airport_ident']).strip()) > 0 and
                    len(str(rowValues['length_ft']).strip()) > 0 and
                    len(str(rowValues['he_heading_degT']).strip()) > 0 and
                    len(str(rowValues['he_latitude_deg']).strip()) > 0 and
                    len(str(rowValues['he_longitude_deg']).strip()) > 0 ):
                   
                #print ( runwayDict['le_ident'] )
                #print ( runwayDict['he_ident'] )
                #print ( runwayDict['airport_ident'])
                '''
                print ( runwayDict['length_ft'] )
                print ( runwayDict['le_heading_degT'] )
                print ( runwayDict['le_latitude_deg'] )
                print ( runwayDict['le_longitude_deg'] )
                
                print ( runwayDict['he_ident'] )
                print ( runwayDict['airport_ident'] )
                print ( runwayDict['length_ft'] )
                print ( runwayDict['he_heading_degT'] )
                print ( runwayDict['he_latitude_deg'] )
                print ( runwayDict['he_longitude_deg'] )
                '''
                
                return runwayDict
            else:
                raise ValueError( json.dumps( runwayDict) )
        return runwayDict
    
        
    def hasRunWays(self, airportICAOcode):
        
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                return True
        return False
 
 
    def getRunWaysAsDict(self, airportICAOcode):
        
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        
        runwaysDict = {}
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                runwaysDict.update(self.getInternalRunWays(rowValues))
        
        return runwaysDict        


    def getRunWays(self, airportICAOcode):
        
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        
        runwaysDict = self.getRunWaysAsDict(airportICAOcode)
        
        for runway in runwaysDict.values():
            yield runway
            
        
    def findAirportRunWays(self, airportICAOcode , runwayLengthFeet = 0.0):
        ''' returns a dictionary with run-ways '''
        ''' assert there is only one sheet '''
        assert not(self.sheet is None)
        assert (isinstance(airportICAOcode, str)) and len(airportICAOcode)>0
        #print self.className + ': find runways for airport= {0}'.format(airportICAOcode)
        runwaysDict = {}
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if runwayLengthFeet > 0.0:
                if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode) and (rowValues[self.ColumnNames['length_ft']] > runwayLengthFeet):
                    runwaysDict.update(self.getInternalRunWays(rowValues))

            else:
                if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                    runwaysDict.update(self.getInternalRunWays(rowValues))
        return runwaysDict
        
        
    def read(self, airlineRoutesAirportsList):
        
        print (self.FilePath)
        assert len(self.FilePath)>0 and os.path.isfile(self.FilePath) 
        
        df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName , engine="openpyxl"))

        for index, row in df_source.iterrows():
            
            #print('Index is: {}'.format(index))
            #print('Row airport = {0} '.format( row['airport_ident']))
            ''' reading a row with runways '''
            runwayDict = self.getInternalRunWays(row)
            
            if ( "airport_ident" in runwayDict ) and ( runwayDict['airport_ident'] in airlineRoutesAirportsList ):
                    
                    print ( runwayDict['airport_ident'] )
                    airport = AirlineAirport.objects.filter(AirportICAOcode = runwayDict['airport_ident']).first()
                    if ( airport ):
                        print ("airport = {0}".format(runwayDict['airport_ident']))
                        ''' some airports have only one run-way '''
                        if ( len(runwayDict['le_ident']) > 0 ) and airport:
                            
                            runWay = AirlineRunWay ( 
                                Name               = runwayDict['le_ident'],
                                Airport            = airport,
                                LengthFeet         = runwayDict['length_ft'],
                                TrueHeadingDegrees = runwayDict['le_heading_degT'],
                                LatitudeDegrees    = runwayDict['le_latitude_deg'],
                                LongitudeDegrees   = runwayDict['le_longitude_deg']
                                )
                            print ( runWay )
                            runWay.save()
                            
                        if ( len(runwayDict['he_ident']) > 0 ) and airport:
                            
                            runWay = AirlineRunWay ( 
                                Name = runwayDict['he_ident'],
                                Airport = airport,
                                LengthFeet = runwayDict['length_ft'],
                                TrueHeadingDegrees = runwayDict['he_heading_degT'],
                                LatitudeDegrees = runwayDict['he_latitude_deg'],
                                LongitudeDegrees = runwayDict['he_longitude_deg']
                                )
                            runWay.save()
                    else:
                        raise ValueError( "airport not found = {0}".format( ))
                
        return True
    
    
    def __str__(self):
        print ( self.className + ':RunWay DataBase= {0}'.format(self.FilePath) )
        
        
    def getFilteredRunWays(self, airportICAOcode, runwayName = ''):
        assert not(airportICAOcode is None) 
        assert isinstance(airportICAOcode, (str)) 
        assert (len(airportICAOcode)>0)
        #print self.className + ': query for airport= {0} and runway= {1}'.format(airportICAOcode, runwayName)
        assert not(self.sheet is None)
        runwaysDict = {}
        for row in range(self.sheet.nrows): 
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if (rowValues[self.ColumnNames['airport_ident']] == airportICAOcode):
                runwaysDict.update(self.getInternalRunWays(rowValues))
        if runwayName in runwaysDict:
            return runwaysDict[runwayName]
        else:
            ''' return arbitrary chosen first run-way '''
            return runwaysDict.get(list (runwaysDict)[0])
        
        
    def __getitem__(self, key):
        if key in self.runWaysDb.keys():
            return self.runWaysDb[key]
        else:
            return None
            
    
