
from django.core.management.base import BaseCommand
from trajectory.management.commands.BadaAircraftDatabase.BadaAircraftDatabaseFile import BadaAircraftDatabase
from trajectory.models import BadaSynonymAircraft

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        
        BadaSynonymAircraft.objects.all().delete()
        acBD = BadaAircraftDatabase()
        if (acBD.exists()):
            print("acBD exists")
            ret = acBD.read()
            print ("read aircraft database result = {0}".format(ret))
        else:
            print("acBD does not exists")