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

app_name = "trajectory"

urlpatterns = [
    
    path('airports/<slug:airlineName>' , getAirports , name='getAirports'),
    path('waypoints/<slug:airlineName>' , getWayPoints , name='getWayPoints'),

    path('launchFlightProfile/<slug:airlineName>' , launchFlightProfile , name='launchFlightProfile'),
    path('computeFlightProfile/<slug:airlineName>' , computeFlightProfile , name='computeFlightProfile'),

    path('computeCosts/<slug:airlineName>' , computeCosts , name='computeCosts'),
    path('getAircraft/<slug:airlineName>' , getAircraft , name="getAircraft"),
    
    path('launchFuelPlanner/<slug:airlineName>' , launchFuelPlanner , name='launchFuelPlanner'),
    
    path('computeRunwayOvershoot/<slug:aircraft>/<slug:airport>/<slug:runway>/<slug:mass>' , computeRunwayOvershoot , name ='computeRunwayOvershoot'),
    
    path('showSidStar/<slug:SidOrStar>/<slug:airport>/<slug:runway>/<slug:waypoint>' , showSidStar , name="showSidStar")

]

''' view to create an EXCEL file '''
urlpatterns += [
    path('excel/<slug:airlineName>', createExcelVerticalProfile , name='createExcel'),
    
]