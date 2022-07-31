'''
Created on 29 août 2021

@author: robert
'''

import os
import logging

from xlrd import open_workbook
from airline.models import AirlineAircraft

''' in service means number of available aircrafts '''
HeaderNames = ['Aircraft' , 'In service', 'Orders' , 'Passengers Delta One', 'Passengers First Class', 'Passengers Premium Select' ,
               'Passengers Delta Confort Plus' , 'Passengers Main Cabin' , 'Passengers Total' , 'Costs per flying hours dollars', 'Refs', 'Notes']


class AirlineFleetDataBase(object):
    FilePath = ''
    
    ''' list of class AirlineAircraft '''
    FleetAircrafts = []
    
    def __init__(self):
        self.className = self.__class__.__name__
        self.FilePath = "AirlineFleet.xls"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        logging.info ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        logging.info ( self.className + ': file path= {0}'.format(self.FilePath) )
        
        
    def exists(self):
        return os.path.exists(self.FilePath) 


    def read(self, badaAircraftDatabase):
        ''' this method reads the whole file - not only the headers '''
        logging.info (self.FilePath)
        assert len(self.FilePath)>0 and os.path.isfile(self.FilePath) 
        book = open_workbook(self.FilePath, formatting_info=True)
        ''' assert there is only one sheet '''
        self.sheet = book.sheet_by_index(0)
        #logging.info ( 'Sheet contains - number of rows = {0}'.format(self.sheet.nrows))
        for row in range(self.sheet.nrows):
            #logging.info ( '--> row --> {0}'.format(row) )
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if row == 0:
                self.ColumnNames = {}
                index = 0
                for column in rowValues:
                    if column not in HeaderNames:
                        logging.info ( self.className + ': ERROR - expected Fleet column name= {0} not in Header names'.format(column) )
                        return False
                    else:
                        self.ColumnNames[column] = index
                    index += 1

            else:
                #logging.info ( str(row) )
                index = 0
                aircraftFullName = ""
                nbAvailableAircrafts = 0
                nbMaxPassengers = 0
                costsFlyingDollars = 0
                for cell in rowValues:
                    if index == 0:
                        if len(str(cell))>0:
                            #logging.info ( cell )
                            aircraftFullName = str(cell).strip()
                        index = index + 1
                    else:
                        if (HeaderNames[index] == "In service"):
                            if len (str(cell).strip()) > 0 :
                                #logging.info ( str(cell).strip() )
                                #logging.info ( type ( str(cell).strip() ) )
                                nbAvailableAircrafts = float(str(cell).strip())
                                nbAvailableAircrafts = int ( nbAvailableAircrafts )
                            
                        if (HeaderNames[index] == "Passengers Total"):
                            if len (str(cell).strip()) > 0 :
                                #logging.info ( str(cell).strip() )
                                nbMaxPassengers = float(str(cell).strip())
                                nbMaxPassengers = int ( nbMaxPassengers )

                        if (HeaderNames[index] == "Costs per flying hours dollars"):
                            if len (str(cell).strip()) > 0 :
                                #logging.info ( cell )
                                assert ( type (str(cell).strip() == float ))
                                costsFlyingDollars = float( str(cell).strip() )
                            
                        index = index + 1
                        
                ''' one ac per row '''
                aircraftICAOcode = badaAircraftDatabase.getAircraftICAOcode(aircraftFullName)
                logging.info ( aircraftFullName )
                print ( aircraftFullName )
                if (aircraftICAOcode):
                    logging.info ("aircraft ICAO code found = {0} for aircraft full name = {1}".format(aircraftICAOcode, aircraftFullName))
                    airlineAircraft = AirlineAircraft( 
                        aircraftICAOcode = aircraftICAOcode, 
                        aircraftFullName = aircraftFullName, 
                        numberOfAircraftsInService = nbAvailableAircrafts, 
                        maximumOfPassengers = nbMaxPassengers, 
                        costsFlyingPerHoursDollars = costsFlyingDollars)
                    airlineAircraft.save()
                    self.FleetAircrafts.append( airlineAircraft )
                
        return True
    
    
    def removeAircrafts(self, listOfFullNames):
        index = 0
        ''' use a copy '''
        for airlineAircraft in list ( self.FleetAircrafts ):
            logging.info ( airlineAircraft.getAircraftFullName() )
            for acFullName in listOfFullNames:
                if acFullName == airlineAircraft.getAircraftFullName():
                    logging.info ( "aircraft found -> {0}".format( acFullName ) )

                    self.FleetAircrafts.pop(index)
                    break
                    
            index = index + 1

    
    def dump(self):
        for aircraft in self.FleetAircraftTypes:
            logging.info ( 'fleet aircraft type -> {0}'.format( aircraft ))
                
    def getAirlineAircrafts(self):
        for airlineAircraft in self.FleetAircrafts:
            assert( isinstance( airlineAircraft, AirlineAircraft ) )
            yield airlineAircraft
            
    def getAircraftNumberOfInstances(self, aircraftICAOcode):
        nbAvailable = 0
        for airlineAircraft in self.FleetAircrafts:
            assert( isinstance( airlineAircraft, AirlineAircraft ) )
            if ( airlineAircraft.getAircraftICAOcode() == aircraftICAOcode ):
                nbAvailable = airlineAircraft.getNumberOfAircraftInstances()
                
        return nbAvailable
    
        