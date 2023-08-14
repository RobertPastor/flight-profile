from django.urls import  path


from airline.views.viewsAirlineFleet import getAirlineFleet
from airline.views.viewsAirlineRoutes import getAirlineRoutes
from airline.views.viewsAirlineRoutesWayPoints import getRouteWayPoints
from airline.views.viewsAirlineCosts import getAirlineCosts, getAirlineCostsAsXlsx
from airline.views.viewsAirlineCostsOptimization import getAirlineCostsOptimization 
from airline.views.viewsAirlineCASM import getAirlineCASM , getAirlineCasmXlsx
from airline.views.viewsAirlineCasmOptimization import getAirlineCasmOptimization
from airline.views.viewsAirlineSeatMilesMaximization import getAirlineSeatsMilesMaxXlsx

from airline.views.viewsUsers import viewUsers

app_name = "airline"

''' 10th April 2023 - retrieve Airline Costs as xlsx file to download  '''
urlpatterns = [
    
    path('airlineRoutes/<slug:airlineName>' , getAirlineRoutes , name='getAirlineRoutes'),
    path('airlineFleet/<slug:airlineName>' , getAirlineFleet , name='getAirlineFleet'),
    path('wayPointsRoute/<slug:Adep>/<slug:Ades>' , getRouteWayPoints , name='getRouteWayPoints'),
    path('airlineCosts/<slug:airlineName>' , getAirlineCosts , name = 'getAirlineCosts'),
    path('airlineCostsOptimization/<slug:airlineName>' , getAirlineCostsOptimization , name = 'getAirlineCostsOptimization'),
    path('getAirlineCostsXlsx/<slug:airlineName>' , getAirlineCostsAsXlsx , name = 'getAirlineCostsAsXlsx'),
    path('getAirlineCASM/<slug:airlineName>' , getAirlineCASM , name = 'getAirlineCASM'),
    path('getAirlineCasmXlsx/<slug:airlineName>' , getAirlineCasmXlsx , name = 'getAirlineCasmXlsx'),
    path('getAirlineCasmOptimization/<slug:airlineName>' , getAirlineCasmOptimization , name = 'getAirlineCasmOptimization'),
    path('getAirlineSeatMilesXlsx/<slug:airlineName>' , getAirlineSeatsMilesMaxXlsx , name = 'getAirlineSeatsMilesMaxXlsx'),
    path('users' , viewUsers , name = 'viewUsers')
    
]