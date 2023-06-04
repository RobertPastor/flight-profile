'''
Created on 4 juin 2023

@author: robert
'''
from django.core.management.base import BaseCommand

from trajectory.management.commands.SidStar.SidStarDatabaseLoader import SidStarLoaderOne
from trajectory.models import AirlineStandardDepartureArrivalRoute

class Command(BaseCommand):
    help = 'Reads the WayPoints and write in a table'

    def handle(self, *args, **options):
        
        ''' clear database only on purpose '''
        #AirlineStandardDepartureArrivalRoute.objects.all().delete()
        
        loaderOne = SidStarLoaderOne( isSID=True , departureOrArrivalAirportICAO="KLAX" , FirstLastWayPointName="SLI" , RunWayStr="24R" )
        if (loaderOne.exists()):
            print("acBD exists")
            ret = loaderOne.load()
            print ("read SID STAR database result = {0}".format(ret))
        else:
            print("SID STAR does not exists")