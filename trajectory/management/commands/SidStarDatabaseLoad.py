'''
Created on 4 juin 2023

@author: robert
'''
from django.core.management.base import BaseCommand

from trajectory.management.commands.SidStar.SidStarDatabaseLoader import SidStarLoaderOne

class Command(BaseCommand):
    help = 'Reads the SID STAR waypoints and write in a table'

    def handle(self, *args, **options):
        
        ''' clear database only on purpose '''
        #AirlineStandardDepartureArrivalRoute.objects.all().delete()
        
        loaderOne = SidStarLoaderOne( isSID=True , departureOrArrivalAirportICAO="KLAX" , FirstLastWayPointName="SLI" , RunWayStr="24R" )
        if (loaderOne.exists()):
            ret = loaderOne.load()
            print ("read SID STAR database result = {0}".format(ret))
        else:
            print("SID STAR does not exists")
            
        loadTwo = SidStarLoaderOne( isSID=False , departureOrArrivalAirportICAO="KATL" , FirstLastWayPointName="MEM" , RunWayStr="26L" )
        if (loadTwo.exists()):
            ret = loadTwo.load()
            print ("read SID STAR database result = {0}".format(ret))
        else:
            print("SID STAR does not exists")
            
        
        loadThree = SidStarLoaderOne( isSID=True , departureOrArrivalAirportICAO="LFPG" , FirstLastWayPointName="ERIXU" , RunWayStr="26L" )
        if (loadThree.exists()):
            ret = loadThree.load()
            print ("read SID STAR database result = {0}".format(ret))
        else:
            print("SID STAR does not exists")
            
        ''' 6th August 2023 - STAR - JFK -> LUKIP - LFPG/08L '''
        loadFour = SidStarLoaderOne( isSID=False , departureOrArrivalAirportICAO="LFPG" , FirstLastWayPointName="LUKIP" , RunWayStr="08L" )
        if (loadFour.exists()):
            print("acBD exists")
            ret = loadFour.load()
            print ("read SID STAR database result = {0}".format(ret))
        else:
            print("SID STAR does not exists")
            