
# add new departure and arrival airports to 
/flight-profile/airline/management/commands/AirlineRoutes/AirlineRoutesAirportsDepartureArrival.xlsx 

Use ICAO codes for the airports

# run the command : python manage.py AirlineRoutesDatabaseLoad

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> python manage.py AirlineRoutesDatabaseLoad
airline routes database exists
Index is: 0
ID is: 0 - Airline is: AmericanWings - Departure Airport = KATL
ID is: 0 - Airline is: AmericanWings - Arrival AIrport = KLAX
departure airport= KATL - arrival airport= KLAX
Index is: 1
ID is: 1 - Airline is: AmericanWings - Departure Airport = KJFK
ID is: 1 - Airline is: AmericanWings - Arrival AIrport = KSEA
departure airport= KJFK - arrival airport= KSEA
Index is: 2
ID is: 2 - Airline is: AmericanWings - Departure Airport = KATL
ID is: 2 - Airline is: AmericanWings - Arrival AIrport = KMSP
departure airport= KATL - arrival airport= KMSP
Index is: 3
ID is: 3 - Airline is: AmericanWings - Departure Airport = KBOS
ID is: 3 - Airline is: AmericanWings - Arrival AIrport = KATL
departure airport= KBOS - arrival airport= KATL
Index is: 4
ID is: 4 - Airline is: AmericanWings - Departure Airport = KIAH
ID is: 4 - Airline is: AmericanWings - Arrival AIrport = KORD
departure airport= KIAH - arrival airport= KORD
Index is: 5
ID is: 5 - Airline is: AmericanWings - Departure Airport = KIAD
ID is: 5 - Airline is: AmericanWings - Arrival AIrport = KSFO
departure airport= KIAD - arrival airport= KSFO
Index is: 6
ID is: 6 - Airline is: AmericanWings - Departure Airport = PANC
ID is: 6 - Airline is: AmericanWings - Arrival AIrport = KATL
departure airport= PANC - arrival airport= KATL
Index is: 7
ID is: 7 - Airline is: AmericanWings - Departure Airport = KLAX
ID is: 7 - Airline is: AmericanWings - Arrival AIrport = KATL
departure airport= KLAX - arrival airport= KATL
Index is: 8
ID is: 8 - Airline is: AmericanWings - Departure Airport = KSEA
ID is: 8 - Airline is: AmericanWings - Arrival AIrport = KJFK
departure airport= KSEA - arrival airport= KJFK
Index is: 9
ID is: 9 - Airline is: AmericanWings - Departure Airport = KMSP
ID is: 9 - Airline is: AmericanWings - Arrival AIrport = KATL
departure airport= KMSP - arrival airport= KATL
Index is: 10
ID is: 10 - Airline is: AmericanWings - Departure Airport = KATL
ID is: 10 - Airline is: AmericanWings - Arrival AIrport = KBOS
departure airport= KATL - arrival airport= KBOS
Index is: 11
ID is: 11 - Airline is: AmericanWings - Departure Airport = KORD
ID is: 11 - Airline is: AmericanWings - Arrival AIrport = KIAH
departure airport= KORD - arrival airport= KIAH
Index is: 12
ID is: 12 - Airline is: AmericanWings - Departure Airport = KSFO
ID is: 12 - Airline is: AmericanWings - Arrival AIrport = KIAD
departure airport= KSFO - arrival airport= KIAD
Index is: 13
ID is: 13 - Airline is: AmericanWings - Departure Airport = KATL
ID is: 13 - Airline is: AmericanWings - Arrival AIrport = PANC
departure airport= KATL - arrival airport= PANC
Index is: 14
ID is: 14 - Airline is: AmericanWings - Departure Airport = KJFK
ID is: 14 - Airline is: AmericanWings - Arrival AIrport = LFPG
departure airport= KJFK - arrival airport= LFPG
Index is: 15
ID is: 15 - Airline is: EuropeanWings - Departure Airport = LFPG
ID is: 15 - Airline is: EuropeanWings - Arrival AIrport = LPPT
departure airport= LFPG - arrival airport= LPPT
Index is: 16
ID is: 16 - Airline is: EuropeanWings - Departure Airport = LFPG
ID is: 16 - Airline is: EuropeanWings - Arrival AIrport = LFML
departure airport= LFPG - arrival airport= LFML
Index is: 17
ID is: 17 - Airline is: EuropeanWings - Departure Airport = LFOB
ID is: 17 - Airline is: EuropeanWings - Arrival AIrport = LHBP
departure airport= LFOB - arrival airport= LHBP
Index is: 18
ID is: 18 - Airline is: EuropeanWings - Departure Airport = LHBP
ID is: 18 - Airline is: EuropeanWings - Arrival AIrport = LFOB
departure airport= LHBP - arrival airport= LFOB
Index is: 19
ID is: 19 - Airline is: IndianWings - Departure Airport = VOBL
ID is: 19 - Airline is: IndianWings - Arrival AIrport = VIDP
departure airport= VOBL - arrival airport= VIDP
Index is: 20
ID is: 20 - Airline is: IndianWings - Departure Airport = VABB
ID is: 20 - Airline is: IndianWings - Arrival AIrport = VECC
departure airport= VABB - arrival airport= VECC
Index is: 21
ID is: 21 - Airline is: IndianWings - Departure Airport = VOMM
ID is: 21 - Airline is: IndianWings - Arrival AIrport = VIJP
departure airport= VOMM - arrival airport= VIJP
read airline routes database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

