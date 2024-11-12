## add the new route to AirlineRoutesAirportsDepartureArrival.xlsx

Airline			Departure Airport	Departure Airport ICAO Code			Arrival Airport					Arrival Airport ICAO Code
EuropeanWings	Faro-Portugal		LPFR								Brussels-National				EBBR

## run the python manage.py command to load the new route

python manage.py AirlineRoutesDatabaseLoad


## query the database and check that the new route has been added

SELECT * FROM public.airline_airlineroute
ORDER BY id ASC 


## add the "new" waypoint names to a new route EXCEL file

--> create the EXCEL file --> AirlineRoute-LPFR-EBBR.xlsx
--> do not forget to ESCAPE the single quote '

order		wayPoint	latitude	longitude
1	VFA		N37°00\'48.99"	W007°58\'30.00"
2	MINTA	N37°07\'43.99"	W007°22\'59.99"
3	OSLEP	N37°09\'54.99"	W007°11\'30.99"
4	OXACA	N37°57\'00.00"	W006°00\'00.00"
5	DIONY	N38°35\'49.99"	W005°28\'36.99"
6	PARKA	N39°00\'00.00"	W005°09\'00.00"
7	TLD		N39°58\'09.99"	W004°20\'15.00"
8	SIE		N41°09\'05.99"	W003°36\'16.99"
9	EDIGO	N41°30\'15.00"	W003°24\'41.99"
10	DGO		N42°27\'11.99"	W002°52\'51.00"
11	ABRIX	N43°38\'47.00"	W001°57\'44.99"
12	ASKAN	N45°02\'39.99"	W001°02\'22.99"
13	ETPAR	N45°11\'44.99"	W000°51\'42.00"
14	POI		N46°34\'52.00"	E000°17\'52.99"
15	BOKNO	N47°02\'48.99"	E000°41\'30.00"
16	DEVRO	N47°29\'43.99"	E000°44\'18.99"
17	VANAD	N47°50\'14.00"	E000°54\'26.00"
18	PIWIZ	N48°12\'54.00"	E001°05\'55.99"
19	VADOM	N48°33\'01.99"	E001°16\'14.99"
20	BAMES	N48°58\'30.99"	E001°29\'10.00"
21	ARSAF	N49°21\'03.00"	E002°08\'03.00"
22	KOPOR	N49°30\'50.99"	E002°25\'17.00"
23	EGOZE	N49°33\'09.99"	E002°29\'22.00"
24	NURMO	N49°49\'33.99"	E002°45\'18.99"
25	PERON	N49°54\'45.00"	E002°50\'23.99"
26	SULEX	N50°00\'00.00"	E002°55\'31.99"
27	CMB		N50°13\'41.00"	E003°09\'05.00"
28	VEKIN	N50°24\'14.99"	E003°16\'29.99"
29	ARVOL	N50°32\'45.00"	E003°29\'48.99"

## analyse the new route file and add the new route

$ python manage.py AirlineRoutesWayPointsDatabaseLoad

## check the content of database (local database is a PostGres one)

SELECT * FROM public.airline_airlineroutewaypoints as h1
where h1."Route_id" = 50
ORDER BY id ASC 

check the route with same id and the new waypoints in the adequate order

"id"	"Order"	"WayPoint"	"Route_id"
11110	0	"VFA"	50
11111	1	"MINTA"	50
11112	2	"OSLEP"	50
11113	3	"OXACA"	50
11114	4	"DIONY"	50
11115	5	"PARKA"	50


## create WayPoints.xlsx

python manage.py WayPointsXlsxFileCreate

...

12 - order                    13
wayPoint              INTIL
latitude      N26▒27'51.00"
longitude    E076▒32'40.99"
Name: 12, dtype: object
file = C:\Users\rober\git\flight-profile\airline\management\commands\AirlineRoutesWayPoints\WayPoints.xlsx created correctly

rober@RobertPastor MINGW64 ~/git/flight-profile (master)
$

## check the updated waypoints.xlsx file in the target folder

the generated WayPoints.xlsx must be copied from source repo 
/flight-profile/airline/management/commands/AirlineRoutesWayPoints 
to the target repo 
/flight-profile/trajectory/management/commands/WayPoints


