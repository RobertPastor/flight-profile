# URL is airlines.eu.pythonanywhere.com

## Code differences in Settings.py

dj-database-url==0.5.0 not used with pythonanywhere
in Settings.py comment the next line
import dj_database_url

# Update database configuration with $DATABASE_URL.
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

# code not needed anymore inSettings.py 

comment the next lines in Settings.py
import django_heroku
django_heroku.settings(locals())


## in requirements.txt
suppress
django-heroku==0.3.1
suppress
psycopg2==2.8.3


# create the new account in eu.pythonanywhere.com
https://eu.pythonanywhere.com/user/airlineservices/
account = airlineservices
password = same as usual

# confirm the email 

# launch a bash console
13:40 ~ $ pwd
/home/airlineservices
13:41 ~ $ 


## Clone the github repository

13:41 ~ $ git clone https://github.com/RobertPastor/flight-profile.git
Cloning into 'flight-profile'...
remote: Enumerating objects: 2546, done.
remote: Counting objects: 100% (252/252), done.
remote: Compressing objects: 100% (164/164), done.
remote: Total 2546 (delta 133), reused 166 (delta 79), pack-reused 2294
Receiving objects: 100% (2546/2546), 20.73 MiB | 23.61 MiB/s, done.
Resolving deltas: 100% (1145/1145), done.
Updating files: 100% (751/751), done.
13:42 ~ $ 

## check the python version in the local home environment

PS C:\Users\rober> python --version
Python 3.7.7
PS C:\Users\rober>

## Create a virtual environment with the appropriate Python version

14:11 ~ $ mkvirtualenv airlineservices --python=/usr/bin/python3.7

13:44 ~ $ mkvirtualenv airlineservices --python=/usr/bin/python3.7
created virtual environment CPython3.7.13.final.0-64 in 9519ms
  creator CPython3Posix(dest=/home/airlineservices/.virtualenvs/airlineservices, clear=False, no_vcs_ignore=False, global=False)
  seeder FromAppData(download=False, pip=bundle, setuptools=bundle, wheel=bundle, via=copy, app_data_dir=/home/airlineservices/.local/share/virtualenv)
    added seed packages: pip==22.1.2, setuptools==62.6.0, wheel==0.37.1
  activators BashActivator,CShellActivator,FishActivator,NushellActivator,PowerShellActivator,PythonActivator
virtualenvwrapper.user_scripts creating /home/airlineservices/.virtualenvs/airlineservices/bin/predeactivate
virtualenvwrapper.user_scripts creating /home/airlineservices/.virtualenvs/airlineservices/bin/postdeactivate
virtualenvwrapper.user_scripts creating /home/airlineservices/.virtualenvs/airlineservices/bin/preactivate
virtualenvwrapper.user_scripts creating /home/airlineservices/.virtualenvs/airlineservices/bin/postactivate
virtualenvwrapper.user_scripts creating /home/airlineservices/.virtualenvs/airlineservices/bin/get_env_details
(airlineservices) 13:44 ~ $ 

## Check python in the python anywhere virtual environment

(airlineservices) 13:45 ~ $ python --version
Python 3.7.13
(airlineservices) 13:45 ~ $ 

## check django version in the local home environment

PS C:\Users\rober> python -m django --version
2.2.11
PS C:\Users\rober>

## Install Django 2.2 in the python anywhere virtual environment

