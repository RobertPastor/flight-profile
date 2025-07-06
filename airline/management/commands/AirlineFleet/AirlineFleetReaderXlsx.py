'''
Created on 29 août 2021

@author: robert
'''

import os
import logging

import pandas as pd

from airline.models import AirlineAircraft, Airline

''' in service means number of available aircrafts '''
HeaderNames = ['Airline', 'Aircraft ICAO', 'Aircraft' , 'In service', 'Orders' , 'Passengers Delta One', 'Passengers First Class', 'Passengers Premium Select' ,
               'Passengers Delta Confort Plus' , 'Passengers Main Cabin' , 'Passengers Total' , 'Costs per flying hours dollars', 
               'Crew Costs per flying hours dollars', 
               'TurnAround Time Minutes' , 'Refs', 'Notes']


class AirlineFleetDataBase(object):
    FilePath = ''
    
    ''' list of class AirlineAircraft '''
    FleetAircrafts = []
    
    def __init__(self):
        self.className = self.__class__.__name__
        self.FilePath = "AirlineFleet.xlsx"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        logging.info ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.FilePath = os.path.abspath(self.FilesFolder+ os.path.sep + self.FilePath)
        logging.info ( self.className + ': file path= {0}'.format(self.FilePath) )
        
        
    def exists(self):
        return os.path.exists(self.FilePath) 


    def read(self):
        ''' this method reads the whole file - not only the headers '''
        print (self.FilePath)
        assert len(self.FilePath)>0 and os.path.isfile(self.FilePath) 
        
        df_source = pd.DataFrame(pd.read_excel(self.FilePath, sheet_name="Fleet" , engine="openpyxl"))
            
        for index, row in df_source.iterrows():
            print('Index is: {}'.format(index))
        
            print ( '--> row --> {0}'.format(row) )
            
            index = 0
            ''' one aircraft per row '''
            
            airlineName            = str(row['Airline']).strip()
            aircraftICAOcode       = str(row['Aircraft ICAO']).strip()
            aircraftFullName       = str(row['Aircraft']).strip()
            
            nbAvailableAircrafts   = int ( row['In service'] )
            nbMaxPassengers        = int ( row['Passengers Total'] )
            costsFlyingDollars     = float ( row['Costs per flying hours dollars'])
            crewCostsFlyingDollars = float ( row['Crew Costs per flying hours dollars'])
            turnAroundTimesMinutes = float ( row['TurnAround Time Minutes'])
            
            print ( aircraftFullName )
            if (aircraftICAOcode):
                logging.info ("aircraft ICAO code found = {0} for aircraft full name = {1}".format(aircraftICAOcode, aircraftFullName))
                airline = Airline.objects.filter(Name=airlineName).first()
                if (airline):
                    ''' 4th May 2023 - add turn around time expressed in minutes '''
                    
                    ''' check if airline Aircraft exists '''
                    if AirlineAircraft.objects.filter( airline = airline , aircraftICAOcode = aircraftICAOcode ).exists():
                        print ( "aircraft = {0} - of airline = {1} is already existing".format( aircraftICAOcode, airlineName))
                    else:
                        print (  "aircraft = {0} - of airline = {1} is new in the database".format( aircraftICAOcode, airlineName) )
                        airlineAircraft = AirlineAircraft( 
                                airline                    = airline,
                                aircraftICAOcode           = aircraftICAOcode, 
                                aircraftFullName           = aircraftFullName, 
                                numberOfAircraftsInService = nbAvailableAircrafts, 
                                maximumOfPassengers        = nbMaxPassengers, 
                                costsFlyingPerHoursDollars     = costsFlyingDollars,
                                crewCostsPerFlyingHoursDollars = crewCostsFlyingDollars,
                                turnAroundTimesMinutes         = turnAroundTimesMinutes)

                        print ( airlineAircraft )
                        airlineAircraft.save()
                        print ( airline )
                        print ( aircraftFullName )
                        self.FleetAircrafts.append( airlineAircraft )
                
            else:
                print("Aircraft ICAO code not found = {0}".format( aircraftFullName )) 
               
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
    
        