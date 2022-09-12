from django.urls import re_path, path

from trajectory.views.viewsAirports import getAirports
from trajectory.views.viewsWayPoints import getWayPoints

from trajectory.views.viewsFlightProfile import launchFlightProfile, computeFlightProfile
from trajectory.views.computeCosts import computeCosts

app_name = "trajectory"

urlpatterns = [
    path('airports/<slug:airlineName>' , getAirports , name='getAirports'),
    path('waypoints/<slug:airlineName>' , getWayPoints , name='getWayPoints'),

    re_path(r'^launchFlightProfile$' , launchFlightProfile , name='launchFlightProfile'),
    re_path(r'^computeFlightProfile$' , computeFlightProfile , name='computeFlightProfile'),

    re_path(r'^computeCosts$' , computeCosts , name='computeCosts'),

]