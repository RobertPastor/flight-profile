
# apply migrations 
#=================
python manage.py makemigrations airline

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> python manage.py makemigrations airline
Migrations for 'airline':
  airline\migrations\0003_airlineaircraft.py
    - Create model AirlineAircraft
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

# migrate
#=========

python manage.py migrate airline

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> python manage.py migrate airline
Operations to perform:
  Apply all migrations: airline
Running migrations:
  Applying airline.0003_airlineaircraft... OK
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

#open pgAdmin4
==============

password = bobby1xx


