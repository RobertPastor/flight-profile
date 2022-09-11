'''
Created on 10 sept. 2022

@author: robert
'''


from airline.management.commands.AirlineRoutesWayPoints.AirlineRoutesReaderFile import AirlineRoutesReader
from airline.management.commands.AirlineRoutesWayPoints.AirlineRoutesWayPointsReader import AirlineRoutesWayPointsDatabase


def test_create_routes():
    
    airlineRoutesWayPointsDatabase = AirlineRoutesWayPointsDatabase()
    airlineRoutesWayPointsDatabase.createRoutesFiles()

def test_one():
    
    print ( '================ test one =================' )
        
    airlineRoutesReader = AirlineRoutesReader()
    airlineRoutesReader.read('KJFK', 'LFPG')
        
        
if __name__ == '__main__':
    test_create_routes()
    test_one()