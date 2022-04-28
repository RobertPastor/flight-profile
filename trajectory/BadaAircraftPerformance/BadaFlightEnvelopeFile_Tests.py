import unittest
from trajectory.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.BadaAircraftPerformance.BadaFlightEnvelopeFile import FlightEnvelope

from trajectory.Environment.Atmosphere import Atmosphere
from trajectory.Environment.Earth import Earth

class Test_Class(unittest.TestCase):

    def test_Class_One(self):
        
        print ( '================ test one ====================' )
        acBd = BadaAircraftDatabase()
        assert acBd.read()
        
        atmosphere = Atmosphere()
        earth = Earth()
        
        aircraftICAOcode = 'A320'
        if ( acBd.aircraftExists(aircraftICAOcode) and
             acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
            
            print ( acBd.getAircraftFullName(aircraftICAOcode) )
            
            aircraftPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))
            flightEnvelope = FlightEnvelope(aircraftPerformance = aircraftPerformance,
                                            ICAOcode = aircraftICAOcode,
                                            atmosphere = atmosphere,
                                            earth = earth)
            print ( flightEnvelope )
        
        
        
if __name__ == '__main__':
    unittest.main() 
    
