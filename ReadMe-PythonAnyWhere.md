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





