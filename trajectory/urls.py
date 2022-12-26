from django.urls import  path

from trajectory.views.viewsAirports import getAirports
from trajectory.views.viewsWayPoints import getWayPoints

from trajectory.views.viewsFlightProfile import launchFlightProfile, computeFlightProfile
from trajectory.views.computeCosts import computeCosts
from trajectory.views.downLoadVerticalProfile import createExcelVerticalProfile

app_name = "trajectory"

urlpatterns = [
    path('airports/<slug:airlineName>' , getAirports , name='getAirports'),
    path('waypoints/<slug:airlineName>' , getWayPoints , name='getWayPoints'),

    path('launchFlightProfile/<slug:airlineName>' , launchFlightProfile , name='launchFlightProfile'),
    path('computeFlightProfile/<slug:airlineName>' , computeFlightProfile , name='computeFlightProfile'),

    path('computeCosts/<slug:airlineName>' , computeCosts , name='computeCosts'),

]

''' view to create an EXCEL file '''
urlpatterns += [
    path('excel/<slug:airlineName>', createExcelVerticalProfile , name='createExcel'),
]