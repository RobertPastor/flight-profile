'''
Created on 3 mai 2023

@author: robert
'''

from django.core.management.base import BaseCommand

from airline.models import AirlineAircraft
from openap import prop

class Command(BaseCommand):
    help = 'Update the airline fleet with turn around times'

    def handle(self, *args, **options):
        
        aircrafts = AirlineAircraft.objects.filter(aircraftICAOcode="A320").order_by("id")
        for ac in aircrafts:
            print ( ac.id )
            AirlineAircraft.objects.filter( id = ac.id ).update( turnAroundTimesMinutes = 25.0 )
            
        aircrafts = AirlineAircraft.objects.filter(aircraftICAOcode="B738").order_by("id")
        for ac in aircrafts:
            print ( ac.id )
            AirlineAircraft.objects.filter( id = ac.id ).update( turnAroundTimesMinutes = 25.0 )
            
        aircrafts = AirlineAircraft.objects.filter(aircraftICAOcode="A332").order_by("id")
        for ac in aircrafts:
            print ( ac.id )
            AirlineAircraft.objects.filter( id = ac.id ).update( turnAroundTimesMinutes = 35.0 )