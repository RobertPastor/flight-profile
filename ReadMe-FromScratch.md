## installation

Windows PowerShell
Copyright (C) Microsoft Corporation. Tous droits réservés.

Installez la dernière version de PowerShell pour de nouvelles fonctionnalités et améliorations ! https://aka.ms/PSWindows

PS C:\Users\rober> pip install django==3.2
Collecting django==3.2
  Downloading Django-3.2-py3-none-any.whl (7.9 MB)
     ---------------------------------------- 7.9/7.9 MB 50.5 MB/s eta 0:00:00
Collecting asgiref<4,>=3.3.2
  Downloading asgiref-3.7.1-py3-none-any.whl (24 kB)
Collecting pytz
  Downloading pytz-2023.3-py2.py3-none-any.whl (502 kB)
     ---------------------------------------- 502.3/502.3 kB 32.8 MB/s eta 0:00:00
Collecting sqlparse>=0.2.2
  Downloading sqlparse-0.4.4-py3-none-any.whl (41 kB)
     ---------------------------------------- 41.2/41.2 kB ? eta 0:00:00
Installing collected packages: pytz, sqlparse, asgiref, django
Successfully installed asgiref-3.7.1 django-3.2 pytz-2023.3 sqlparse-0.4.4

[notice] A new release of pip available: 22.3.1 -> 23.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip
PS C:\Users\rober>
PS C:\Users\rober> pip install xlrd
Collecting xlrd
  Downloading xlrd-2.0.1-py2.py3-none-any.whl (96 kB)
     ---------------------------------------- 96.5/96.5 kB ? eta 0:00:00
Installing collected packages: xlrd
Successfully installed xlrd-2.0.1

[notice] A new release of pip available: 22.3.1 -> 23.1.2
[notice] To update, run: python.exe -m pip install --upgrade pip
PS C:\Users\rober> python.exe -m pip install --upgrade pip
Requirement already satisfied: pip in c:\users\rober\appdata\local\programs\python\python311\lib\site-packages (22.3.1)
Collecting pip
  Downloading pip-23.1.2-py3-none-any.whl (2.1 MB)
     ---------------------------------------- 2.1/2.1 MB 43.7 MB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 22.3.1
    Uninstalling pip-22.3.1:
      Successfully uninstalled pip-22.3.1
Successfully installed pip-23.1.2
PS C:\Users\rober> pip install psycopg2
Collecting psycopg2
  Downloading psycopg2-2.9.6-cp311-cp311-win_amd64.whl (1.2 MB)
     ---------------------------------------- 1.2/1.2 MB 72.0 MB/s eta 0:00:00
Installing collected packages: psycopg2
Successfully installed psycopg2-2.9.6
PS C:\Users\rober> pip install xmltodict
Collecting xmltodict
  Downloading xmltodict-0.13.0-py2.py3-none-any.whl (10.0 kB)
Installing collected packages: xmltodict
Successfully installed xmltodict-0.13.0
PS C:\Users\rober> pip install pandas
Collecting pandas
  Downloading pandas-2.0.1-cp311-cp311-win_amd64.whl (10.6 MB)
     ---------------------------------------- 10.6/10.6 MB 50.3 MB/s eta 0:00:00
Collecting python-dateutil>=2.8.2 (from pandas)
  Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
     ---------------------------------------- 247.7/247.7 kB 14.8 MB/s eta 0:00:00
Requirement already satisfied: pytz>=2020.1 in c:\users\rober\appdata\local\programs\python\python311\lib\site-packages (from pandas) (2023.3)
Collecting tzdata>=2022.1 (from pandas)
  Downloading tzdata-2023.3-py2.py3-none-any.whl (341 kB)
     ---------------------------------------- 341.8/341.8 kB 22.1 MB/s eta 0:00:00
Collecting numpy>=1.21.0 (from pandas)
  Downloading numpy-1.24.3-cp311-cp311-win_amd64.whl (14.8 MB)
     ---------------------------------------- 14.8/14.8 MB 46.7 MB/s eta 0:00:00
Collecting six>=1.5 (from python-dateutil>=2.8.2->pandas)
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: tzdata, six, numpy, python-dateutil, pandas
Successfully installed numpy-1.24.3 pandas-2.0.1 python-dateutil-2.8.2 six-1.16.0 tzdata-2023.3
PS C:\Users\rober>
PS C:\Users\rober>
PS C:\Users\rober> pip install xlsxwriter
Collecting xlsxwriter
  Downloading XlsxWriter-3.1.1-py3-none-any.whl (152 kB)
     ---------------------------------------- 152.9/152.9 kB 9.5 MB/s eta 0:00:00
Installing collected packages: xlsxwriter
Successfully installed xlsxwriter-3.1.1
PS C:\Users\rober> pip install pulp
Collecting pulp
  Downloading PuLP-2.7.0-py3-none-any.whl (14.3 MB)
     ---------------------------------------- 14.3/14.3 MB 46.7 MB/s eta 0:00:00
