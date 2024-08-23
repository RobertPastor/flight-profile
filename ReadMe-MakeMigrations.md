# make migrations and migrate


airlineservices) 14:31 ~/flight-profile (master)$ python manage.py makemigrations
No changes detected
(airlineservices) 14:31 ~/flight-profile (master)$ python manage.py migrate

# migrate

(airlineservices) 19:46 ~/flight-profile (master)$ python manage.py makemigrations
linux-6.5.0-1022-aws-x86_64-with-debian-bullseye-sid
No changes detected
(airlineservices) 19:49 ~/flight-profile (master)$ python manage.py migrate
linux-6.5.0-1022-aws-x86_64-with-debian-bullseye-sid
Operations to perform:
  Apply all migrations: admin, airline, auth, contenttypes, sessions, trajectory
Running migrations:
  Applying trajectory.0011_windtemperaturealoft... OK
(airlineservices) 19:49 ~/flight-profile (master)$ 