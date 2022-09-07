'''
Created on 1 sept. 2022

@author: robert
'''

from django.core.management.base import BaseCommand
from airline.models import Airline

class Command(BaseCommand):
    help = 'load the Airline table'

    def handle(self, *args, **options):
        
        Airline.objects.all().delete()

        airlineOne = Airline( 
                        Name = "AmericanWings",
                        MinLongitudeDegrees = -130.0, 
                        MinLatitudeDegrees = 25.0, 
                        MaxLongitudeDegrees = -70.0, 
                        MaxLatitudeDegrees = 50.0)
        airlineOne.save()
        print ( airlineOne )
        
        airlineTwo = Airline (
                        Name = "EuropeanWings",
                        MinLongitudeDegrees = -13.0, 
                        MinLatitudeDegrees = 32.0, 
                        MaxLongitudeDegrees = 32.0, 
                        MaxLatitudeDegrees = 61.0)
        airlineTwo.save()
        print ( airlineTwo )
        
        airlineThree = Airline (
                        Name = "IndianWings",
                        MinLongitudeDegrees = 60.0, 
                        MinLatitudeDegrees = 8.0, 
                        MaxLongitudeDegrees = 92.0, 
                        MaxLatitudeDegrees = 32.0)
            
        airlineThree.save() 
        print ( airlineThree )
        
        return