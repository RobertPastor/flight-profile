'''
Created on 7 mai 2023

@author: robert
'''

from django.core.management.base import BaseCommand
from trajectory.models import AirlineAirport, AirlineRunWay

class Command(BaseCommand):
    help = 'Load the Airports table'

    def handle(self, *args, **options):
        
        airportCode = "KATL"
        airport = AirlineAirport.objects.filter(AirportICAOcode=airportCode).first()
        print ( airport )
        for runWay in AirlineRunWay.objects.filter(Airport=airport):
            print ( runWay )
        print ( "{0} - number of runways = {1}".format( airportCode , AirlineRunWay.objects.filter(Airport=airport).count() ))    
            
        airportCode = "PANC"
        airport = AirlineAirport.objects.filter(AirportICAOcode=airportCode).first()
        print ( airport )
        for runWay in AirlineRunWay.objects.filter(Airport=airport):
            print ( runWay )
        print ( "{0} - number of runways = {1}".format( airportCode , AirlineRunWay.objects.filter(Airport=airport).count() ))    
