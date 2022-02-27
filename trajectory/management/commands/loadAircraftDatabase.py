
from django.core.management.base import BaseCommand, CommandError
from trajectory.models import Aircrafts

from trajectory.management.commands.BadaAircraftDatabaseFile import BadaAircraftDatabase

class Command(BaseCommand):
    help = 'Reads the Synonym file and load the Aircrafts table'

    def handle(self, *args, **options):
        acBD = BadaAircraftDatabase()
        if (acBD.exists()):
            print("acBD exists")
            ret = acBD.read()
        else:
            print("acBD does not exists")