## launch the database waypoints load (from the EXCEL waypoints file)

rober@RobertPastor MINGW64 ~/git/flight-profile (master)
$ python manage.py WayPointsDatabaseLoad

## check the updated waypoints in the database (local database is PostGres SQL)

SELECT * FROM public.trajectory_airlinewaypoint
where "WayPointName" = 'VFA'
ORDER BY "WayPointName" ASC 


"WayPointName"	"Type"	"Latitude"	"Longitude"	"Continent"
"VFA"	"WayPoint"	37.01360833333334	-7.9750000000000005	"Europe"

## launch the Airports load

python manage.py AirportsDatabaseLoad

{'Airport ID': '9414', 'Airport Name': 'Jimmy Carter Regional', 'City': 'Americus', 'Country': 'United States', 'IATA/FAA': 'ACJ', 'ICAO Code': 'KACJ', 'LatitudeDegrees': '32.0665', 'LongitudeDegrees': '-84.1133', 'AltitudeFeet': '468', 'TimeZone': '-5', 'DST': 'A'}
{'Airport ID': '9415', 'Airport Name': 'Weedon Field', 'City': 'Eufala', 'Country': 'United States', 'IATA/FAA': 'EUF', 'ICAO Code': 'KEUF', 'LatitudeDegrees': '31.5708', 'LongitudeDegrees': '-85.0774', 'AltitudeFeet': '285', 'TimeZone': '-6', 'DST': 'A'}
{'Airport ID': '9416', 'Airport Name': 'Saluda County', 'City': 'Saluda', 'Country': 'United States', 'IATA/FAA': '6J4', 'ICAO Code': 'K6J4', 'LatitudeDegrees': '33.5561', 'LongitudeDegrees': '-81.4768', 'AltitudeFeet': '539', 'TimeZone': '-5', 'DST': 'A'}
{'Airport ID': '9417', 'Airport Name': 'Dare County Regional', 'City': 'Manteo', 'Country': 'United States', 'IATA/FAA': 'MQI', 'ICAO Code': 'KMQI', 'LatitudeDegrees': '35.5514', 'LongitudeDegrees': '-75.4173', 'AltitudeFeet': '13', 'TimeZone': '-5', 'DST': 'A'}
{'Airport ID': '9418', 'Airport Name': 'Auburn University Regional', 'City': 'Auburn', 'Country': 'United States', 'IATA/FAA': 'AUO', 'ICAO Code': 'KAUO', 'LatitudeDegrees': '32.3691', 'LongitudeDegrees': '-85.2604', 'AltitudeFeet': '777', 'TimeZone': '-6', 'DST': 'A'}
{'Airport ID': '9419', 'Airport Name': 'Tri-Cities', 'City': 'Endicott', 'Country': 'United States', 'IATA/FAA': 'CZG', 'ICAO Code': 'KCZG', 'LatitudeDegrees': '42.0471', 'LongitudeDegrees': '-76.0578', 'AltitudeFeet': '833', 'TimeZone': '-5', 'DST': 'A'}
read airports database result = True

rober@RobertPastor MINGW64 ~/git/flight-profile (master)

## update the Airports runways

python manage.py RunWaysDatabaseLoad

## check the runways in the SQL database

SELECT * FROM public.trajectory_airlinerunway
where "Airport_id" = 'EBBR'
ORDER BY id ASC 


"id"	"Name"	"LengthFeet"	"TrueHeadingDegrees"	"LatitudeDegrees"	"LongitudeDegrees"	"Airport_id"
1447	"01"	9800	14	50.88690185546875	4.491419792175293	"EBBR"
1448	"19"	9800	194	50.912899017333984	4.502019882202148	"EBBR"
1449	"07L"	11936	65	50.89889907836914	4.455659866333008	"EBBR"
1450	"25R"	11936	245	50.91260147094727	4.502630233764648	"EBBR"
1451	"07R"	10535	70	50.88899993896485	4.480420112609863	"EBBR"
1452	"25L"	10535	250	50.89889907836914	4.5233001708984375	"EBBR"



