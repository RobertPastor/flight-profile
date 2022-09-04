from django.urls import re_path, path


from airline.views.viewsAirlineFleet import getAirlineFleet
from airline.views.viewsAirlineRoutes import getAirlineRoutes
from airline.views.viewsAirlineRoutesWayPoints import getRouteWayPoints

urlpatterns = [
    re_path(r'^airlineRoutes$' , getAirlineRoutes , name='getAirlineRoutes'),
    
    path('airlineFleet/<slug:airlineName>' , getAirlineFleet , name='getAirlineFleet'),
    
    path('wayPointsRoute/<slug:Adep>/<slug:Ades>' , getRouteWayPoints , name='getRouteWayPoints'),
]