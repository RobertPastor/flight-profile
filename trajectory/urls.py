from django.urls import re_path

from . import views

app_name = "trajectory"

urlpatterns = [
    re_path(r'^airports$' , views.getAirports , name='getAirports'),
    re_path(r'^waypoints$' , views.getWayPoints , name='getWayPoints'),
    re_path(r'^showFlightProfile$' , views.showFlightProfile , name='showFlightProfile'),
    re_path(r'^launchFlightProfile$' , views.launchFlightProfile , name='launchFlightProfile'),
    re_path(r'^computeFlightProfile$' , views.computeFlightProfile , name='computeFlightProfile')

]