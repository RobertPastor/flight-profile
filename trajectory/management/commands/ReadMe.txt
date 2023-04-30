


 cd "C:\Users\rober\Documents\04 - Workspace\flight-profile"
 
# list all available commands

python manage.py makemigrations -a flight-profile
python manage.py migrate -a flight-profile

python manage.py -a flight-profile --help

# run one command
python manage.py WayPointsDatabaseLoad -a flight-profile 

python manage.py AirportsDatabaseLoad -a flight-profile 
