'''
Created on 1 sept. 2021

@author: robert PASTOR
'''
import os
import logging 

from xlrd import open_workbook
from airline.models import AirlineRoute

HeaderNames = ["Departure Airport", "Departure Airport ICAO Code", "Arrival Airport", "Arrival Airport ICAO Code"]

class AirlineRoutesDataBase(object):
    FilePath = ''
    RoutesAirports = []

    def __init__(self):
        self.className = self.__class__.__name__

        self.FilePath = "AirlineRoutesAirportsDepartureArrival.xls"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        logging.info ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        logging.info ( self.className + ': file path= {0}'.format(self.FilePath) )
        
    def exists(self):
        return os.path.exists(self.FilePath) 
    
    def read(self):
        ''' this method reads the whole dataset file - not only the headers '''
        logging.info (self.FilePath)
        assert len(self.FilePath)>0 and os.path.isfile(self.FilePath) 
        
        book = open_workbook(self.FilePath, formatting_info=True)
        ''' assert there is only one sheet '''
        self.sheet = book.sheet_by_index(0)
        #logging.info ( self.className + ' Sheet contains - number of rows = {0}'.format(self.sheet.nrows))
        for row in range(self.sheet.nrows):
            #logging.info ( '--> row --> {0}'.format(row) )
            rowValues = self.sheet.row_values(row, start_colx=0, end_colx=self.sheet.ncols)
            if row == 0:
                ''' header row '''
                self.ColumnNames = {}
                index = 0
                for column in rowValues:
                    if column not in HeaderNames:
                        logging.info ( self.className + ': ERROR - expected Routes Airports column name= {0} not in Header names'.format(column) )
                        return False
                    else:
                        self.ColumnNames[column] = index
                    index += 1

            else:
                #logging.info ( str(row) )
                index = 0
                route = {}
                for cell in rowValues:
                    
                    if len(str(cell))>0:
                        #logging.info ( str(cell) )
                        route[HeaderNames[index]] = str(cell)
                        
                    index = index + 1
                logging.info ( route )
                airlineRoute = AirlineRoute(
                    DepartureAirport = route[HeaderNames[0]],
                    DepartureAirportICAOCode = route[HeaderNames[1]],
                    ArrivalAirport = route[HeaderNames[2]],
                    ArrivalAirportICAOCode = route[HeaderNames[3]]
                    )
                airlineRoute.save()
                self.RoutesAirports.append(route)
        
        return True
    
    
    def dump(self):
        for route in self.RoutesAirports:
            logging.info ( route )
    
    #def getDepartureArrivalAirportICAOcode(self):
    #    for route in self.RoutesAirports:
    #        yield route[HeaderNames[1]] , route[HeaderNames[3]]
            
    def getRoutes(self):
        for route in self.RoutesAirports:
            airlineRoute = AirlineRoute(route[HeaderNames[1]], route[HeaderNames[3]])
            airlineRoute.setRoute(route)
            #logging.info (route)
            yield airlineRoute
    
    def getFlightLegList(self):
        flightLegList = []
        for route in self.RoutesAirports:
            Adep = route[HeaderNames[1]]
            Ades = route[HeaderNames[3]]
            flightLegList.append( Adep + "-" + Ades)
        return flightLegList
    
    def getDepartureAirportsICAOcode(self):
        for route in self.RoutesAirports:
            airportICAOcode = route[HeaderNames[1]]
            yield airportICAOcode
             
    def getDepartureAirportsICAOcodeList(self):
        
        departureAirportICAOcodeList = []
        for route in self.RoutesAirports:
            airportICAOcode = route[HeaderNames[1]]
            departureAirportICAOcodeList.append(airportICAOcode)
                
        return departureAirportICAOcodeList

    def getArrivalAirportsICAOcode(self):
        for route in self.RoutesAirports:
            airportICAOcode = route[HeaderNames[3]]
            yield airportICAOcode
            
    def getArrivalAirportsICAOcodeList(self):
        
        arrivalAirportICAOcodeList = []
        for route in self.RoutesAirports:
            airportICAOcode = route[HeaderNames[3]]
            arrivalAirportICAOcodeList.append(airportICAOcode)

        return arrivalAirportICAOcodeList
            
    def getAirportsICAOcode(self):
        
        listOfAirportICAOcodes = set()
        for route in self.RoutesAirports:
            AdepICAOcode = route[HeaderNames[1]]
            #logging.info ( self.className + ' - Adep= {0} '.format(AdepICAOcode) )

            listOfAirportICAOcodes.add(AdepICAOcode)
            
            AdesICAOcode = route[HeaderNames[3]]
            #logging.info ( self.className + ' - Ades= {0} '.format(AdesICAOcode) )

            listOfAirportICAOcodes.add(AdesICAOcode)
            
        #logging.info ( listOfAirportICAOcodes )
        return list(listOfAirportICAOcodes)