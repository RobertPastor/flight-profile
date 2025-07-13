'''
Created on 26 déc. 2022

@author: robert PASTOR
'''
import logging

from airline.models import Airline,  AirlineAircraft, AirlineRoute, AirlineCosts

from trajectory.models import  AirlineRunWay , BadaSynonymAircraft
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance

from trajectory.Environment.Earth import EarthRadiusMeters
from trajectory.Environment.Constants import Meter2NauticalMiles
from trajectory.Guidance.GeographicalPointFile import GeographicalPoint

from trajectory.models import AirlineStandardDepartureArrivalRoute, AirlineAirport

from openap import prop
from trajectory.Openap.AircraftMainFile import OpenapAircraft
from trajectory.Environment.Earth import Earth
from trajectory.Environment.Atmosphere import Atmosphere

def getAircraftFromRequest(request):
    return request.GET['aircraft']

def getRouteFromRequest(request):
    return request.GET['route']

def getAdepRunwayFromRequest(request):
    return request.GET['adepRwy']

def getAdesRunwayFromRequest(request):
    return request.GET['adesRwy']

def getMassFromRequest(request):
    return request.GET['mass']

def getFlightLevelFromRequest(request):
    return request.GET['fl']

def getReducedClimbPowerCoeffFromRequest(request):
    return request.GET['reduc']

def getDirectRouteFromRequest(request):
    try:
        if ( request.GET['direct'] == 'true'):
            return True
        else:
            return False
    except:
        return False

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
                ''' two digits of milliseconds '''
                DecimalValue += (float(TenthOfSecondsValue)/float(3600.0)) / 100.0
                    
            DecimalValue = coeff * DecimalValue
        else:
            raise ValueError ('unexpected Degrees Minutes Seconds format')
    else:
        raise ValueError ('unexpected Degrees Minutes Seconds format')

    #print "DegreeMinuteSecond= ", DegreeMinuteSecond, " DecimalValue= ", DecimalValue
    return DecimalValue

def computeRouteLengthMiles( AdepICAOcode, AdesICAOcode ):
    try:
        adepAirport = AirlineAirport.objects.filter( AirportICAOcode = AdepICAOcode ).first()
        adesAirport = AirlineAirport.objects.filter( AirportICAOcode = AdesICAOcode ).first()
        
        adepGeo = GeographicalPoint(adepAirport.getLatitudeDegrees() , adepAirport.getLongitudeDegrees(), EarthRadiusMeters)
        adesGeo = GeographicalPoint(adesAirport.getLatitudeDegrees() , adesAirport.getLongitudeDegrees(), EarthRadiusMeters)
        #print ( "end of runway extended path = {0}".format(pathEnd) )
    
        return adepGeo.computeDistanceMetersTo(adesGeo) * Meter2NauticalMiles
    except :
        return 0.0

def isAirportInAirlineAirports(airline , airlineAirport ):
    
    assert ( isinstance ( airline , Airline ))
    assert ( isinstance ( airlineAirport , AirlineAirport ))

    for airlineRoute in AirlineRoute.objects.filter(airline = airline):
        if (airlineAirport.getICAOcode() == airlineRoute.getDepartureAirportICAOcode()) or (airlineAirport.getICAOcode() == airlineRoute.getArrivalAirportICAOcode() ):
            return True
        
    return False

def computeListOfDepartureRunWaysWithSID(airlineRoute):
    sidStars = AirlineStandardDepartureArrivalRoute.objects.all()
    for sidStar in sidStars:
        if ( sidStar.getIsSID() ):
            if ( airlineRoute.getDepartureAirportICAOcode() == sidStar.getDepartureArrivalAirport().getICAOcode() ):
                ''' there is a SID with the same departure airport '''
                #print ( sidStar )
                firstRouteWayPoint = airlineRoute.getFirstRouteWayPoint()
                #print ( firstRouteWayPoint )
                
                if ( sidStar.getFirstLastRouteWayPoint() == firstRouteWayPoint):
                    ''' warning : there might be several runways related to the same airport and the same first waypoint '''
                    SidName = sidStar.getDepartureArrivalAirport().getICAOcode() +"/" + sidStar.getDepartureArrivalRunWay().getName() + "/" + firstRouteWayPoint.getWayPointName()
                    return SidName

    return ""

def computeListOfArrivalRunWaysWithSTAR(airlineRoute):
    sidStars = AirlineStandardDepartureArrivalRoute.objects.all()
    for sidStar in sidStars:
        if ( sidStar.getIsSTAR() ):
            if ( airlineRoute.getArrivalAirportICAOcode() == sidStar.getDepartureArrivalAirport().getICAOcode() ):
                ''' there is a STAR with the same arrival airport '''
                lastRouteWayPoint = airlineRoute.getLastRouteWayPoint()
                ''' equating Django objects '''
                if ( sidStar.getFirstLastRouteWayPoint() == lastRouteWayPoint):
                    ''' warning : there might be several runways related to the same airport and the same first waypoint '''
                    StarName = sidStar.getDepartureArrivalAirport().getICAOcode() +"/" + sidStar.getDepartureArrivalRunWay().getName() + "/" + lastRouteWayPoint.getWayPointName()
                    return StarName
    
    return ""

