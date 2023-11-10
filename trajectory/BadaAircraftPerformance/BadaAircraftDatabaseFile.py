'''
Created on 23 mai 2015

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
        

this class is responsible for reading the synonym file
The SYNONYM file provided by BADA contains the set of aircraft ICAO code and the prefix to fetch its OPF (Performance file)
this class is aware of the synonym file structure

'''
import os
import logging
from trajectory.models import BadaSynonymAircraft

BADA_381_DATA_FILES = 'Bada381DataFiles'

    
class BadaAircraftDatabase(object):
    ''' this class is responsible for reading the synonym file '''
    
    def __init__(self):
        self.className = self.__class__.__name__
        
        #self.OPFfileExtension = '.OPF'
        self.JsonFileExtension = '.json'

        self.BadaSynonymFilePath = 'SYNONYM.NEW'
        
        self.FilesFolder = os.path.dirname(__file__)
            
        self.BadaSynonymFilePath = (self.FilesFolder + os.path.sep + self.BadaSynonymFilePath)

        self.aircraftFilesFolder = BADA_381_DATA_FILES
        self.aircraftFilesFolder = os.path.join (os.path.dirname(__file__) , self.aircraftFilesFolder )
               
        self.aircraftDict = {}

    def exists(self):
        return os.path.exists(self.BadaSynonymFilePath) and os.path.isfile(self.BadaSynonymFilePath)
        
    def getSynonymFilePath(self):
        return self.BadaSynonymFilePath
    
    def read(self):
        try:
            f = open(self.BadaSynonymFilePath, "r")
            for line in f:
                line = line.strip()
                useSynonym = False
                if str(line).startswith('CD'):
                    #logging.info self.className + ' line= {0}'.format(line)
                    itemIndex = 0
                    aircraftFullName = ''
                    aircraftICAOcode = ''
                    for item in str(line).split():
                        ''' second item 0..1..2 is the aircraft ICAO code '''
                        if itemIndex == 1:
                            if str(item).strip() == '-':
                                #logging.info self.className +' : has main OPF file'
                                useSynonym = False
                            elif str(item).strip() == '*':
                                #logging.info self.className +' : use synonym OPF file'
                                useSynonym = True

                        if itemIndex == 2:
                            ''' second item is the ICAO code '''
                            aircraftICAOcode = str(item).strip()
                            
                        if (item.endswith('_')):
                            break
                        
                        elif itemIndex > 3:
                            aircraftFullName += ' ' + item
                            
                        elif itemIndex > 2:
                            aircraftFullName += item
                        
                        itemIndex += 1
                    ''' 2-November-2023- move to json performance files  '''
                    filePrefix = str(str(line).split()[-3]).replace("_","")
                    ''' situation after the item finishing with two underscores __ '''
                    if aircraftICAOcode in self.aircraftDict:
                        logging.info ( self.className + ' aircraft ICAO code already in Database' )
                    else:
                        
                        badaSynonymAircraft = BadaSynonymAircraft(      AircraftICAOcode = aircraftICAOcode,
                                                                        AircraftModel = aircraftFullName,
                                                                        AircraftFile = filePrefix,
                                                                        useSynonym = useSynonym)
                        
                        self.aircraftDict[aircraftICAOcode] = badaSynonymAircraft
                        
            f.close()
            logging.info ( self.className + ' number of aircrafts in db= {0}'.format(len(self.aircraftDict)) )
            return True
        except Exception as e:
            raise ValueError(self.className + ' error= {0} while reading= {1} '.format(e, self.BadaSynonymFilePath))
        return False    

    def aircraftExists(self, aircraftICAOcode):
        aircraftICAOcode = str(aircraftICAOcode).upper()
        logging.info ( self.className + ' aircraft= {0} exists= {1}'.format(aircraftICAOcode, aircraftICAOcode in self.aircraftDict ) )
        return aircraftICAOcode in self.aircraftDict

    def getAircraftFullName(self, aircraftICAOcode):
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            ac = self.aircraftDict[aircraftICAOcode]
            return ac.getAircraftFullName()
        else:
            return ''

    def getAircraftPerformanceFile(self, aircraftICAOcode):
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            
            ac = self.aircraftDict[aircraftICAOcode]
            filePrefix = ac.getAircraftOPFfilePrefix().replace("_","")
            
            filePath = os.path.join ( os.path.dirname(__file__) , ".." , BADA_381_DATA_FILES , filePrefix + self.JsonFileExtension )
            return filePath
        
        return ''
    
    def getAircraftJsonPerformanceFile(self, aircraftICAOcode):
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            
            ac = self.aircraftDict[aircraftICAOcode]
            filePrefix = ac.getAircraftOPFfilePrefix().replace("_","")
            
            filePath = os.path.join ( os.path.dirname(__file__) , ".." , BADA_381_DATA_FILES , filePrefix + self.JsonFileExtension )
            return filePath
        
        return ''
        
    def getAircraftICAOcode(self, aircraftFullName):
        acICAOcode = None
        for key, value in self.aircraftDict.items():
            if ( self.getAircraftFullName(key) == str(aircraftFullName).upper() ):
                acICAOcode = key
        return acICAOcode
            
        
    def aircraftPerformanceFileExists(self, aircraftICAOcode):
        ''' checks that the performance file OPF exists in its specific folder '''
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            logging.info ( self.className + ' aircraft= {0} - found in database'.format(aircraftICAOcode) )
            ac = self.aircraftDict[aircraftICAOcode]
            ''' 2-November-2023 - move to json performance files '''
            filePrefix = ac.getAircraftOPFfilePrefix().replace("_","")
            filePath = os.path.join ( os.path.dirname(__file__) , ".." , BADA_381_DATA_FILES , filePrefix + self.JsonFileExtension )
            return os.path.exists(filePath) and os.path.isfile(filePath)
        
        return False
    
    def aircraftPerformanceJsonFileExists(self, aircraftICAOcode):
        ''' checks that the performance file OPF exists in its specific folder '''
        aircraftICAOcode = str(aircraftICAOcode).upper()
        if aircraftICAOcode in self.aircraftDict:
            logging.info ( self.className + ' aircraft= {0} - found in database'.format(aircraftICAOcode) )
            ac = self.aircraftDict[aircraftICAOcode]
            ''' 2-November-2023 - move to json performance files '''
            filePrefix = ac.getAircraftOPFfilePrefix().replace("_","")
            filePath = os.path.join ( os.path.dirname(__file__) , ".." , BADA_381_DATA_FILES , filePrefix + self.JsonFileExtension )
            return os.path.exists(filePath) and os.path.isfile(filePath)
        
        return False

    def dump(self):
        for key, value in self.aircraftDict.items():
            logging.info ( key )
            logging.info ( value )
            logging.info ( self.getAircraftFullName(key) )

    def getAircraftICAOcodes(self):
        for key, value in self.aircraftDict.items():
            yield key