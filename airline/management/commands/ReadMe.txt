# run from heroku -> commands used to load the operational database

heroku login 
-> opens a web browser and connect using your smartphone authenticator code specific to heroku

# list the available commands

heroku run python manage.py -help

# run one command
heroku run python manage.py AirlineRoutesDatabaseLoad -a flight-profile 

heroku run python manage.py makemigrations -a flight-profile
heroku run python manage.py migrate -a flight-profile