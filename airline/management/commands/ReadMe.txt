

# list the available commands
#============================

python manage.py help

# run one command
#================

python manage.py AirlineRoutesDatabaseLoad -a flight-profile 

python manage.py makemigrations -a flight-profile
python manage.py migrate -a flight-profile


# run command in local environment
#=================================

Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[airline]
    AirlineFleetDatabaseLoad
    AirlineRoutesDatabaseLoad
    
# run command in heroku
#=====================
heroku run python manage.py AirlineFleetDatabaseLoad -a flight-profile 
    
PS C:\Users\rober\Documents\04 - Workspace\flight-profile> heroku run python manage.py AirlineFleetDatabaseLoad -a flight-profile
 »   Warning: heroku update available from 7.59.2 to 7.59.4.
Running python manage.py AirlineFleetDatabaseLoad on ⬢ flight-profile... up, run.9883 (Free)
AirlineFleetDataBase: file folder= /app/airline/management/commands/AirlineFleet
AirlineFleetDataBase: file path= /app/airline/management/commands/AirlineFleet/AirlineFleet.xls
BadaAircraftDatabase: file folder= /app/trajectory/BadaAircraftPerformance
BadaAircraftDatabase: file path= /app/trajectory/BadaAircraftPerformance/SYNONYM.NEW
airline fleet database exists
BadaAircraftDatabase: opening file=  /app/trajectory/BadaAircraftPerformance/SYNONYM.NEW
BadaAircraftDatabase: number of aircrafts in db= 322
Bada aircraft database read correctly = True
/app/airline/management/commands/AirlineFleet/AirlineFleet.xls
Airbus A220-100
Airbus A220-300
Airbus A319-100
Airbus A319
aircraft ICAO code found = A319 for aircraft full name = Airbus A319
Airbus A320-200
Airbus A320
aircraft ICAO code found = A320 for aircraft full name = Airbus A320
Airbus A321-200
Airbus A321neo
Airbus A330-200
aircraft ICAO code found = A332 for aircraft full name = Airbus A330-200
Airbus A330-300
aircraft ICAO code found = A333 for aircraft full name = Airbus A330-300

Airbus A330-900
Airbus A350-900
Boeing 717-200
aircraft ICAO code found = B712 for aircraft full name = Boeing 717-200
Boeing 737-800
aircraft ICAO code found = B738 for aircraft full name = Boeing 737-800
Boeing 737-900ER
Boeing 757-200
aircraft ICAO code found = B752 for aircraft full name = Boeing 757-200



Boeing 757-300
aircraft ICAO code found = B753 for aircraft full name = Boeing 757-300
Boeing 767-300ER

Boeing 767-400ER

read airline fleet database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>