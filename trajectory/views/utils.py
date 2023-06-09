'''
Created on 26 déc. 2022

@author: robert PASTOR
'''

from airline.models import Airline,  AirlineAircraft, AirlineRoute, AirlineCosts

from trajectory.models import  AirlineRunWay , BadaSynonymAircraft, AirlineAirport
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance

from trajectory.Environment.Earth import EarthRadiusMeters
from trajectory.Environment.Constants import Meter2NauticalMiles
from trajectory.Guidance.GeographicalPointFile import GeographicalPoint


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


def computeRouteLengthMiles( AdepICAOcode, AdesICAOcode ):
    adepAirport = AirlineAirport.objects.filter( AirportICAOcode = AdepICAOcode ).first()
    adesAirport = AirlineAirport.objects.filter( AirportICAOcode = AdesICAOcode ).first()
    
    adepGeo = GeographicalPoint(adepAirport.getLatitudeDegrees() , adepAirport.getLongitudeDegrees(), EarthRadiusMeters)
    adesGeo = GeographicalPoint(adesAirport.getLatitudeDegrees() , adesAirport.getLongitudeDegrees(), EarthRadiusMeters)
            #print ( "end of runway extended path = {0}".format(pathEnd) )

    return adepGeo.computeDistanceMetersTo(adesGeo) * Meter2NauticalMiles


def getAirlineRoutesFromDB(airline):
    airlineRoutesList = []
    for airlineRoute in AirlineRoute.objects.filter(airline = airline):
        #logger.debug ( str ( airlineRoute ) )
        airlineRoutesList.append({
                "Airline"                  : airlineRoute.airline.Name,
                "DepartureAirport"         : airlineRoute.DepartureAirport ,
                "DepartureAirportICAOCode" : airlineRoute.DepartureAirportICAOCode,
                "ArrivalAirport"           : airlineRoute.ArrivalAirport,
                "ArrivalAirportICAOCode"   : airlineRoute.ArrivalAirportICAOCode,
                "RouteLengthMiles"         : round ( computeRouteLengthMiles(airlineRoute.DepartureAirportICAOCode , airlineRoute.ArrivalAirportICAOCode) , 2 )
                } )
    return airlineRoutesList


def getAirlineTripPerformanceFromDB( airline ):
    
    assert ( isinstance( airline , Airline ))
    airlineTripPerformanceList = []
    for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
        pass
        badaAircraft = BadaSynonymAircraft.objects.all().filter( AircraftICAOcode=airlineAircraft.aircraftICAOcode ).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
            if acPerformance:
                for airlineRoute in AirlineRoute.objects.filter(airline = airline):
                    pass
                    for airlineCosts in AirlineCosts.objects.filter( airline = airline, airlineAircraft = airlineAircraft, airlineRoute = airlineRoute):
                        OneHourReserveFuelKg =  ( airlineCosts.getFlightLegFuelBurnKg() / airlineCosts.getFlightLegDurationSeconds() ) * 3600.0 
                        airlineTripPerformanceList.append( {
                            "Airline"               : airlineRoute.airline.Name,
                            "Aircraft"              : airlineAircraft.getAircraftICAOcode(),
                            "Route"                 : airlineRoute.getFlightLegAsString(),
                            "TakeOffMassKg"         : airlineCosts.getTakeOffMassKg(),
                            "LegDurationSec"        : round ( airlineCosts.getFlightLegDurationSeconds() , 1 ) ,
                            "LegLengthMiles"        : round ( airlineCosts.getFlightLegLengthMiles() , 1 ) ,
                            "TripFuelBurnKg"        : round ( airlineCosts.getFlightLegFuelBurnKg() , 1 ) ,
                            "OneHourReserveFuelKg"      : round (  OneHourReserveFuelKg , 1 ), 
                            "OptimalTakeOffMassKg"      : round ( acPerformance.getMinimumMassKilograms() + ( ( 80.0 * acPerformance.getMaximumPayLoadMassKilograms() ) / 100.0 ) + airlineCosts.getFlightLegFuelBurnKg() + OneHourReserveFuelKg , 1 )
                            })
    return airlineTripPerformanceList



def getAirlineRunWaysFromDB():
    airlineRunWaysList = []
    for airlineRunWay in AirlineRunWay.objects.all():
        airlineRunWaysList.append( {
            'airlineAirport': airlineRunWay.Airport.AirportICAOcode,
            'airlineRunWayName' : airlineRunWay.Name,
            'airlineRunWayTrueHeadindDegrees': airlineRunWay.TrueHeadingDegrees})
    #print ( "Size of RunWays list = {0}".format(len(airlineRunWaysList)))
    return airlineRunWaysList


def getAirportsFromDB(airline):
    ICAOlist = []
    airportsList = []
    ''' airports are not related to airlines '''
    for airport in AirlineAirport.objects.all():
        ''' routes are related to airlines '''
        for airlineRoute in AirlineRoute.objects.filter(airline = airline):
            #print ( airlineRoute )
            if (airport.AirportICAOcode == airlineRoute.getDepartureAirportICAOcode()) or (airport.AirportICAOcode == airlineRoute.getArrivalAirportICAOcode() ):
                if ( airport.AirportICAOcode not in ICAOlist):
                    #logger.debug (airport.AirportICAOcode)
                    # add airport only once
                    ICAOlist.append(airport.AirportICAOcode)
                    airportsList.append({
                        "AirportICAOcode" : airport.AirportICAOcode ,
                        "AirportName": airport.AirportName,
                        "Longitude": airport.Longitude,
                        "Latitude": airport.Latitude
                        } )
    return airportsList


def getAirlineAircraftsFromDB(airline):
    airlineAircraftsList = []
    for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
        #print (str(airlineAircraft))
        acMaxTakeOffWeightKg = 0.0
        acMinTakeOffWeightKg = 0.0
        acMaxOpAltitudeFeet  = 0.0 
        badaAircraft = BadaSynonymAircraft.objects.all().filter(AircraftICAOcode=airlineAircraft.aircraftICAOcode).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            acPerformance = AircraftPerformance(badaAircraft.getAircraftPerformanceFile())
            if acPerformance:
                acMaxTakeOffWeightKg = acPerformance.getMaximumMassKilograms()
                acMinTakeOffWeightKg = acPerformance.getMinimumMassKilograms()
                acMaxOpAltitudeFeet  = acPerformance.getMaxOpAltitudeFeet()
                acMaxPayLoadKg       = acPerformance.getMaximumPayLoadMassKilograms()
        airlineAircraftsList.append({
            "airlineAircraftICAOcode" : airlineAircraft.aircraftICAOcode,
            "airlineAircraftFullName" : airlineAircraft.aircraftFullName,
            "acMaxTakeOffWeightKg"    : acMaxTakeOffWeightKg,
            "acMinTakeOffWeightKg"    : acMinTakeOffWeightKg,
            "acMaxOpAltitudeFeet"     : acMaxOpAltitudeFeet,
            "acMaxPayLoadKg"          : acMaxPayLoadKg
            })
    #print ("length of airline aircrafts list = {0}".format(len(airlineAircraftsList)))
    return airlineAircraftsList
