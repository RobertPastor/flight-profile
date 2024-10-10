#!/bin/bash

# launch in gitbash
# ensure that the local host is running properly
# extended usage of API
# launch -> . ./curl-tests.sh


# airline URLs

curl -v "http://localhost:8000/airline/airlineFleet/AmericanWings" -o results/airlineFleet-001-1.json
curl -v "http://localhost:8000/airline/airlineFleet/EuropeanWings" -o results/airlineFleet-001-2.json
curl -v "http://localhost:8000/airline/airlineFleet/IndianWings"   -o results/airlineFleet-001-3.json
curl -v "http://localhost:8000/airline/airlineFleet/UnknownWings"  -o results/airlineFleet-001-4.json

curl -v "http://localhost:8000/airline/airlineRoutes/AmericanWings" -o results/airlineRoutes-002-1.json
curl -v "http://localhost:8000/airline/airlineRoutes/EuropeanWings" -o results/airlineRoutes-002-2.json
curl -v "http://localhost:8000/airline/airlineRoutes/IndianWings"   -o results/airlineRoutes-002-3.json
curl -v "http://localhost:8000/airline/airlineRoutes/UnknownWings"  -o results/airlineRoutes-002-4.json

curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KLAX"    -o results/wayPointsRoute-003-1.json
curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KBOS"    -o results/wayPointsRoute-003-2.json
curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KMSP"    -o results/wayPointsRoute-003-3.json
curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/PANC"    -o results/wayPointsRoute-003-4.json

curl -v "http://localhost:8000/airline/airlineCosts/AmericanWings" -o results/airlineCosts-004-1.json
curl -v "http://localhost:8000/airline/airlineCosts/EuropeanWings" -o results/airlineCosts-004-2.json
curl -v "http://localhost:8000/airline/airlineCosts/IndianWings"   -o results/airlineCosts-004-3.json
curl -v "http://localhost:8000/airline/airlineCosts/UnknownWings"  -o results/airlineCosts-004-4.json

curl -v "http://localhost:8000/airline/airlineCostsOptimization/AmericanWings"  -o results/airlineCostsOptimization-1.json
curl -v "http://localhost:8000/airline/airlineCostsOptimization/EuropeanWings"  -o results/airlineCostsOptimization-2.json
curl -v "http://localhost:8000/airline/airlineCostsOptimization/IndianWings"    -o results/airlineCostsOptimization-3.json
curl -v "http://localhost:8000/airline/airlineCostsOptimization/UnknownWings"   -o results/airlineCostsOptimization-4.json

curl -v "http://localhost:8000/airline/getAirlineCostsXlsx/AmericanWings"  -o results/Costs-AmericanWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineCostsXlsx/EuropeanWings"  -o results/Costs-EuropeanWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineCostsXlsx/IndianWings"    -o results/Costs-IndianWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineCostsXlsx/UnknownWings"   -o results/Costs-Errors.xlsx

curl -v "http://localhost:8000/airline/getAirlineCASM/AmericanWings"  -o results/getAirlineCASM-AmericanWings.json
curl -v "http://localhost:8000/airline/getAirlineCASM/EuropeanWings"  -o results/getAirlineCASM-EuropeanWings.json
curl -v "http://localhost:8000/airline/getAirlineCASM/IndianWings"    -o results/getAirlineCASM-IndianWings.json
curl -v "http://localhost:8000/airline/getAirlineCASM/UnknownWings"   -o results/getAirlineCASM-UnknownWings.json

curl -v "http://localhost:8000/airline/getAirlineCasmXlsx/AmericanWings"  -o results/CASM-AmericanWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineCasmXlsx/EuropeanWings"  -o results/CASM-EuropeanWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineCasmXlsx/IndianWings"    -o results/CASM-IndianWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineCasmXlsx/UnknownWings"   -o results/CASM-Errors.xlsx

curl -v "http://localhost:8000/airline/getAirlineCasmOptimization/AmericanWings"  -o results/getAirlineCasmOptimization-1.json
curl -v "http://localhost:8000/airline/getAirlineCasmOptimization/EuropeanWings"  -o results/getAirlineCasmOptimization-2.json
curl -v "http://localhost:8000/airline/getAirlineCasmOptimization/IndianWings"    -o results/getAirlineCasmOptimization-3.json
curl -v "http://localhost:8000/airline/getAirlineCasmOptimization/UnknownWings"   -o results/getAirlineCasmOptimization-4.json

