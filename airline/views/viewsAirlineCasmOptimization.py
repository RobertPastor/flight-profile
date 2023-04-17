'''
Created on 17 mars 2023

@author: robert
'''


from pulp import LpProblem , LpMinimize ,  LpVariable, LpInteger, lpSum, LpStatus ,  PULP_CBC_CMD, value
from django.http import  JsonResponse

import logging
from pulp.constants import LpBinary
logger = logging.getLogger(__name__)

from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute
from airline.models import AirlineAircraftInstances

from trajectory.Environment.Constants import kerosene_kilo_to_US_gallons , US_gallon_to_US_dollars
from trajectory.Environment.Constants import Meter2NauticalMiles

def getAirlineCasmOptimization(request, airlineName):
    
    logger.debug ("get Airline Fleet for airline = {0}".format(airlineName))

    if (request.method == 'GET'):
        
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            
            nbFligthtLegs = AirlineRoute.objects.filter(airline=airline).count()
            aircraftInstances = AirlineAircraftInstances()
            aircraftInstancesList = aircraftInstances.computeAirlineAircraftInstances(airlineName , nbFligthtLegs)
            logger.info ( aircraftInstancesList )
        
            airlineCasmArray = []
            airlineAircraftICAOcodeList = []
            airlineAircraftFullNameList = []
            
            for aircraftInstance in aircraftInstancesList:
                
                acICAOcode = aircraftInstances.getAircraftInstanceICAOcode(aircraftInstance)
                airlineAircraft = AirlineAircraft.objects.filter(airline=airline , aircraftICAOcode=acICAOcode).first()
                                
                nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                
                airlineAircraftICAOcodeList.append(airlineAircraft.aircraftICAOcode)
                airlineAircraftFullNameList.append(airlineAircraft.aircraftFullName)
                
                aircraftCasmArray = []
                airlineFlightLegsList = []
                
                for airlineRoute in AirlineRoute.objects.filter(airline=airline):
                    
                    #print ( airlineRoute.getFlightLegAsString() )
                    airlineFlightLegsList.append(airlineRoute.getFlightLegAsString())
                    
                    airlineCosts = AirlineCosts.objects.all().filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                    if airlineCosts:
                        
                        massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                        fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                
                        operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                                
                        crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                        totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars     
                        
                        ''' 5th February 2023 - Costs per Available Seat Mile '''
                        miles = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                        seatsPerMiles = nbSeats * miles
                        casmUSdollars = totalCostsUSdollars / seatsPerMiles
                        
                        #print ( "{0} - {1} - {2}".format(airlineAircraft.aircraftICAOcode, airlineRoute.getFlightLegAsString() , type(totalCostsUSdollars) ))
                            
                        aircraftCasmArray.append( float(casmUSdollars) )
                        
                airlineCasmArray.append(aircraftCasmArray)
                
            print ( airlineCasmArray )
            
            num_flight_legs = len( AirlineRoute.objects.filter(airline=airline) )
            logger.info ( "num flight legs = {0}".format(num_flight_legs) )
            num_aircraft_instances = len(aircraftInstancesList)
            
            logger.info ( "number of aircraft instances = {0}".format( num_aircraft_instances ) )
            num_flight_legs = len(airlineCasmArray[0])
            logger.info ( "num flight legs = {0}".format(num_flight_legs) )

            prob = LpProblem("CASM-Problem", LpMinimize)
            
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
            prob += lpSum( [ airlineCasmArray[i][j] * x_vars[i,j] for i in range(num_aircraft_instances) for j in range(num_flight_legs) ])

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
                #check_constraints(prob, c_list)

                #solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) <= 1)
                
            ''' minimize the costs '''
            #solver.Minimize(solver.Sum(objective_terms))
            prob.solve(PULP_CBC_CMD(msg=0))
            logger.info ("Status: {0}".format( str( LpStatus[prob.status] ) ) )
            
            results = []
            for v in prob.variables():
                result = {}
                result["airline"] = airlineName
                result["status"] = str(LpStatus[prob.status])
                
                acICAOcode = str(v.name).split("_")[0]
                result["aircraft"] = acICAOcode
                
                ''' between index 0 which is the aircraft ICAO code and the flight leg there is the aircraft instance '''
                Adep = str(v.name).split("_")[2]
                result["AdepICAO"] = Adep
                
                Ades = str(v.name).split("_")[3]
                result["AdesICAO"] = Ades
                
                airlineRoute = AirlineRoute.objects.filter(airline=airline , DepartureAirportICAOCode=Adep  , ArrivalAirportICAOCode=Ades).first()
                if ( airlineRoute ):
                    result["Adep"] = airlineRoute.DepartureAirport
                    result["Ades"] = airlineRoute.ArrivalAirport
                    
                    airlineAircraft = AirlineAircraft.objects.filter(airline=airline, aircraftICAOcode=acICAOcode).first()
                    if airlineAircraft:
                        
                        nbSeats = airlineAircraft.getMaximumNumberOfPassengers()
                        
                        airlineCosts = AirlineCosts.objects.filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                        if airlineCosts:
                            
                            massLossKg =  airlineCosts.initialTakeOffMassKg - airlineCosts.finalMassKg    
                            fuelCostsUSdollars = massLossKg * kerosene_kilo_to_US_gallons * US_gallon_to_US_dollars
                                    
                            operationalFlyingCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCostsFlyingPerHoursDollars()
                                    
                            crewCostsUSdollars = ( airlineCosts.flightDurationSeconds / 3600.0 ) *  airlineAircraft.getCrewCostsPerFlyingHoursDollars()
                            totalCostsUSdollars = fuelCostsUSdollars + operationalFlyingCostsUSdollars + crewCostsUSdollars     
                            
                            ''' 5th February 2023 - Costs per Available Seat Mile '''
                            miles = airlineCosts.finalLengthMeters * Meter2NauticalMiles
                            seatsPerMiles = nbSeats * miles
                            casmUSdollars = totalCostsUSdollars / seatsPerMiles
                            
                            result["Seats"] =  nbSeats 
                            result["Miles"] =  round ( miles , 2 )
                            result["Costs"] =  round ( totalCostsUSdollars , 2 )
                            result["CASM"] = round ( casmUSdollars , 4 )
                            
                if ( v.varValue > 0.0 ):
                    logger.info ( "var name = {0} - var value = {1}".format( v.name, v.varValue ) )
                    result["assigned"] = "yes"
                    results.append(result)
                else:
                    result["assigned"] = "no"

            # The optimized objective function value is printed to the screen
            logger.info ( "Total CASM Objective  = {0}".format( value(prob.objective) ) )
            
            return JsonResponse({'results': results})
            
        else:
            return JsonResponse({'errors': "unknown airline = {0}".format(airlineName)})
        
        
    else:
        return JsonResponse({'errors': "expecting GET method"})

