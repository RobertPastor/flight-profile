'''
@since: Created on 6 mars 2015

@author: PASTOR Robert

        Written By:
                Robert PASTOR 
                @Email: < robert [--DOT--] pastor0691 (--AT--) gmail [--DOT--] com >

        http://trajectoire-predict.monsite-orange.fr/ 
        Copyright 2015 Robert PASTOR 

        This program is free software; you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation; either version 3 of the License, or
        (at your option) any later version.
 
        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.
 
        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''
from trajectory.BadaAircraftPerformance.BadaAircraftJsonPerformanceFile import AircraftJsonPerformance

Kilogram2Pounds = 2.20462262 # 1 kilogram = 2.204 lbs

import logging

class AircraftMass(object):
    '''
    Four mass values are specified for each aircraft in tons:
    mmin - minimum mass
    mmax - maximum mass
    mref - reference mass
    mpyld - maximum payload mass
    '''
    className = ""
    minimumMassKilograms = 0.0
    maximumMassKilograms = 0.0
    referenceMassKilograms = 0.0
    maximumPayLoadMassKilograms = 0.0
    currentMassKilograms = 0.0
    initialMassKilograms = 0.0
    fuelCapacityKilograms = 0.0
    
    def __init__(self, aircraftPerformance):
        
        assert isinstance(aircraftPerformance, AircraftJsonPerformance)
        self.className = self.__class__.__name__
        self.referenceMassKilograms = aircraftPerformance.getReferenceMassKilograms()
        self.minimumMassKilograms = aircraftPerformance.getMinimumMassKilograms()
        self.maximumMassKilograms = aircraftPerformance.getMaximumMassKilograms()
        self.maximumPayLoadMassKilograms = aircraftPerformance.getMaximumPayLoadMassKilograms()
        ''' aircraft mass is computed adding the pay-load to the minimum and adding the fuel mass '''
        self.currentMassKilograms = self.referenceMassKilograms
        self.initialMassKilograms = self.referenceMassKilograms
        self.fuelCapacityKilograms = aircraftPerformance.getMaximumFuelCapacityKilograms()
        self.dump()
        
    def setAircraftMassKilograms(self, massKilograms):
        assert (self.minimumMassKilograms <= massKilograms) and (massKilograms <= self.maximumMassKilograms)
        logging.info ( self.className + ' ==========================================================' )
        logging.info ( self.className + ': set Aircraft Mass= {0:.2f} kg - Mass= {1:.2f} pounds'.format(massKilograms, massKilograms*Kilogram2Pounds) )
        self.initialMassKilograms = massKilograms
        self.currentMassKilograms = massKilograms
        logging.info ( self.className + ' ==========================================================' )

    def getCurrentMassKilograms(self):
        return self.currentMassKilograms
        
    def getInitialMassKilograms(self):
        return self.initialMassKilograms
        
    def getMinimumMassKilograms(self):
        return self.minimumMassKilograms
    
    def getMaximumMassKilograms(self):
        return self.maximumMassKilograms
    
    def getReferenceMassKilograms(self):
        return self.referenceMassKilograms
    
    def computeInitialFuelMassKilograms(self, flightPathRangeMeters):
        logging.info ( self.className + ': compute Fuel mass in KiloGrams for flight path range= ' + str(flightPathRangeMeters) + ' meters' )
        '''
        SFC Specific Fuel Consumption 
        SFC is defined as the mass flow rate of fuel per unit of thrust (lbm/s/lbf or kg/s/N).
        
        range = Cruise Speed / acceleration of gravity ) * ( 1 / SFC ) * log Nep ( Initial Weight / Final Weight) 
        range = ( speed of sound * Mach ) * ( 1 / ct ) * (CL / CD ) * log nep ( initial Weight / final Weight )
        '''
        #return self.aircraftMass.referenceMassKilograms - self.aircraftMass.minimumMassKilograms  
        return self.fuelCapacityKilograms   
    
    def getMaximumFuelCapacityKilograms(self):
        return self.fuelCapacityKilograms
    
    def computeAircraftMass(self, rangeMeters):
        '''
        mass of the aircraft is obtained using the Breguet range equation
        The maximal total range is the distance an aircraft can fly between take-off and landing.
        '''
        assert isinstance(rangeMeters, float)
        logging.info ( self.className + ': compute aircraft mass - from the range expressed in Meters ' )
        return self.referenceMassKilogramms
    
    def updateAircraftMassKilograms(self, fuelFlowKilograms):
        
        self.currentMassKilograms = self.currentMassKilograms - fuelFlowKilograms
        
        if self.currentMassKilograms > self.maximumMassKilograms:
            raise ValueError (self.className + ': current mass greater to Maximum Mass')
        
        if self.currentMassKilograms < self.minimumMassKilograms:
            raise ValueError (self.className + ': no more fuel !!!')
        
        if self.currentMassKilograms < self.getInitialMassKilograms() - self.getMaximumFuelCapacityKilograms():
            raise ValueError (self.className + ': no more fuel !!!')
        
        return self.currentMassKilograms

    
    def dump(self):
        logging.info ( self.className + ': aircraft reference mass= {0:.2f} kg'.format(self.referenceMassKilograms) )
        logging.info ( self.className + ': aircraft minimum mass= {0:.2f} kg'.format(self.minimumMassKilograms))
        logging.info ( self.className + ': aircraft maximum mass= {0:.2f} kg'.format(self.maximumMassKilograms))
        logging.info ( self.className + ': aircraft maximum pay load mass= {0:.2f} kg'.format(self.maximumPayLoadMassKilograms))
        
        
