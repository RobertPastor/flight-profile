
# launch in gitbash
# ensure that the local host is running properly

# airlineURLs
curl -v "http://localhost:8000/airline/airlineFleet/AmericanWings" -o result-001.json


curl -v "http://localhost:8000/airline/airlineRoutes/AmericanWings" -o result-002.json


curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KLAX" -o result-003.json


curl -v "http://localhost:8000/airline/airlineCosts/AmericanWings" -o result-004.json


curl -v "http://localhost:8000/airline/airlineCostsOptimization/AmericanWings"  -o result-005.json



# trajectory URLs

curl -v "http://localhost:8000/trajectory/airports/AmericanWings"  -o result-006.json


curl -v "http://localhost:8000/trajectory/waypoints/AmericanWings?minlatitude=-20&maxlatitude=60&minlongitude=-126&maxlongitude=-74"  -o result-007.json


curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=KLAX-KATL&AdepRwy=24R&AdesRwy=26L&mass=67000&fl=39000"  -o result-008.json


curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=MMMX-KSEA&AdepRwy=05L&AdesRwy=16L&mass=67000&fl=39000" -o result-009.json


curl -v "http://localhost:8000/trajectory/computeRunwayOvershoot/A332/KATL/08L/230" -o result-010.json


curl -v "http://localhost:8000/trajectory/fuelPlanner/AmericanWings" -o result-011.json


curl -v "http://localhost:8000/airline/airlineRoutes/AmericanWings" -o result-012.json

