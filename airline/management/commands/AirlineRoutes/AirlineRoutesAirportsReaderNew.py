'''
Created on 29 nov. 2022

@author: robert
'''
import os
import logging 
import pandas as pd

from airline.models import AirlineRoute
from airline.models import Airline

HeaderNames = ["Airline" , "Departure Airport", "Departure Airport ICAO Code", "Arrival Airport", "Arrival Airport ICAO Code"]


class AirlineRoutesDataBaseXlsx(object):
    
    FilePath = ''
    RoutesAirports = []

    def __init__(self):
        self.className = self.__class__.__name__

        self.FilePath = "AirlineRoutesAirportsDepartureArrival.xlsx"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        logging.info ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        logging.info ( self.className + ': file path= {0}'.format(self.FilePath) )
        
        self.sheetName = "Routes"
        
        
    def exists(self):
        return os.path.exists(self.FilePath)
    
    
    def read(self):
        pass
        if os.path.exists(self.FilePath):
            df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName , engine="openpyxl"))
            
            for index, row in df_source.iterrows():
                print('Index is: {}'.format(index))
                print('ID is: {} - Airline is: {} - Departure Airport = {}'.format(index, row['Airline'], row['Departure Airport ICAO Code']))
                print('ID is: {} - Airline is: {} - Arrival AIrport = {}'.format(index, row['Airline'], row['Arrival Airport ICAO Code']))

                Route = {}
                for header in HeaderNames:
                    Route[header] = row[header]
                
                self.RoutesAirports.append(Route)
            return True
        else:
            return False
    
    def createAirlineRoutes(self):
        
        if os.path.exists(self.FilePath):
            df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name=self.sheetName , engine="openpyxl"))
            
            for index, row in df_source.iterrows():
                print('Index is: {}'.format(index))
                print('ID is: {} - Airline is: {} - Departure Airport = {}'.format(index, row['Airline'], row['Departure Airport ICAO Code']))
                print('ID is: {} - Airline is: {} - Arrival AIrport = {}'.format(index, row['Airline'], row['Arrival Airport ICAO Code']))

                Route = {}
                for header in HeaderNames:
                    Route[header] = row[header]
                
                self.RoutesAirports.append(Route)
                
                airline = Airline.objects.filter(Name=row[HeaderNames[0]]).first()
                if (airline):
                    airlineRoute = AirlineRoute(
                        airline = airline,
                        DepartureAirport = row[HeaderNames[1]],
                        DepartureAirportICAOCode = row[HeaderNames[2]],
                        ArrivalAirport = row[HeaderNames[3]],
                        ArrivalAirportICAOCode = row[HeaderNames[4]]
                        )
                    print ( str(airlineRoute) )
                    airlineRoute.save()
                
                
    def dump(self):
        for route in self.RoutesAirports:
            logging.info ( route )
    
    #def getDepartureArrivalAirportICAOcode(self):
    #    for route in self.RoutesAirports:
    #        yield route[HeaderNames[1]] , route[HeaderNames[3]]
    
    def getICAORoutes(self):
        for route in self.RoutesAirports:
            airlineRoute = {}
            airlineRoute["Adep"] = route[HeaderNames[2]]
            airlineRoute["Ades"] = route[HeaderNames[4]]
            yield airlineRoute
            
            
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
