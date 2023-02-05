from django.urls import  path


from airline.views.viewsAirlineFleet import getAirlineFleet
from airline.views.viewsAirlineRoutes import getAirlineRoutes
from airline.views.viewsAirlineRoutesWayPoints import getRouteWayPoints
from airline.views.viewsAirlineCosts import getAirlineCosts
from airline.views.viewsAirlineCostsOptimization import getCostsOptimization

urlpatterns = [
    
    path('airlineRoutes/<slug:airlineName>' , getAirlineRoutes , name='getAirlineRoutes'),
    path('airlineFleet/<slug:airlineName>' , getAirlineFleet , name='getAirlineFleet'),
    path('wayPointsRoute/<slug:Adep>/<slug:Ades>' , getRouteWayPoints , name='getRouteWayPoints'),
    path('getAirlineCosts/<slug:airlineName>' , getAirlineCosts , name = 'getAirlineCosts'),
    path('getCostsOptimization/<slug:airlineName>' , getCostsOptimization , name = 'getCostsOptimization')
    
]