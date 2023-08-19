'''
Created on 15 août 2023

@author: robert
'''

import unittest
import os
import xlsxwriter
from trajectory.Environment.Atmosphere import Atmosphere

class Test_Main(unittest.TestCase):

    def test_mains(self):

        fileName = "Tabular Atmosphere.xlsx"
        print ( "===================Tabular Atmosphere start======================" )
        fileName = os.path.dirname(__file__) + os.path.sep  + fileName
        print ( fileName )
        
        workbook = xlsxwriter.Workbook(fileName)
        worksheet = workbook.add_worksheet('Temperature Degrees')
        
        RowIndex = 0
        ColumnIndex = 0
        for header in ['Altitude-Meters', 
                       'Temperature-Degrees',
                       'Temperature-Kelvins',
                       'Air-density-kg-per-cubic-meters',
                       'speed-of-sound',
                       'pressure-hecto-pascals']:
            worksheet.write(RowIndex, ColumnIndex, header)
            ColumnIndex += 1
        
        RowIndex += 1
        # =======================
        atmos = Atmosphere()
        for xAltDecaMeters in range (0,2000):
            
            AltitudeMeters = xAltDecaMeters*10.
            ColumnIndex = 0
            #print  ( '====================================' )
            
            worksheet.write( RowIndex, ColumnIndex, AltitudeMeters )
            ColumnIndex += 1
            
            worksheet.write( RowIndex, ColumnIndex, atmos.getTemperatureDegrees(AltitudeMeters))
            ColumnIndex += 1
    
            worksheet.write( RowIndex, ColumnIndex, atmos.getTemperatureKelvins(AltitudeMeters))
            ColumnIndex += 1
    
            worksheet.write( RowIndex, ColumnIndex, atmos.getAirDensityKilogramsPerCubicMeters(AltitudeMeters))
            ColumnIndex += 1
    
            worksheet.write( RowIndex, ColumnIndex, atmos.getSpeedOfSoundMetersPerSecond(AltitudeMeters))
            ColumnIndex += 1
            
            worksheet.write( RowIndex, ColumnIndex, atmos.getPressurePascals(AltitudeMeters)/100.)
    
            RowIndex += 1
        
        workbook.close()
        print ( "===================Tabular Atmosphere end======================" )
    
if __name__ == '__main__':
    unittest.main()