(airlineservices) 13:45 ~ $ pip install django==2.2
Looking in links: /usr/share/pip-wheels
Collecting django==2.2
  Downloading Django-2.2-py3-none-any.whl (7.4 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.4/7.4 MB 39.6 MB/s eta 0:00:00
Collecting sqlparse
  Downloading sqlparse-0.4.3-py3-none-any.whl (42 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 42.8/42.8 kB 750.1 kB/s eta 0:00:00
Collecting pytz
  Downloading pytz-2022.6-py2.py3-none-any.whl (498 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 498.1/498.1 kB 12.0 MB/s eta 0:00:00
Installing collected packages: pytz, sqlparse, django
Successfully installed django-2.2 pytz-2022.6 sqlparse-0.4.3
(airlineservices) 13:48 ~ $ 

## Install xlsxwriter in the virtual environment

(airlineservices) 13:49 ~ $ pip install xlsxwriter
Looking in links: /usr/share/pip-wheels
Collecting xlsxwriter
  Downloading XlsxWriter-3.0.3-py3-none-any.whl (149 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 150.0/150.0 kB 3.8 MB/s eta 0:00:00
Installing collected packages: xlsxwriter
Successfully installed xlsxwriter-3.0.3
(airlineservices) 13:49 ~ $ 

## Install openpyxl in the virtual environment

(airlineservices) 13:52 ~ $ pip install openpyxl
Looking in links: /usr/share/pip-wheels
Collecting openpyxl
  Downloading openpyxl-3.0.10-py2.py3-none-any.whl (242 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 242.1/242.1 kB 5.2 MB/s eta 0:00:00
Collecting et-xmlfile
  Downloading et_xmlfile-1.1.0-py3-none-any.whl (4.7 kB)
Installing collected packages: et-xmlfile, openpyxl
Successfully installed et-xmlfile-1.1.0 openpyxl-3.0.10
(airlineservices) 13:54 ~ $ 

## Install pandas in the virtual environment
## this installation installs also numpy

(airlineservices) 13:51 ~ $ pip install pandas
Looking in links: /usr/share/pip-wheels
Collecting pandas
  Downloading pandas-1.3.5-cp37-cp37m-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (11.3 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 11.3/11.3 MB 35.6 MB/s eta 0:00:00
Collecting numpy>=1.17.3
  Downloading numpy-1.21.6-cp37-cp37m-manylinux_2_12_x86_64.manylinux2010_x86_64.whl (15.7 MB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 15.7/15.7 MB 34.2 MB/s eta 0:00:00
Requirement already satisfied: pytz>=2017.3 in ./.virtualenvs/airlineservices/lib/python3.7/site-packages (from pandas) (2022.6)
Collecting python-dateutil>=2.7.3
  Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 247.7/247.7 kB 7.8 MB/s eta 0:00:00
Collecting six>=1.5
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: six, numpy, python-dateutil, pandas
Successfully installed numpy-1.21.6 pandas-1.3.5 python-dateutil-2.8.2 six-1.16.0
(airlineservices) 13:52 ~ $ 

## Install whitenoise in the virtual environment

(airlineservices) 13:56 ~ $ pip install whitenoise
Looking in links: /usr/share/pip-wheels
Collecting whitenoise
  Downloading whitenoise-6.2.0-py3-none-any.whl (19 kB)
Installing collected packages: whitenoise
Successfully installed whitenoise-6.2.0
(airlineservices) 13:57 ~ $ 

## Install xmltodict - used when a xml flight profile is send to the browser / client

(airlineservices) 14:00 ~ $ pip install xmltodict
Looking in links: /usr/share/pip-wheels
Collecting xmltodict
  Downloading xmltodict-0.13.0-py2.py3-none-any.whl (10.0 kB)
Installing collected packages: xmltodict
Successfully installed xmltodict-0.13.0
(airlineservices) 14:00 ~ $ 


## Install mysqlclient

(airlineservices) 13:54 ~ $ pip install mysqlclient
Looking in links: /usr/share/pip-wheels
Collecting mysqlclient
  Downloading mysqlclient-2.1.1.tar.gz (88 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 88.1/88.1 kB 2.9 MB/s eta 0:00:00
  Preparing metadata (setup.py) ... done
Building wheels for collected packages: mysqlclient
  Building wheel for mysqlclient (setup.py) ... done
  Created wheel for mysqlclient: filename=mysqlclient-2.1.1-cp37-cp37m-linux_x86_64.whl size=109879 sha256=1f80d1a277e9ea22e3332fd287626e0a5846e7a0c845695e54367cd8ed0c4770
  Stored in directory: /home/airlineservices/.cache/pip/wheels/95/2d/67/2cb3f82e435fc8e055cb2761a15a0812bf086068f6fb835462
Successfully built mysqlclient
Installing collected packages: mysqlclient
Successfully installed mysqlclient-2.1.1
(airlineservices) 13:55 ~ $ 

## locate the virtual environment (to be used later)

(airlineservices) 14:02 ~ $ ls -al .virtualenvs/airlineservices
total 24
drwxrwxr-x 4 airlineservices registered_users 4096 Dec 10 13:44 .
drwxrwxr-x 3 airlineservices registered_users 4096 Dec 10 13:44 ..
-rw-rw-r-- 1 airlineservices registered_users   40 Dec 10 13:44 .gitignore
drwxrwxr-x 3 airlineservices registered_users 4096 Dec 10 13:51 bin
drwxrwxr-x 3 airlineservices registered_users 4096 Dec 10 13:44 lib
-rw-rw-r-- 1 airlineservices registered_users  223 Dec 10 13:44 pyvenv.cfg
(airlineservices) 14:02 ~ $ 

## path to your virtual environment
/home/airlineservices/.virtualenvs/airlineservices

## create new web app - enter manual configuration - select Django and the Python version 3.7

https://eu.pythonanywhere.com/user/airlineservices/webapps/#tab_id_airlineservices_eu_pythonanywhere_com

## enter the path to your virtual environment in the web tab

Virtualenv:
enter the path to your virtual environment
/home/airlineservices/.virtualenvs/airlineservices/

## configure MySQL database
https://eu.pythonanywhere.com/user/airlineservices/databases/ 

Enter a password for the MySQL database

Database host address:airlineservices.mysql.eu.pythonanywhere-services.com
Username:airlineservices

create a database
Database name: airlineservices

MySQL password:

# check git remote in the bash console
need to move in the folder containing the .git

airlineservices) 14:22 ~ $ cd flight-profile/
(airlineservices) 14:22 ~/flight-profile (master)$ git remote -v
origin  https://github.com/RobertPastor/flight-profile.git (fetch)
origin  https://github.com/RobertPastor/flight-profile.git (push)
(airlineservices) 14:22 ~/flight-profile (master)$ 

## update MySQL database settings (after performing changes in GitHub) - run git pull

(airlineservices) 14:23 ~/flight-profile (master)$ git pull
remote: Enumerating objects: 9, done.
remote: Counting objects: 100% (9/9), done.
remote: Compressing objects: 100% (2/2), done.
remote: Total 5 (delta 3), reused 5 (delta 3), pack-reused 0
Unpacking objects: 100% (5/5), 2.92 KiB | 42.00 KiB/s, done.
From https://github.com/RobertPastor/flight-profile
   20ea4e9..4409c8b  master     -> origin/master
Updating 20ea4e9..4409c8b
Fast-forward
 FlightProfile/settings.py |   6 ++---
 ReadMe-PythonAnyWhere.md  | 198 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 2 files changed, 201 insertions(+), 3 deletions(-)
(airlineservices) 14:23 ~/flight-profile (master)$ 


# make migrations and migrate

airlineservices) 14:25 ~/flight-profile (master)$ python manage.py makemigrations
SystemCheckError: System check identified some issues:
ERRORS:
airline.Airline.Name: (mysql.E001) MySQL does not allow unique CharFields to have a max_length > 255.
(airlineservices) 14:25 ~/flight-profile (master)$ 

## change the models and reduce the name of airline.Airline.Name to 250

airlineservices) 14:31 ~/flight-profile (master)$ python manage.py makemigrations
No changes detected
(airlineservices) 14:31 ~/flight-profile (master)$ python manage.py migrate
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
  Applying airline.0004_auto_20221210_1528... OK
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
(airlineservices) 14:32 ~/flight-profile (master)$ 

## create super user

airlineservices) 14:33 ~/flight-profile (master)$ python manage.py createsuperuser                                                                                                      
Username (leave blank to use 'airlineservices'): 
Email address: robert.pastor0691@gmail.com
Password: 
Password (again): 
Superuser created successfully.
(airlineservices) 14:34 ~/flight-profile (master)$ 

## go to the pythonanywhere web tab and reload the site .... It should be working now

edit the wsgi.py file located here

/var/www/airlineservices_eu_pythonanywhere_com_wsgi.py

'# +++++++++++ DJANGO +++++++++++
'# To use your own Django app use code like this:
import os
import sys

'# assuming your Django settings file is at '/home/myusername/mysite/mysite/settings.py'
path = '/home/myusername/mysite'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'FlightProfile.settings'

'## Uncomment the lines below depending on your Django version
'###### then, for Django >=1.5:
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

## allowed hosts
DisallowedHost at /
Invalid HTTP_HOST header: 'airlineservices.eu.pythonanywhere.com'. You may need to add 'airlineservices.eu.pythonanywhere.com' to ALLOWED_HOSTS.

in settings.py add the allowed host
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'airlineservices.eu.pythonanywhere.com']


#ImproperlyConfigured at /
You're using the staticfiles app without having set the STATIC_ROOT setting to a filesystem path.

'# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))

# configure the airline database

(airlineservices) 19:27 ~/flight-profile (master)$ python manage.py AirlineDatabaseLoad
AmericanWings
EuropeanWings
IndianWings
(airlineservices) 19:27 ~/flight-profile (master)$

# configure the airline fleet database

airlineservices) 19:27 ~/flight-profile (master)$ python manage.py AirlineFleetDatabaseLoad
airline fleet database exists
Bada aircraft database read correctly = True
/home/airlineservices/flight-profile/airline/management/commands/AirlineFleet/AirlineFleet.xls
--> row --> 0
--> row --> 1
1
Airbus A320-200
--> row --> 2
2
Airbus A320
AmericanWings
Airbus A320
--> row --> 3
--> row --> 3
3
Airbus A330-200
AmericanWings
Airbus A330-200
--> row --> 4
4
Boeing 737-800
AmericanWings
Boeing 737-800
--> row --> 5
5
Boeing 737-900ER
--> row --> 6
6
Airbus A320-200
--> row --> 7
7
Airbus A320
EuropeanWings
Airbus A320
--> row --> 8
8
Airbus A330-200
EuropeanWings
Airbus A330-200
--> row --> 9
9
Boeing 737-800
EuropeanWings
Boeing 737-800
--> row --> 10
10
Boeing 737-900ER
--> row --> 11
11
Airbus A320-200
--> row --> 12
12
Airbus A320
IndianWings
Airbus A320
--> row --> 13
13
Airbus A330-200
IndianWings
Airbus A330-200
--> row --> 14
14
Boeing 737-800
IndianWings
Boeing 737-800
--> row --> 15
15
Boeing 737-900ER
read airline fleet database result = True
(airlineservices) 19:29 ~/flight-profile (master)$


