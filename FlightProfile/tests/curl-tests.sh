
# launch in gitbash
# ensure that the local host is running properly

# airlineURLs
curl -v "http://localhost:8000/airline/airlineFleet/AmericanWings"


curl -v "http://localhost:8000/airline/airlineRoutes/AmericanWings"


curl -v "http://localhost:8000/airline/wayPointsRoute/KATL/KLAX"


curl -v "http://localhost:8000/airline/airlineCosts/AmericanWings"


curl -v "http://localhost:8000/airline/airlineCostsOptimization/AmericanWings"



# trajectory URLs

curl -v "http://localhost:8000/trajectory/airports/AmericanWings"


curl -v "http://localhost:8000/trajectory/waypoints/AmericanWings?minlatitude=-20&maxlatitude=60&minlongitude=-126&maxlongitude=-74"


curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=KLAX-KATL&AdepRwy=24R&AdesRwy=26L&mass=67000&fl=39000"


curl -v "http://localhost:8000/trajectory/computeFlightProfile/AmericanWings?aircraft=A320&route=MMMX-KSEA&AdepRwy=05L&AdesRwy=16L&mass=67000&fl=39000"


curl -v "http://localhost:8000/trajectory/computeRunwayOvershoot/A332/KATL/08L/230" 


curl -v "http://localhost:8000/trajectory/fuelPlanner/AmericanWings" 


curl -v "http://localhost:8000/airline/airlineRoutes/AmericanWings"