Installing collected packages: pulp
Successfully installed pulp-2.7.0
PS C:\Users\rober> pip install whitenoise
Collecting whitenoise
  Downloading whitenoise-6.4.0-py3-none-any.whl (19 kB)
Installing collected packages: whitenoise
Successfully installed whitenoise-6.4.0
PS C:\Users\rober>


## install postgres for the development environment and configure a database

error -> 
django.db.utils.ProgrammingError: relation "airline_airline" does not exist
LINE 1: ...ees", "airline_airline"."MaxLatitudeDegrees" FROM "airline_a...

## create the tables 

python manage.py makemigrations
python manage.py migrate


PS C:\Users\rober\git\flight-profile> python manage.py makemigrations
System check identified some issues:

WARNINGS:
airline.Airline: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the AirlineConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
airline.AirlineAircraft: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the AirlineConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
airline.AirlineCosts: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the AirlineConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
airline.AirlineRoute: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the AirlineConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
airline.AirlineRouteWayPoints: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the AirlineConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
trajectory.AirlineRunWay: (models.W042) Auto-created primary key used when not defining a primary key type, by default 'django.db.models.AutoField'.
        HINT: Configure the DEFAULT_AUTO_FIELD setting or the TrajectoryConfig.default_auto_field attribute to point to a subclass of AutoField, e.g. 'django.db.models.BigAutoField'.
No changes detected
PS C:\Users\rober\git\flight-profile>

## add in settings

DEFAULT_AUTO_FIELD = 'django.db.models.AutoField'

## create the tables

PS C:\Users\rober\git\flight-profile>
PS C:\Users\rober\git\flight-profile> python manage.py makemigrations
No changes detected
PS C:\Users\rober\git\flight-profile> python manage.py migrate
Operations to perform:
  Apply all migrations: admin, airline, auth, contenttypes, sessions, trajectory
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying auth.0001_initial... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying airline.0001_initial... OK
  Applying airline.0002_auto_20220903_2115... OK
  Applying airline.0003_airlineroute_airline... OK
  Applying airline.0004_auto_20221210_1528... OK
  Applying airline.0005_airlinecosts... OK
  Applying airline.0006_airlinecosts_finallengthmeters... OK
  Applying airline.0007_auto_20230429_2104... OK
  Applying airline.0008_airlineaircraft_turnaroundtimesminutes... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying sessions.0001_initial... OK
  Applying trajectory.0001_initial... OK
  Applying trajectory.0002_auto_20220227_2053... OK
  Applying trajectory.0003_waypoint_continent... OK
  Applying trajectory.0004_airport... OK
  Applying trajectory.0005_runway... OK
  Applying trajectory.0006_auto_20220422_2214... OK
  Applying trajectory.0007_kmloutputfile... OK
  Applying trajectory.0008_delete_kmloutputfile... OK
PS C:\Users\rober\git\flight-profile>

## launch creation of the different airlines

python manage.py AirlineDatabaseLoad

PS C:\Users\rober\git\flight-profile> python manage.py AirlineDatabaseLoad
AmericanWings
EuropeanWings
IndianWings
PS C:\Users\rober\git\flight-profile>

## create fleet



## warning - need to create the BADA aircrafts to get the fleet data as some are coming from the aircraft such as mass

PS C:\Users\rober\git\flight-profile> python manage.py BadaAircraftDatabaseLoad
BadaAircraftDatabase: file folder= C:\Users\rober\git\flight-profile\trajectory\management\commands\BadaAircraftDatabase
BadaAircraftDatabase: file path= C:\Users\rober\git\flight-profile\trajectory\management\commands\BadaAircraftDatabase\SYNONYM.NEW
acBD exists
BadaAircraftDatabase: opening file=  C:\Users\rober\git\flight-profile\trajectory\management\commands\BadaAircraftDatabase\SYNONYM.NEW
BadaAircraftDatabase: number of aircrafts in db= 322
read aircraft database result = True
PS C:\Users\rober\git\flight-profile>

## open PostGres PgAdmin and check the BADA aircraft table

## load the airline routes

PS C:\Users\rober\git\flight-profile> python manage.py AirlineRoutesDatabaseLoad
AirlineRoutesDataBaseXlsx: file folder= C:\Users\rober\git\flight-profile\airline\management\commands\AirlineRoutes
AirlineRoutesDataBaseXlsx: file path= C:\Users\rober\git\flight-profile\airline\management\commands\AirlineRoutes\AirlineRoutesAirportsDepartureArrival.xlsx
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
PS C:\Users\rober\git\flight-profile>


## need to load the airports database with latitude longitude to see the airports on the map

PS C:\Users\rober\git\flight-profile> python manage.py AirportsDatabaseLoad
AirportsDatabase: file folder= C:\Users\rober\git\flight-profile\trajectory\management\commands\Airports
AirportsDatabase: file path= C:\Users\rober\git\flight-profile\trajectory\management\commands\Airports\Airports.csv
airports database exists
read airports database result = True
PS C:\Users\rober\git\flight-profile>

## open PgAdmin to see the airline routes and the airports table content



