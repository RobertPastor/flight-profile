'''
Created on 15 août 2023

@author: robert
'''

import time
import csv
import unittest
import os
import math

from trajectory.Environment.Earth import Earth

#============================================
class Test_Main(unittest.TestCase):

    def test_main_one(self):
    
        print ("=========== gravity =========== " + time.strftime("%c"))
        fileName = "gravity.csv"
        fileName = os.path.dirname(__file__) + os.path.sep + fileName
            
        CsvFile = open(fileName, "w")
        dtr = math.pi/180.
        earthRadiusMeters = 6378.135e3
        try:
            writer = csv.writer(CsvFile, delimiter=";")
            print (   type (("latitude in degrees").encode()) )
            #writer.writerow( "latitude in degrees".encode() )
            writer.writerow( ("latitude in degrees", "latitude radians", "radius in meters", "gc" , "gnorth"))
            earth = Earth()
            
            for latitudeDegrees in range(0, 180):
                print ('latitude in degrees: ', latitudeDegrees, " degrees")
                gc , gnorth = earth.gravity(earthRadiusMeters, latitudeDegrees*dtr)
                print (gc , gnorth)
                writer.writerow((latitudeDegrees, latitudeDegrees*dtr, earthRadiusMeters, gc , gnorth))
            
        finally:
            CsvFile.close()
            
    def test_main_two(self):
        
        print ("=========== earth =========== " + time.strftime("%c"))

        earth = Earth()
        earth.dump()
        
        print ("=========== earth =========== " + time.strftime("%c"))
        print (str(earth))
        
if __name__ == '__main__':
    unittest.main()