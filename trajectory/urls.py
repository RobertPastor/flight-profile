from django.urls import re_path, path

from trajectory.views.viewsAirports import getAirports
from trajectory.views.viewsWayPoints import getWayPoints

from trajectory.views.viewsFlightProfile import launchFlightProfile, computeFlightProfile
from trajectory.views.computeCosts import computeCosts

app_name = "trajectory"

urlpatterns = [
    path('airports/<slug:airlineName>' , getAirports , name='getAirports'),
    path('waypoints/<slug:airlineName>' , getWayPoints , name='getWayPoints'),

    path('launchFlightProfile/<slug:airlineName>' , launchFlightProfile , name='launchFlightProfile'),
    path('computeFlightProfile/<slug:airlineName>' , computeFlightProfile , name='computeFlightProfile'),

    path('computeCosts/<slug:airlineName>' , computeCosts , name='computeCosts'),

]