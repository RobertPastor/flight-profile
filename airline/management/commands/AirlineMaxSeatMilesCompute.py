'''
Created on 4 mai 2023

@author: robert

compute max number of rotations for each aircraft type for each flight leg
on a typical 20 hours day durations - using cycles
one cycle = flight leg one way + turn around time + flight leg return 
one way and return are based upon the cost durations


'''
from django.core.management.base import BaseCommand

import logging
from pulp.constants import LpMaximize
logger = logging.getLogger(__name__)

from airline.models import Airline, AirlineAircraft, AirlineRoute, AirlineCosts, AirlineAircraftInstances
from trajectory.Environment.Constants import Meter2NauticalMiles

from pulp import LpProblem  ,  LpVariable,  lpSum, LpStatus ,  PULP_CBC_CMD,  LpBinary

maxDailyHours= 20.0

def computeNumberOfRotations(flightDurationSeconds , turnAroundTimesSeconds):
    ''' the aircraft is ready after one flight level duration + 1 turn around time at the arrival airport + 1 flight leg duration + 1 turn around time at the departure airport '''
    return ( maxDailyHours * 3600 ) / ( ( flightDurationSeconds + turnAroundTimesSeconds ) * 2 ) 

class Command(BaseCommand):

    def handle(self, *args, **options):
        
        logger.setLevel(logging.INFO)
        
        help = 'Compute the maximum of seats per miles'
        
        for airline in Airline.objects.all():
            print ( airline )
            
            airlineName = airline.Name
            airlineSeatsMiles = []
            ''' need to define aircraft instances as the "costs" table must be squared between aircrafts instances and flight legs '''
            
            nbFligthtLegs = AirlineRoute.objects.filter(airline=airline).count()
            aircraftInstances = AirlineAircraftInstances()
            aircraftInstancesList = aircraftInstances.computeAirlineAircraftInstances(airlineName , nbFligthtLegs)
            #print ( aircraftInstancesList )
            
            for aircraftInstance in aircraftInstancesList:
                
                acICAOcode = aircraftInstances.getAircraftInstanceICAOcode(aircraftInstance)
                airlineAircraft = AirlineAircraft.objects.filter(airline=airline , aircraftICAOcode=acICAOcode).first()
                                
                nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                turnAroundTimesSeconds = airlineAircraft.getTurnAroundTimesMinutes() * 60
            
                print ( "aircraft = {0} - number of seats = {1} - turnAround times Seconds = {2}".format( airlineAircraft , nbSeats , turnAroundTimesSeconds) )
                
                aircraftSeatMiles = []
                airlineFlightLegsList = []
                
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                    
                    airlineFlightLegsList.append(airlineRoute.getFlightLegAsString())
                    
                    airlineCosts = AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                    if airlineCosts:
                        
                        milesFlownPerLeg = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                        #print ("aircraft = {0} - flight leg = {1} - flight duration (Seconds) = {2} - distance flown (nautics) = {3}".format(airlineAircraft, airlineRoute.getFlightLegAsString() , airlineCosts.flightDurationSeconds, milesFlownPerLeg))
                        nbRotationsDay = computeNumberOfRotations( airlineCosts.flightDurationSeconds , turnAroundTimesSeconds)
                        #print ( "nb rotations = {0} - nb rotations = {1}".format( nbRotationsDay , int(nbRotationsDay) ) )
                        
                        totalSeatMilesFlownPerDay = nbSeats * int(nbRotationsDay) * 2 * milesFlownPerLeg
                        #print ( "total miles flown in 20 hours = {0}".format( totalSeatMilesFlownPerDay ))
                        
                        aircraftSeatMiles.append( totalSeatMilesFlownPerDay )
                        
                airlineSeatsMiles.append(aircraftSeatMiles)
    
            prob = LpProblem("Seat-Miles-Problem", LpMaximize)
            
            num_aircraft_instances = len(aircraftInstancesList)
            num_flight_legs = len( AirlineRoute.objects.filter(airline=airline) )

            ''' define the variables '''
            x_vars = {}
            #print ( range(num_aircrafts) )
            for i in range(num_aircraft_instances):
                #print ( "---> {0} - {1}".format( i , airlineAircraftICAOcodeList[i] ) )
                for j in range(num_flight_legs):
                    #print ( "------> {0} - {1}".format ( j , airlineFlightLegsList[j] ) )
                    #print ( '{0}-{1}'.format(airlineAircraftICAOcodeList[i], airlineFlightLegsList[j]) )
                    #x[i, j] = solver.IntVar(0, 1, '{0}-{1}'.format("A320", airlineFlightLegsList[j]))
                    pass
                    #x_vars = LpVariable("x_vars", lowBound=0, upBound=1, cat='Integer', e=None)
                    x_vars[i,j] = LpVariable(name="{0}-{1}".format(aircraftInstancesList[i], airlineFlightLegsList[j]), lowBound=0, upBound=1, cat=LpBinary)
                    
            ''' define the objective function '''
            prob += lpSum( [ airlineSeatsMiles[i][j] * x_vars[i,j] for i in range(num_aircraft_instances) for j in range(num_flight_legs) ])

            logger.info ( "--- add constraints ----")
            '''  Each aircraft is assigned to at most 1 flight leg. '''
            for i in range(num_aircraft_instances):
                pass
                #solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
                prob += lpSum( [ x_vars[i,j] for j in range(num_flight_legs) ] ) <= 1
                
            ''' Each flight leg is assigned to exactly one aircraft '''
            for j in range(num_flight_legs):
                pass
                prob += lpSum ( [ x_vars[i,j] for i in range(num_aircraft_instances) ] ) == 1
                
            prob.solve(PULP_CBC_CMD(msg=0))
            logger.info ("Status: {0}".format( str( LpStatus[prob.status] ) ) )
            
            results = []
            for v in prob.variables():
                result = {}
                result["airline"] = airlineName
                result["status"] = str(LpStatus[prob.status])
                
                print ( result )
                