# run from heroku -> commands used to load the operational database

heroku login 
-> opens a web browser and connect using your smartphone authenticator code specific to heroku


 cd "C:\Users\rober\Documents\04 - Workspace\flight-profile"
 
# list all available commands
heroku run python manage.py makemigrations -a flight-profile
heroku run python manage.py migrate -a flight-profile

heroku run python manage.py -a flight-profile --help

# run one command
heroku run python manage.py WayPointsDatabaseLoad -a flight-profile 

heroku run python manage.py AirportsDatabaseLoad -a flight-profile 
