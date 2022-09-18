
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


# when tables are not created
=============================

python manage.py migrate --fake APPNAME zero
This will make your migration to fake. Now you can run the migrate script

python manage.py migrate APPNAME
Tables will be created and you solved your problem.. Cheers!!!

# re create tables
==================

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> heroku run python manage.py migrate --fake -a flight-profile
 »   Warning: heroku update available from 7.60.2 to 7.63.4.
Running python manage.py migrate --fake on ⬢ flight-profile... up, run.1700 (Free)
Operations to perform:
  Apply all migrations: admin, airline, auth, contenttypes, sessions, trajectory
Running migrations:
  Applying airline.0003_airlineroute_airline... FAKED
  Applying trajectory.0007_kmloutputfile... FAKED
  Applying trajectory.0008_delete_kmloutputfile... FAKED
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>


#if everything fails
====================

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> heroku pg:reset DATABASE_URL -a flight-profile
 »   Warning: heroku update available from 7.60.2 to 7.63.4.
 !    WARNING: Destructive action
 !    postgresql-cubic-90469 will lose all of its data
 !
 !    To proceed, type flight-profile or re-run this command with --confirm flight-profile

> flight-profile
Resetting postgresql-cubic-90469... done
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>

==============================================================

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> heroku run python manage.py makemigrations  -a flight-profile
 »   Warning: heroku update available from 7.60.2 to 7.63.4.
Running python manage.py makemigrations on ⬢ flight-profile... up, run.3765 (Free)
No changes detected

==================================================================

PS C:\Users\rober\Documents\04 - Workspace\flight-profile> heroku run python manage.py migrate  -a flight-profile
 »   Warning: heroku update available from 7.60.2 to 7.63.4.
Running python manage.py migrate on ⬢ flight-profile... up, run.2616 (Free)
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
  Applying sessions.0001_initial... OK
  Applying trajectory.0001_initial... OK
  Applying trajectory.0002_auto_20220227_2053... OK
  Applying trajectory.0003_waypoint_continent... OK
  Applying trajectory.0004_airport... OK
  Applying trajectory.0005_runway... OK
  Applying trajectory.0006_auto_20220422_2214... OK
  Applying trajectory.0007_kmloutputfile... OK
  Applying trajectory.0008_delete_kmloutputfile... OK
PS C:\Users\rober\Documents\04 - Workspace\flight-profile>





