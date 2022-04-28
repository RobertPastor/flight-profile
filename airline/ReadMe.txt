
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

# heroku commands
=================

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> heroku run python manage.py makemigrations -a flight-profile
 »   Warning: heroku update available from 7.59.2 to 7.59.4.
Running python manage.py makemigrations on ⬢ flight-profile... up, run.1277 (Free)
No changes detected
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>


PS C:\Users\rober\Documents\04 - Workspace\flight-profile> heroku run python manage.py migrate -a flight-profile
 »   Warning: heroku update available from 7.59.2 to 7.59.4.
Running python manage.py migrate on ⬢ flight-profile... up, run.6957 (Free)
Operations to perform:
  Apply all migrations: admin, airline, auth, contenttypes, sessions, trajectory
Running migrations:
  No migrations to apply.
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>







