import unittest
from trajectory.BadaAircraftPerformance.BadaAircraftDatabaseFile import BadaAircraftDatabase
from trajectory.BadaAircraftPerformance.BadaAircraftPerformanceFile import AircraftPerformance
from trajectory.BadaAircraftPerformance.BadaEngineFile import Engine

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
            assert ( aircraftPerformance.read() , True )
            engine = Engine(aircraftPerformance)
            
            print ('engine is Jet= {0}'.format(engine.isJet()) )
            print ('engine is Turbo Prop= {0}'.format(engine.isTurboProp()) )
            print ( 'engine is Piston= {0}'.format(engine.isPiston()) )
            self.assertTrue(engine.isJet(), 'A320 is a jet aircraft')


    def test_Class_Two(self):
        
        print ( '================ test Two ====================' )

        acBd = BadaAircraftDatabase()
        assert acBd.read()
        
        aircraftICAOcode = 'A320'
        if ( acBd.aircraftExists(aircraftICAOcode) and
             acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
            
            print ( acBd.getAircraftFullName(aircraftICAOcode) )
            
            aircraftPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))
            assert ( aircraftPerformance.read() , True )
            engine = Engine(aircraftPerformance)
            
            print ( 'engine fuel consumption coeff= {0}'.format(engine.getFuelConsumptionCoeff()) )
        
        
    def test_Class_Three(self):

        print ( '================ test Three ====================' )
                
        acBd = BadaAircraftDatabase()
        assert acBd.read()
        
        aircraftICAOcode = 'A320'
        if ( acBd.aircraftExists(aircraftICAOcode) and
             acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
            
            print ( acBd.getAircraftFullName(aircraftICAOcode) )
            
            aircraftPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))
            assert ( aircraftPerformance.read() )
            engine = Engine(aircraftPerformance)
            
            for index in range(0,5):
                print ( index )
                print ( 'engine Max Climb Thrust coeff= {0}'.format(engine.getMaxClimbThrustCoeff(index)) )
            
    def test_Class_Four(self):

        print ( '================ test Four ====================' )

        acBd = BadaAircraftDatabase()
        assert acBd.read()
        
        aircraftICAOcode = 'A320'
        if ( acBd.aircraftExists(aircraftICAOcode) and
             acBd.aircraftPerformanceFileExists(aircraftICAOcode)):
            
            print ( acBd.getAircraftFullName(aircraftICAOcode) )
            
            aircraftPerformance = AircraftPerformance(acBd.getAircraftPerformanceFile(aircraftICAOcode))
            assert ( aircraftPerformance.read() , True )
            engine = Engine(aircraftPerformance)
            
            for index in range(0,5):
                print ( index )
                print ( 'engine Descent Thrust Coeff= {0}'.format(engine.getDescentThrustCoeff(index)) )
        
if __name__ == '__main__':
    unittest.main()
