'''
Created on 4 juin 2023

@author: robert
'''

import os
import pandas as pd
from trajectory.models import AirlineAirport, AirlineStandardDepartureArrivalRoute, AirlineRunWay, AirlineWayPoint, AirlineSidStarWayPointsRoute
from trajectory.views.utils import convertDegreeMinuteSecondToDecimal

class SidStarLoaderOne():
    pass

    def __init__(self , isSID , departureOrArrivalAirportICAO  , FirstLastWayPointName , RunWayStr):
        
        self.className = self.__class__.__name__
        
        self.isSID = isSID
        assert ( isinstance( self.isSID, bool))
        
        assert ( isinstance( departureOrArrivalAirportICAO, str) and (len(departureOrArrivalAirportICAO)>0))
        self.departureOrArrivalAirportICAO = departureOrArrivalAirportICAO
        
        assert ( isinstance( FirstLastWayPointName, str) and (len(FirstLastWayPointName)>0))
        self.FirstLastWayPointName = FirstLastWayPointName
        
        assert ( isinstance( RunWayStr, str) and (len(RunWayStr)>0))
        self.RunWayStr = RunWayStr
        
        self.SIDFileNamePrefix = "SID"
        self.STARFileNamePrefix = "STAR"
        
        if ( self.isSID ):
            self.fileName = self.SIDFileNamePrefix + "-" + self.departureOrArrivalAirportICAO + "-" + self.RunWayStr + "-" + self.FirstLastWayPointName + ".xlsx"
        else:
            self.fileName = self.STARFileNamePrefix + "-" + self.departureOrArrivalAirportICAO + "-" + self.FirstLastWayPointName + "-" + self.RunWayStr + ".xlsx"
        
        #self.FilesFolder = os.getcwd()
        self.FilesFolder = os.path.dirname(__file__)

        print ( self.className + ': file folder= {0}'.format(self.FilesFolder) )
        self.sheetName = "WayPoints"
        
        
    def exists( self ):
        print ( self.fileName )
        self.filePath = os.path.join( self.FilesFolder , self.fileName)
        print ( self.filePath )
        return os.path.exists(self.filePath)
    
    def getAirport(self):
        return self.airport
    
    def getRunWay(self):
        return self.runway
    
    def getOrCreateSidStarDBObject(self):
        
        sidStarDbObj = None
        self.airport = AirlineAirport.objects.filter( AirportICAOcode = self.departureOrArrivalAirportICAO ).first()
        if ( self.airport is None ):
            raise ValueError ( "airport = {0} not found in databaase ".format( self.departureOrArrivalAirportICAO ))
        else:
            self.runway = AirlineRunWay.objects.filter( Name = self.RunWayStr , Airport = self.airport ).first()
            if ( self.runway is None ):
                raise ValueError ( "runway = {0} not found in databaase ".format( self.RunWayStr ))
            else:
                waypoint = AirlineWayPoint.objects.filter( WayPointName = self.FirstLastWayPointName).first()
                if ( waypoint is None ):
                    raise ValueError ( "waypoint = {0} not found in database ".format( self.FirstLastWayPointName ))
                else:
                    
                    sidStarDbObj = AirlineStandardDepartureArrivalRoute.objects.filter (
                                    isSID                   = self.isSID ,
                                    DepartureArrivalAirport = self.airport,
                                    DepartureArrivalRunWay  = self.runway ,
                                    FirstLastRouteWayPoint  = waypoint
                                    ).first()
                    if ( sidStarDbObj is None):
                        sidStarDbObj = AirlineStandardDepartureArrivalRoute(
                                        isSID                   = self.isSID ,
                                        DepartureArrivalAirport = self.airport,
                                        DepartureArrivalRunWay  = self.runway ,
                                        FirstLastRouteWayPoint  = waypoint
                                        )
                        sidStarDbObj.save()
                        
        return sidStarDbObj
    
    
    def load( self ):
        
        sidStarDbObj = self.getOrCreateSidStarDBObject()
        assert ( isinstance( sidStarDbObj , AirlineStandardDepartureArrivalRoute ) )
        
        ''' delete previous waypoints related to the same SID STAR route  '''
        AirlineSidStarWayPointsRoute.objects.filter ( Route = sidStarDbObj ).delete()
        
        if self.exists():
            print ( "file exists = {0}".format( self.filePath ))
            df_source = pd.DataFrame(pd.read_excel(self.filePath, sheet_name=self.sheetName , engine="openpyxl"))
            for index, row in df_source.iterrows():
                
                print('Index is: {}'.format(index))
                print ("order is {0}".format(row["order"]))
                print ("wayPoint name is {0}".format(row["waypoint"]))
                
                latitudeDegrees = 0.0
                longitudeDegrees = 0.0
                ''' search for the airport '''
                if ( str(row["waypoint"]).startswith( self.airport.getICAOcode() )):
                    ''' first entry is airport ICAO code / runway name '''
                    if ( str ( row["waypoint"] ).index( "/" ) > 0):
                        ''' there is a SLASH as expected '''
                        runwayName = str(row["waypoint"]).split("/")[1]
                        print ( runwayName )
                        latitudeDegrees = self.runway.getLatitudeDegrees()
                        longitudeDegrees= self.runway.getLongitudeDegrees()
                    else:
                        raise ValueError ( "Expecting a SLASH in airport name = {0} but not found ".format( str ( row["waypoint"] ) ) )
                else:
                    print ("latitude is {0}".format(row["latitude"]))
                    strLatitude = str( row["latitude"] ).strip()
                    if ('°' in strLatitude ):
                        strLatitude = str(strLatitude).replace('°','-')
                        strLatitude = str(strLatitude).strip().replace("'", '-').replace(' ','').replace('"','')
                        latitudeDegrees = convertDegreeMinuteSecondToDecimal ( strLatitude )
                    else:
                        raise ValueError ( "Expecting a ° degree symbol in latitude = {0} but not found ".format( str( row["latitude"] ) ) )
                            
                    print ("longitude is {0}".format(row["longitude"]))
                    strLongitude = str( row["longitude"] ).strip()
                    if ('°' in strLongitude):
                        strLongitude = str(strLongitude).replace('°','-')
                        strLongitude = str(strLongitude).strip().replace("'", '-').replace(' ','').replace('"','')
                        longitudeDegrees = convertDegreeMinuteSecondToDecimal ( strLongitude )
                    else:
                        raise ValueError ( "Expecting a ° degree symbol in longitude = {0} but not found ".format( str( row["longitude"] ) ) )
                
                print ("----------- {0} -----------".format(row["order"]))
                ''' 10th August 2023 - DASH is a separator in the fixlist -> need to replace it with UNDERSCORE '''
                waypointWithoutDash = str(row["waypoint"]).strip().replace("-", "_")
                sidStarWayPoint = AirlineSidStarWayPointsRoute ( 
                                Route           = sidStarDbObj ,
                                Order           = int( row["order"] ),
                                WayPointName    =  waypointWithoutDash,
                                LatitudeDegrees  = latitudeDegrees,
                                LongitudeDegrees = longitudeDegrees
                                )
                sidStarWayPoint.save()
                
                ''' 6th June 2023 - SID STAR way-points must be loaded in the WayPoints database '''
                airlineWayPoint = AirlineWayPoint.objects.filter ( WayPointName = waypointWithoutDash ).first()
                if ( airlineWayPoint is None ):
                    airlineWayPoint = AirlineWayPoint( WayPointName = waypointWithoutDash ,
                                                       Latitude = latitudeDegrees,
                                                       Longitude = longitudeDegrees )
                    airlineWayPoint.save()
                
            return df_source
                
        else:
            print ( "file does not exist = {0}".format( self.filePath ))
            return None
            