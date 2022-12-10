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

