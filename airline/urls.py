from django.urls import re_path, path

from . import views

urlpatterns = [
    re_path(r'^airlineRoutes$' , views.getAirlineRoutes , name='getAirlineRoutes'),
    re_path(r'^airlineFleet$' , views.getAirlineFleet , name='getAirlineFleet'),
    
    path('wayPointsRoute/<slug:Adep>/<slug:Ades>' , views.getRouteWayPoints , name='getRouteWayPoints'),
]