'''
Created on 10 déc. 2022

@author: robert
'''

"""
WSGI config for gettingstarted project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "FlightProfile.settings")

from django.core.wsgi import get_wsgi_application
#from whitenoise import WhiteNoise

application = get_wsgi_application()

#PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
#application = WhiteNoise(application)