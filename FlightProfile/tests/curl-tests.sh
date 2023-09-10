#!/bin/bash

# launch in gitbash
# ensure that the local host is running properly
# extended usage of API
# launch -> . ./curl-tests.sh


# airline URLs

curl -v "http://localhost:8000/airline/airlineFleet/AmericanWings" -o result-001-1.json
curl -v "http://localhost:8000/airline/airlineFleet/EuropeanWings" -o result-001-2.json
curl -v "http://localhost:8000/airline/airlineFleet/IndianWings"   -o result-001-3.json
curl -v "http://localhost:8000/airline/airlineFleet/UnknownWings"  -o result-001-4.json

curl -v "http://localhost:8000/airline/airlineRoutes/AmericanWings" -o result-002-1.json
curl -v "http://localhost:8000/airline/airlineRoutes/EuropeanWings" -o result-002-2.json
curl -v "http://localhost:8000/airline/airlineRoutes/IndianWings"   -o result-002-3.json
curl -v "http://localhost:8000/airline/airlineRoutes/UnknownWings"  -o result-002-4.json

curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KLAX"    -o result-003-1.json
curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KBOS"    -o result-003-2.json
curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KMSP"    -o result-003-3.json
curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/PANC"    -o result-003-4.json

curl -v "http://localhost:8000/airline/airlineCosts/AmericanWings" -o result-004-1.json
curl -v "http://localhost:8000/airline/airlineCosts/EuropeanWings" -o result-004-2.json
curl -v "http://localhost:8000/airline/airlineCosts/IndianWings"   -o result-004-3.json
curl -v "http://localhost:8000/airline/airlineCosts/UnknownWings"  -o result-004-4.json

curl -v "http://localhost:8000/airline/airlineCostsOptimization/AmericanWings"  -o result-005-1.json
curl -v "http://localhost:8000/airline/airlineCostsOptimization/EuropeanWings"  -o result-005-2.json
curl -v "http://localhost:8000/airline/airlineCostsOptimization/IndianWings"    -o result-005-3.json
curl -v "http://localhost:8000/airline/airlineCostsOptimization/UnknownWings"   -o result-005-4.json


# trajectory URLs

curl -v "http://localhost:8000/trajectory/airports/AmericanWings"  -o result-006-1.json
curl -v "http://localhost:8000/trajectory/airports/EuropeanWings"  -o result-006-2.json
curl -v "http://localhost:8000/trajectory/airports/IndianWings"    -o result-006-3.json
curl -v "http://localhost:8000/trajectory/airports/UnknownWings"   -o result-006-4.json

curl -v "http://localhost:8000/trajectory/waypoints/AmericanWings?minlatitude=-20&maxlatitude=60&minlongitude=-126&maxlongitude=-74"  -o result-007-1.json
curl -v "http://localhost:8000/trajectory/waypoints/EuropeanWings"  -o result-007-2.json
curl -v "http://localhost:8000/trajectory/waypoints/IndianWings"    -o result-007-3.json
curl -v "http://localhost:8000/trajectory/waypoints/UnknownWings"   -o result-007-4.json

curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=KLAX-KATL&AdepRwy=24R&AdesRwy=26L&mass=67000&fl=39000"  -o result-008.json

curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=MMMX-KSEA&AdepRwy=05L&AdesRwy=16L&mass=67000&fl=39000" -o result-009.json

curl -v "http://localhost:8000/trajectory/computeRunwayOvershoot/A332/KATL/08L/230" -o result-010.json

curl -v "http://localhost:8000/trajectory/fuelPlanner/AmericanWings" -o result-011.json

curl -v "http://localhost:8000/airline/airlineRoutes/AmericanWings" -o result-012.json
curl -v "http://localhost:8000/airline/airlineRoutes/EuropeanWings" -o result-012.json
curl -v "http://localhost:8000/airline/airlineRoutes/IndianWings" -o result-012.json