# run airline airports to fill the latitude longitude for the new airports

python manage.py AirportsDatabaseLoad

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> python manage.py AirportsDatabaseLoad
airports database exists
read airports database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

launch the application and check the airports.

# add the two route waypoints xlsx files in /flight-profile/airline/management/commands/AirlineRoutesWayPoints

/flight-profile/airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VABB-VECC.xlsx

/flight-profile/airline/management/commands/AirlineRoutesWayPoints/AirlineRoute-VOMM-VIJP.xlsx

# do not forget to name the sheet as "wayPoints"

# launch the following command to update the target WayPoints xlsx file

python manage.py AirlineRoutesWayPointsDatabaseLoad

this command creates the WayPoints.xlsx database

# move the updated WayPoints.xls to /flight-profile/trajectory/management/commands/WayPoints

# launch the following command to update the Django database with the new WayPoints

python manage.py WayPointsDatabaseLoad

# launch the following command to update the Django database with the new RunWays

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> python manage.py RunWaysDatabaseLoad
RunWaysDatabase: file folder= C:\Users\rober\Documents\04 - Workspace\flight-profile\trajectory\management\commands\RunWays
RunWaysDatabase: file path= C:\Users\rober\Documents\04 - Workspace\flight-profile\trajectory\management\commands\RunWays\RunWays.xls
runwaysDB exists
C:\Users\rober\Documents\04 - Workspace\flight-profile\trajectory\management\commands\RunWays\RunWays.xls
airport = KATL
KATL/08L
airport = KATL
KATL/08R
airport = KATL
KATL/09L
airport = KATL
KATL/09R
airport = KATL
KATL/10
airport = KBOS
KBOS/04L
airport = KBOS
KBOS/04R
airport = KBOS
KBOS/09
airport = KBOS
KBOS/14
airport = KBOS
KBOS/15L
airport = KBOS
KBOS/15R
airport = KIAD
KIAD/01C
airport = KIAD
KIAD/01L
airport = KIAD
KIAD/01R
airport = KIAD
KIAD/12
airport = KIAH
KIAH/08L
airport = KIAH
KIAH/08R
airport = KIAH
KIAH/09
airport = KIAH
KIAH/15L
airport = KIAH
KIAH/15R
airport = KJFK
KJFK/04L
airport = KJFK
KJFK/04R
airport = KJFK
KJFK/13L
airport = KJFK
KJFK/13R
airport = KLAX
KLAX/06L
airport = KLAX
KLAX/06R
airport = KLAX
KLAX/07L
airport = KLAX
KLAX/07R
airport = KMSP
KMSP/04
airport = KMSP
KMSP/12L
airport = KMSP
KMSP/12R
airport = KMSP
KMSP/17
airport = KORD
KORD/04L
airport = KORD
KORD/04R
airport = KORD
KORD/09L
airport = KORD
KORD/09R
airport = KORD
KORD/10C
airport = KORD
KORD/10L
airport = KORD
KORD/10R
airport = KORD
KORD/14L
airport = KORD
KORD/15
airport = KORD
KORD/18
airport = KSEA
KSEA/16C
airport = KSEA
KSEA/16L
airport = KSEA
KSEA/16R
airport = KSFO
KSFO/01L
airport = KSFO
KSFO/01R
airport = KSFO
KSFO/10L
airport = KSFO
KSFO/10R
airport = LFML
LFML/13L
airport = LFML
LFML/13R
airport = LFOB
LFOB/04
airport = LFOB
LFOB/12
airport = LFPG
LFPG/08L
airport = LFPG
LFPG/08R
airport = LFPG
LFPG/09L
airport = LFPG
LFPG/09R
airport = LHBP
LHBP/13L
airport = LHBP
LHBP/13R
airport = LPPT
LPPT/02
airport = LPPT
LPPT/17
airport = PANC
PANC/07L
airport = PANC
PANC/07R
airport = PANC
PANC/15
airport = VABB
VABB/09
airport = VABB
VABB/14
airport = VECC
VECC/01L
airport = VECC
VECC/01R
airport = VIDP
VIDP/09
airport = VIDP
VIDP/10
airport = VIDP
VIDP/11
airport = VIJP
VIJP/09
airport = VIJP
VIJP/15
airport = VOBL
VOBL/09L
airport = VOBL
VOBL/09R
airport = VOMM
VOMM/07
airport = VOMM
VOMM/12
read runways database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

# update the costs database as it updates the Django database

python manage.py AirlineCostsDatabaseCompute