curl -v "http://localhost:8000/airline/getAirlineSeatMilesXlsx/AmericanWings"  -o results/getAirlineSeatMilesXlsx-AmericanWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineSeatMilesXlsx/EuropeanWings"  -o results/getAirlineSeatMilesXlsx-EuropeanWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineSeatMilesXlsx/IndianWings"    -o results/getAirlineSeatMilesXlsx-IndianWings.xlsx
curl -v "http://localhost:8000/airline/getAirlineSeatMilesXlsx/UnknownWings"   -o results/getAirlineSeatMilesXlsx-Errors.xlsx

# trajectory URLs

curl -v "http://localhost:8000/trajectory/airports/AmericanWings"  -o results/airports-006-1.json
curl -v "http://localhost:8000/trajectory/airports/EuropeanWings"  -o results/airports-006-2.json
curl -v "http://localhost:8000/trajectory/airports/IndianWings"    -o results/airports-006-3.json
curl -v "http://localhost:8000/trajectory/airports/UnknownWings"   -o results/airports-006-4.json

curl -v "http://localhost:8000/trajectory/waypoints/AmericanWings"  -o results/waypoints-007-1.json
curl -v "http://localhost:8000/trajectory/waypoints/EuropeanWings"  -o results/waypoints-007-2.json
curl -v "http://localhost:8000/trajectory/waypoints/IndianWings"    -o results/waypoints-007-3.json
curl -v "http://localhost:8000/trajectory/waypoints/UnknownWings"   -o results/waypoints-007-4.json

curl -v "http://localhost:8000/trajectory/launchFlightProfile/AmericanWings"  -o results/launchFlightProfile-AmericanWings-2.json
curl -v "http://localhost:8000/trajectory/launchFlightProfile/EuropeanWings"  -o results/launchFlightProfile-EuropeanWings-2.json
curl -v "http://localhost:8000/trajectory/launchFlightProfile/IndianWings"    -o results/launchFlightProfile-IndianWings-3.json
curl -v "http://localhost:8000/trajectory/launchFlightProfile/UnknownWings"   -o results/launchFlightProfile-UnknownWings-4.json

curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=KLAX-KATL&adepRwy=24R&adesRwy=26L&mass=67000&fl=39000"  -o results/computeFlightProfile-008.json

curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=MMMX-KSEA&adepRwy=05L&adesRwy=16L&mass=67000&fl=39000" -o results/computeFlightProfile-009.json

curl -v "http://localhost:8000/trajectory/computeCosts/AmericanWings?aircraft=A320&route=KLAX-KATL&adepRwy=24R&adesRwy=26L&mass=67000&fl=39000"  -o results/computeCosts-008.json

curl -v "http://localhost:8000/trajectory/computeCosts/AmericanWings?aircraft=A320&route=MMMX-KSEA&adepRwy=05L&adesRwy=16L&mass=67000&fl=39000" -o results/computeCosts-009.json

curl -v "http://localhost:8000/trajectory/fuelPlanner/AmericanWings" -o results/fuelPlanner-AmericanWings.json
curl -v "http://localhost:8000/trajectory/fuelPlanner/EuropeanWings" -o results/fuelPlanner-EuropeanWings.json
curl -v "http://localhost:8000/trajectory/fuelPlanner/IndianWings" -o results/fuelPlanner-IndianWings.json
curl -v "http://localhost:8000/trajectory/fuelPlanner/UnknownWings" -o results/fuelPlanner-UnknownWings.json

curl -v "http://localhost:8000/trajectory/computeRunwayOvershoot/A332/KATL/08L/230" -o results/computeRunwayOvershoot-010.json

curl -v "http://localhost:8000/trajectory/aircraft?aircraft=A320" -o results/aircraft-A320.json

#curl -v "http://localhost:8000/trajectory/metar/AmericanWings" -o results/metar-AmericanWings.json
#curl -v "http://localhost:8000/trajectory/metar/EuropeanWings" -o results/metar-EuropeanWings.json
#curl -v "http://localhost:8000/trajectory/metar/IndianWings" -o results/metar-IndianWings.json
#curl -v "http://localhost:8000/trajectory/metar/UnknownWings" -o results/metar-UnknownWings.json
