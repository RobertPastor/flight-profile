
# add new departure and arrival airports to 

/flight-profile/airline/management/commands/AirlineRoutes/AirlineRoutesAirportsDepartureArrival.xlsx 

Use ICAO codes for the airports

# extend the list of routes

python manage.py AirlineRoutesDatabaseLoad
airline routes database exists
Index is: 0
ID is: 0 - Airline is: AmericanWings - Departure Airport = KATL
ID is: 0 - Airline is: AmericanWings - Arrival AIrport = KLAX
departure airport= KATL - arrival airport= KLAX
Index is: 1
..............


Index is: 21
ID is: 21 - Airline is: IndianWings - Departure Airport = VOMM
ID is: 21 - Airline is: IndianWings - Arrival AIrport = VIJP
departure airport= VOMM - arrival airport= VIJP
read airline routes database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

# run airline airports to fill the latitude longitude for the new airports

python manage.py AirportsDatabaseLoad

airports database exists
read airports database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

launch the application and check the airports, the new airports should appear on the map

# add the two route waypoints xlsx files in /flight-profile/airline/management/commands/AirlineRoutesWayPoints

/flight-profile/airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VABB-VECC.xlsx

/flight-profile/airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VOMM-VIJP.xlsx

## do not forget to name the sheet as "wayPoints"
## do not forget to suppress the departure and arrival airports

# launch the following command to update the database with the new airline route

python manage.py AirlineRoutesWayPointsDatabaseLoad

## launch the following command to update the target WayPoints xlsx file
## this should be needed only in the development environment as the WayPoints.xlsx file is moved to the trajectory folder

python manage.py WayPointsXlsxFileCreate

this command creates the WayPoints.xlsx database

## move the updated WayPoints.xls to /flight-profile/trajectory/management/commands/WayPoints

## launch the following command to update the Django database with the new WayPoints

python manage.py WayPointsDatabaseLoad

# launch the following command to update the Django database with the new RunWays

python manage.py RunWaysDatabaseLoad

RunWaysDatabase: file folder= C:\Users\rober\Documents\04 - Workspace\flight-profile\trajectory\management\commands\RunWays
RunWaysDatabase: file path= C:\Users\rober\Documents\04 - Workspace\flight-profile\trajectory\management\commands\RunWays\RunWays.xls
runwaysDB exists
C:\Users\rober\Documents\04 - Workspace\flight-profile\trajectory\management\commands\RunWays\RunWays.xls
airport = KATL
KATL/08L
...

added MMMX airport and 2 runways for the Mexico airport

airport = VOMM
VOMM/07
airport = VOMM
VOMM/12
read runways database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

## launch an update of the SID STAR that are depending upon the airports, and runways and waypoints

python manage.py SidStarDatabaseLoad

using PgAdmin check the SID STAR database table

the same command is loading also the SID STAR waypoints
using PgAdmin check the SID STAR waypoints database table



## update the costs database as it updates the Django database

python manage.py AirlineCostsDatabaseCompute


