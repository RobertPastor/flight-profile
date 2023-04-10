from django.urls import  path


from airline.views.viewsAirlineFleet import getAirlineFleet
from airline.views.viewsAirlineRoutes import getAirlineRoutes
from airline.views.viewsAirlineRoutesWayPoints import getRouteWayPoints
from airline.views.viewsAirlineCosts import getAirlineCosts, getAirlineCostsAsXlsx
from airline.views.viewsAirlineCostsOptimization import getAirlineCostsOptimization 
from airline.views.viewsAirlineCASM import getAirlineCASM , getAirlineCasmXlsx
from airline.views.viewsAirlineCasmOptimization import getAirlineCasmOptimization

''' 10th April 2023 - retrieve Airline Costs as xlsx file to download  '''
urlpatterns = [
    
    path('airlineRoutes/<slug:airlineName>' , getAirlineRoutes , name='getAirlineRoutes'),
    path('airlineFleet/<slug:airlineName>' , getAirlineFleet , name='getAirlineFleet'),
    path('wayPointsRoute/<slug:Adep>/<slug:Ades>' , getRouteWayPoints , name='getRouteWayPoints'),
    
    path('getAirlineCosts/<slug:airlineName>' , getAirlineCosts , name = 'getAirlineCosts'),
    path('getAirlineCostsXlsx/<slug:airlineName>' , getAirlineCostsAsXlsx , name = 'getAirlineCostsAsXlsx'),
    
    path('getAirlineCostsOptimization/<slug:airlineName>' , getAirlineCostsOptimization , name = 'getAirlineCostsOptimization'),
    
    path('getAirlineCASM/<slug:airlineName>' , getAirlineCASM , name = 'getAirlineCASM'),
    path('getAirlineCasmXlsx/<slug:airlineName>' , getAirlineCasmXlsx , name = 'getAirlineCasmXlsx'),
    
    path('getAirlineCasmOptimization/<slug:airlineName>' , getAirlineCasmOptimization , name = 'getAirlineCasmOptimization')
    
]