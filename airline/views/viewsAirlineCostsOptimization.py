'''
Created on 29 janv. 2023

@author: robert
'''

#from ortools.linear_solver import pywraplp
from pulp import LpProblem , LpMinimize ,  LpVariable, LpInteger, lpSum, LpStatus ,  PULP_CBC_CMD, value
from django.http import  JsonResponse

import logging
from pulp.constants import LpBinary
logger = logging.getLogger(__name__)
from airline.models import Airline, AirlineCosts, AirlineAircraft, AirlineRoute

from airline.views.utils import compute_total_costs
from airline.models import AirlineAircraftInstances

def check_constraints(prob, c_list):
    if prob.objective:
        for c in c_list:
            if '=' not in str(c):
                print ('no operator found in constraint')
                break
            else:
                prob.addConstraint(c)
    else:
        print ('Please define an objective before you define constraints')

def getCostsOptimization(request, airlineName):
    logger.debug ("get Airline Fleet for airline = {0}".format(airlineName))
    
    if (request.method == 'GET'):
        
        
        #solver_list = listSolvers(onlyAvailable=True)
        #print (solver_list)
        
        airline = Airline.objects.all().filter(Name=airlineName).first()
        if airline:
            
            nbFligthtLegs = AirlineRoute.objects.filter(airline=airline).count()
            aircraftInstances = AirlineAircraftInstances()
            aircraftInstancesList = aircraftInstances.computeAirlineAircraftInstances(airlineName , nbFligthtLegs)
            print ( aircraftInstancesList )
            
            print ( "length of flight legs = {0}".format( AirlineRoute.objects.filter(airline=airline).count() ) )
            
            airlineCostsArray = []
            airlineAircraftICAOcodeList = []
            airlineAircraftFullNameList = []
            #for airlineAircraft in AirlineAircraft.objects.filter(airline=airline):
            for aircraftInstance in aircraftInstancesList:
                
                acICAOcode = aircraftInstances.getAircraftInstanceICAOcode(aircraftInstance)
                airlineAircraft = AirlineAircraft.objects.filter(airline=airline , aircraftICAOcode=acICAOcode).first()
                
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
                        
                        totalCostsUSdollars = compute_total_costs( airlineCosts, airlineAircraft )
                        
                        #print ( "{0} - {1} - {2}".format(airlineAircraft.aircraftICAOcode, airlineRoute.getFlightLegAsString() , type(totalCostsUSdollars) ))
                            
                        aircraftCostsArray.append( float(totalCostsUSdollars) )
                        
                airlineCostsArray.append(aircraftCostsArray)
                
            print ( airlineCostsArray )
            #print ( "number of aircrafts = {0}".format( len( AirlineAircraft.objects.filter(airline=airline) ) ) )
            #print ( "number of routes = {0}".format( len( AirlineRoute.objects.filter(airline=airline) ) ) )
            
            '''  x[i, j] is an array of 0-1 variables, which will be 1 '''
            '''  if worker i is assigned to task j. '''
            #num_aircrafts = len( AirlineAircraft.objects.filter(airline=airline) )
            num_flight_legs = len( AirlineRoute.objects.filter(airline=airline) )
            
            #num_aircrafts = len(airlineCostsArray)
            num_aircraft_instances = len(aircraftInstancesList)
            print ( "number of aircraft instances = {0}".format( num_aircraft_instances ))
            num_flight_legs = len(airlineCostsArray[0])
            #print ( num_flight_legs )
            
            ''' Create the MIP solver with the SCIP back-end '''
            #solver = pywraplp.Solver.CreateSolver('SCIP')
            prob = LpProblem("AssignmentProblem", LpMinimize)
            
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
                    
            
            ''' --------- objective function --------------'''
            for i in range(num_aircraft_instances):
                for j in range(num_flight_legs):
                    pass
                    #objective_terms.append(float(airlineCostsArray[i][j]) * x[i, j])
            prob += lpSum( [ airlineCostsArray[i][j] * x_vars[i,j] for i in range(num_aircraft_instances) for j in range(num_flight_legs) ])
                    
            print ("--- add constraints ----")
            '''  Each aircraft is assigned to at most 1 flight leg. '''
            for i in range(num_aircraft_instances):
                pass
                #solver.Add(solver.Sum([x[i, j] for j in range(num_flight_legs)]) <= 1)
                prob += lpSum( [ x_vars[i,j] for j in range(num_flight_legs) ] ) <= 1
                #c_list = lpSum ( [x_vars[i,j] for j in range(num_flight_legs)] ) <= 1
                #check_constraints(prob, c_list)
                
            ''' Each flight leg is assigned to exactly one aircraft '''
            for j in range(num_flight_legs):
                pass
                prob += lpSum ( [ x_vars[i,j] for i in range(num_aircraft_instances) ] ) == 1
                #check_constraints(prob, c_list)

                #solver.Add(solver.Sum([x[i, j] for i in range(num_aircrafts)]) <= 1)
                
            ''' minimize the costs '''
            #solver.Minimize(solver.Sum(objective_terms))
            prob.solve(PULP_CBC_CMD(msg=0))
            print ("Status:", LpStatus[prob.status])
            
            #for name, c in list(prob.constraints.items()):
            #    print(name, ":", c, "\t", c.pi, "\t\t", c.slack)
            
            prob.writeLP("pulp_problem.lp", writeSOS=1, mip=1 )
            
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
                        airlineCosts = AirlineCosts.objects.filter(airline=airline, airlineAircraft=airlineAircraft, airlineRoute=airlineRoute).first()
                        if airlineCosts:
                            
                            totalCostsUSdollars = compute_total_costs(airlineCosts, airlineAircraft )
                            result["costs"] = round ( totalCostsUSdollars , 2 )

                
                if ( v.varValue > 0.0 ):
                    print ( v.name, "=", v.varValue )
                    result["assigned"] = "yes"
                    results.append(result)
                else:
                    result["assigned"] = "no"
                

            # The optimized objective function value is printed to the screen
            print ( "Total Cost  = ", value(prob.objective))
            
            return JsonResponse({'results': results})


        else:
            return JsonResponse({'errors': "unknown airline = {0}".format(airlineName)})

    else:
        return JsonResponse({'errors': "expecting GET method"})
        

