from django.urls import path, re_path

from . import views

app_name = "trajectory"

urlpatterns = [
    re_path(r'^airports$' , views.getAirports , name='getAirports'),
    re_path(r'^flightprofile$' , views.getFlightProfile , name='getFlightProfile')

]