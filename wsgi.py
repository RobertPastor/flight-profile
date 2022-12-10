'''
Created on 10 déc. 2022

@author: robert
'''


import os
import sys

path = os.path.expanduser('~/airlineservices')
if path not in sys.path:
    sys.path.insert(0, path)
    
os.environ['DJANGO_SETTINGS_MODULE'] = 'FlightProfile.settings'
from django.core.wsgi import get_wsgi_application
from django.contrib.staticfiles.handlers import StaticFilesHandler
application = StaticFilesHandler(get_wsgi_application())