

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
    
# after 
$ python manage.py AirlineRoutesWayPointsDatabaseLoad
--> check name of the waypoints for the new route

# run WayPointsXlsxFileCreate
§ python manage.py WayPointsXlsxFileCreate