'''
Created on 19 juil. 2022

@author: robert
'''
import time
import unittest

from trajectory.Guidance.TurnLegBaseFile import BaseTurnLeg

#============================================
class Test_Class(unittest.TestCase):

    def test_Class(self):

    
        print ( "=========== Base Turn Leg testing   =========== " + time.strftime("%c") )
        
        baseTurnLeg = BaseTurnLeg(150.0, 190.0, 1.0)
        baseTurnLeg.build()
        print ( baseTurnLeg )
        
        print ( "=========== Base Turn Leg testing   =========== " + time.strftime("%c") )
    
        baseTurnLeg = BaseTurnLeg(350.0, 10.0, 1.0)
        baseTurnLeg.build()
        print ( baseTurnLeg )
        
        print ( "=========== Base Turn Leg testing   =========== " + time.strftime("%c") )
        baseTurnLeg = BaseTurnLeg(10.0, 350.0, -1.0)
        baseTurnLeg.build()
        print ( baseTurnLeg )
        
        print ( "=========== Base Turn Leg testing   =========== " + time.strftime("%c") )
        baseTurnLeg = BaseTurnLeg(270.0, 80.0, -1.0)
        baseTurnLeg.build()
        print ( baseTurnLeg )
        
        print ( "=========== Base Turn Leg testing   =========== " + time.strftime("%c") )
        try:
            BaseTurnLeg(361.0, 0.0, 0.0)
            self.assertFalse(True)
        except:
            self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()