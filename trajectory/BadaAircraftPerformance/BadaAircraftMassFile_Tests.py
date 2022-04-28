import unittest
from trajectory.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile  import AircraftPerformance
from trajectory.BadaAircraftPerformance.BadaAircraftMassFile import AircraftMass

class Test_Class(unittest.TestCase):

    def test_Class_One(self):
            
        print ( '================ test one ====================' )
        acBd = BadaAircraftDatabase()
        assert acBd.read()
        
        aircraftICAOcode = 'A320'
        if ( acBd.aircraftExists(aircraftICAOcode) and
             acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
            
            print ( acBd.getAircraftFullName(aircraftICAOcode) )
            
            aircraftPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))
            aircraftMass = AircraftMass(aircraftPerformance)
            
if __name__ == '__main__':
    unittest.main() 
    