def getAirlineRoutesFromDB(airline):
    airlineRoutesList = []
    for airlineRoute in AirlineRoute.objects.filter(airline = airline).distinct().order_by("DepartureAirportICAOCode"):
        #print ( airlineRoute )
        #logger.debug ( str ( airlineRoute ) )
        airlineRoutesList.append({
                "Airline"                  : airlineRoute.airline.Name,
                "DepartureAirport"         : airlineRoute.DepartureAirport ,
                "DepartureAirportICAOCode" : airlineRoute.DepartureAirportICAOCode,
                "SID"                      : computeListOfDepartureRunWaysWithSID(airlineRoute),
                "ArrivalAirport"           : airlineRoute.ArrivalAirport,
                "ArrivalAirportICAOCode"   : airlineRoute.ArrivalAirportICAOCode,
                "STAR"                     : computeListOfArrivalRunWaysWithSTAR(airlineRoute),
                "RouteLengthMiles"         : round ( computeRouteLengthMiles(airlineRoute.DepartureAirportICAOCode , airlineRoute.ArrivalAirportICAOCode) , 2 ),
                "BestDepartureRunway"      : airlineRoute.computeBestDepartureRunWay(),
                "BestArrivalRunway"        : airlineRoute.computeBestArrivalRunWay()
                } )
    return airlineRoutesList

def getAirlineTripPerformanceFromDB( airline ):
    assert ( isinstance( airline , Airline ))
    airlineTripPerformanceList = []
    for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
        badaAircraft = BadaSynonymAircraft.objects.all().filter( AircraftICAOcode=airlineAircraft.aircraftICAOcode ).first()
        if ( badaAircraft and badaAircraft.aircraftPerformanceFileExists()):
            acPerformance = AircraftJsonPerformance(airlineAircraft.aircraftICAOcode, badaAircraft.getAircraftPerformanceFile())
            if acPerformance.read():
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
                        "AirportName"     : airport.AirportName,
                        "Longitude"       : airport.Longitude,
                        "Latitude"        : airport.Latitude
                        } )
    return airportsList


def getAirlineAircraftsFromDB(airline , BadaWrapMode):
    #print(BadaWrapMode)
    earth = Earth()
    atmosphere = Atmosphere()
    airlineAircraftsList = []
    
    if BadaWrapMode == "BADA":
        for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
            #print (str(airlineAircraft))
            acMaxTakeOffWeightKg = 0.0
            acMinTakeOffWeightKg = 0.0
            acMaxOpAltitudeFeet  = 0.0 
            acReferenceWeightKg  = 0.0
            
            badaAircraft = BadaSynonymAircraft.objects.filter(AircraftICAOcode = airlineAircraft.aircraftICAOcode).first()
            if ( badaAircraft and badaAircraft.aircraftJsonPerformanceFileExists()):
                acPerformance = AircraftJsonPerformance(airlineAircraft.aircraftICAOcode, badaAircraft.getAircraftJsonPerformanceFile())
                if acPerformance.read():
                    acMaxTakeOffWeightKg = acPerformance.getMaximumMassKilograms()
                    acMinTakeOffWeightKg = acPerformance.getMinimumMassKilograms()
                    acMaxOpAltitudeFeet  = round ( acPerformance.getMaxOpAltitudeFeet() , 0 )
                    acMaxPayLoadKg       = acPerformance.getMaximumPayLoadMassKilograms()
                    acReferenceWeightKg  = acPerformance.getReferenceMassKilograms()
                    
                    airlineAircraftsList.append({
                        "airlineAircraftICAOcode"    : airlineAircraft.aircraftICAOcode,
                        "airlineAircraftFullName"    : airlineAircraft.aircraftFullName,
                        "acMaxTakeOffWeightKg"       : acMaxTakeOffWeightKg,
                        "acReferenceTakeOffWeightKg" : acReferenceWeightKg,
                        "acMinTakeOffWeightKg"       : acMinTakeOffWeightKg,
                        "acMaxOpAltitudeFeet"        : acMaxOpAltitudeFeet,
                        "acMaxPayLoadKg"             : acMaxPayLoadKg
                        })
    else:
        ''' WRAP mode '''
        for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):

            airlineAircraftICAOcode = airlineAircraft.aircraftICAOcode
            
            available_Wrap_aircrafts = prop.available_aircraft(use_synonym=True)
            for aircraftICAOcode in available_Wrap_aircrafts:
                
                if ( str( aircraftICAOcode ).lower() in ['a359','a388','b38m','b744','b748','b752','b763','b773','b77w','b788','b789','c550'] \
                     or str( aircraftICAOcode ).lower() in ['e145','glf6','a124','a306','a310','at72','at75','at76','b733','b735','b762','b77l'] \
                     or str ( aircraftICAOcode ).lower() in ['c25a','c525','c56x','crj2','crj9','e290','glf5','gl5t','gl6t','tj45','md11','pc24','su95','lj45','bx3m'] ):
                    #pass
                    continue
                
                if aircraftICAOcode.upper() == airlineAircraftICAOcode:
                
                    ac = OpenapAircraft( aircraftICAOcode , earth , atmosphere , initialMassKilograms = None)
                    logging.info( ac.getAircraftName() )
                    airlineAircraftsList.append({
                        "airlineAircraftICAOcode"    : str(aircraftICAOcode).upper(),
                        "airlineAircraftFullName"    : ac.getAircraftName(),
                        "acMaxTakeOffWeightKg"       : ac.getMaximumTakeOffMassKilograms(),
                        "acReferenceTakeOffWeightKg" : ac.getReferenceMassKilograms(),
                        "acMinTakeOffWeightKg"       : ac.getMinimumMassKilograms(),
                        "acMaxOpAltitudeFeet"        : round ( ac.getMaxCruiseAltitudeFeet() ,0),
                        "acMaxPayLoadKg"             : 0.0
                        })

    #print ("length of airline aircrafts list = {0}".format(len(airlineAircraftsList)))
    return airlineAircraftsList
