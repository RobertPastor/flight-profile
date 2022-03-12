# run from heroku -> commands used to load the operational database
#==================================================================

heroku login 
-> opens a web browser and connect using your smartphone authenticator code specific to heroku

# list the available commands
#============================

heroku run python manage.py help

# run one command
#================

heroku run python manage.py AirlineRoutesDatabaseLoad -a flight-profile 

heroku run python manage.py makemigrations -a flight-profile
heroku run python manage.py migrate -a flight-profile


# run command in local environment
#=================================

Type 'manage.py help <subcommand>' for help on a specific subcommand.

Available subcommands:

[airline]
    AirlineFleetDatabaseLoad
    AirlineRoutesDatabaseLoad
    
C:\Users\rober\Documents\04 - Workspace\flight-profile\airline\management\commands\AirlineFleet\AirlineFleet.xls
Airbus A220-100
Airbus A220-300
Airbus A319-100
Airbus A319
Airbus A320-200
Airbus A320
Airbus A321-200
Airbus A321neo
Airbus A330-200
Airbus A330-300

Airbus A330-900
Airbus A350-900
Boeing 717-200
Boeing 737-800
Boeing 737-900ER
Boeing 757-200



Boeing 757-300
Boeing 767-300ER

Boeing 767-400ER

read airline fleet database result = True
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>