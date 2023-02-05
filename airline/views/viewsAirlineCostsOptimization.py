'''
Created on 29 janv. 2023

@author: robert
'''

#from ortools.linear_solver import pywraplp
from pulp import LpProblem , LpMinimize , listSolvers, LpVariable, LpInteger, lpSum, LpStatus , value, PULP_CBC_CMD
from django.http import  JsonResponse

import logging
logger = logging.getLogger(__name__)
from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute

kerosene_kilo_to_US_gallons = 0.33
US_gallon_to_US_dollars = 3.25


def getCostsOptimization(request, airlineName):
    logger.debug ("get Airline Fleet for airline = {0}".format(airlineName))
    
    if (request.method == 'GET'):
        
        ''' Create the MIP solver with the SCIP back-end '''
        #solver = pywraplp.Solver.CreateSolver('SCIP')
        prob = LpProblem("AssignmentProblem", LpMinimize)
        #solver_list = listSolvers(onlyAvailable=True)
        #print (solver_list)
        
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            
            airlineCostsArray = []
            airlineAircraftICAOcodeList = []
            airlineAircraftFullNameList = []
            for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
                
                #print ( airlineAircraft.aircraftFullName )
                airlineAircraftICAOcodeList.append(airlineAircraft.aircraftICAOcode)
                airlineAircraftFullNameList.append(airlineAircraft.aircraftFullName)
                
                aircraftCostsArray = []
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
                        
                        #print ( "{0} - {1} - {2}".format(airlineAircraft.aircraftICAOcode, airlineRoute.getFlightLegAsString() , type(totalCostsUSdollars) ))
                            
                        aircraftCostsArray.append( float(totalCostsUSdollars) )
                        
                airlineCostsArray.append(aircraftCostsArray)
                
            #print ( airlineCostsArray )
            #print ( "number of aircrafts = {0}".format( len( AirlineAircraft.objects.filter(airline=airline) ) ) )
            #print ( "number of routes = {0}".format( len( AirlineRoute.objects.filter(airline=airline) ) ) )
            
            '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
            '''  if worker i is assigned to task j. '''
            num_aircrafts = len( AirlineAircraft.objects.filter(airline=airline) )
            num_flight_legs = len( AirlineRoute.objects.filter(airline=airline) )
            
            num_aircrafts = len(airlineCostsArray)
            #print ( num_aircrafts )
            num_flight_legs = len(airlineCostsArray[0])
            #print ( num_flight_legs )
            
            x_vars = {}
            #print ( range(num_aircrafts) )
            for i in range(num_aircrafts):
                #print ( "---> {0} - {1}".format( i , airlineAircraftICAOcodeList[i] ) )
                for j in range(num_flight_legs):
                    #print ( "------> {0} - {1}".format ( j , airlineFlightLegsList[j] ) )
                    #print ( '{0}-{1}'.format(airlineAircraftICAOcodeList[i], airlineFlightLegsList[j]) )
                    #x[i, j] = solver.IntVar(0, 1, '{0}-{1}'.format("A320", airlineFlightLegsList[j]))
                    pass
                    #x_vars = LpVariable("x_vars", lowBound=0, upBound=1, cat='Integer', e=None)
                    x_vars[i,j] = LpVariable(name="{0}-{1}".format(airlineAircraftICAOcodeList[i], airlineFlightLegsList[j]), lowBound=0, upBound=1, cat=LpInteger)
                    
            
            ''' --------- objective function --------------'''
            for i in range(num_aircrafts):
                for j in range(num_flight_legs):
                    #objective_terms.append(float(airlineCostsArray[i][j]) * x[i, j])
                    prob += lpSum(airlineCostsArray[i][j] * x_vars[i,j])
                    
            '''  Each aircraft is assigned to at most 1 flight leg. '''
            for i in range(num_aircrafts):
                pass
                #solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
                #prob += lpSum(x_vars[i][j] for j in range(num_flight_legs)) <= 1, ""
                
            ''' Each flight leg is assigned to exactly one aircraft '''
            for j in range(num_flight_legs):
                pass
                prob += lpSum(x_vars[i,j] for i in range(num_aircrafts)) == 1, ""

                #solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) <= 1)
                
            ''' minimize the costs '''
            #solver.Minimize(solver.Sum(objective_terms))
            prob.solve(PULP_CBC_CMD(msg=0))
            print ("Status:", LpStatus[prob.status])
            
            results = []
            for v in prob.variables():
                result = {}
                result["airline"] = airlineName
                result["status"] = str(LpStatus[prob.status])
                result["aircraft"] = str(v.name).split("_")[0]
                
                result["Adep"] = str(v.name).split("_")[1]
                result["Ades"] = str(v.name).split("_")[2]
                print ( v.name, "=", v.varValue )
                if ( v.varValue > 0.0 ):
                    result["assigned"] = "yes"
                    results.append(result)
                else:
                    result["assigned"] = "no"
                

            # The optimized objective function value is printed to the screen
            #print ( "Total Cost  = ", value(prob.objective))
            
            return JsonResponse({'results': results})


        else:
            return JsonResponse({'errors': "unknown airline = {0}".format(airlineName)})

    else:
        return JsonResponse({'errors': "expecting GET method"})
        

