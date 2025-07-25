from django.urls import  path


from trajectory.views.viewsAirports import getAirports
from trajectory.views.viewsWayPoints import getWayPoints
from trajectory.views.viewsAircraft import getAircraft

from trajectory.views.viewsFlightProfile import launchFlightProfile, computeFlightProfile
from trajectory.views.computeCosts import computeCosts
from trajectory.views.downLoadVerticalProfile import createExcelVerticalProfile
from trajectory.views.viewsFuelPlanner import launchFuelPlanner
from trajectory.views.computeRunwayOvershoot import computeRunwayOvershoot
from trajectory.views.viewsSidStar import showSidStar
from trajectory.views.downloadKMLfile import createKMLfile
from trajectory.views.viewsMetar import getMetar
from trajectory.views.viewsWindTemperature import getWindTemperatureExcel

app_name = "trajectory"

''' 25th September 2023 - add Metar '''
urlpatterns = [
    
    path('airports/<slug:airlineName>' , getAirports , name='getAirports'),
    path('waypoints/<slug:airlineName>' , getWayPoints , name='getWayPoints'),
    path('launchFlightProfile/<slug:airlineName>/<slug:BadaWrap>' , launchFlightProfile , name='launchFlightProfile'),
    path('computeFlightProfile/<slug:airlineName>/<slug:BadaWrap>' , computeFlightProfile , name='computeFlightProfile'),
    path('computeCosts/<slug:airlineName>/<slug:BadaWrap>' , computeCosts , name='computeCosts'),
    path('aircraft' , getAircraft , name="getAircraft"),
    path('fuelPlanner/<slug:airlineName>' , launchFuelPlanner , name='launchFuelPlanner'),
    path('computeRunwayOvershoot/<slug:aircraftICAOcode>/<slug:airport>/<slug:runway>/<slug:mass>' , computeRunwayOvershoot , name ='computeRunwayOvershoot'),
    path('sidStar/<slug:SidOrStar>/<slug:airport>/<slug:runway>/<slug:waypoint>' , showSidStar , name="showSidStar"),
    path('metar/<slug:airlineName>' , getMetar , name='getMetar'),
    path('windTemperature/<slug:airlineName>' , getWindTemperatureExcel , name='getWindTemperatureExcel')

]

''' view to create an EXCEL file with the state vector (vertical profile) or a KML Google Earth file '''
urlpatterns += [
    
    path('excel/<slug:airlineName>/<slug:BadaWrap>', createExcelVerticalProfile , name='createExcel'),
    path('kml/<slug:airlineName>/<slug:BadaWrap>', createKMLfile , name='createKMLfile'),
    
]