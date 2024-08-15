'''
Created on 27 juil. 2024

@author: robert

ABI      9900+17 0507+13 0414+08 9900-08 3416-19 363832 363440 352550
ABQ              3415+17 3315+10 3310-05 3318-17 323032 324142 312551
ABR 2016 2129+20 2130+12 2230+06 2235-07 2338-19 223934 213943 233649
AMA      2016    2317+15 1810+08 3208-07 3614-18 353032 354041 354051
AST 9900 9900+12 3209+07 2913+01 3023-13 2932-24 304439 304847 303953


Wind direction is always in reference to true north, and wind speed is given in knots.

The temperature is given in degrees Celsius.

No winds are forecast when a given level is within 1,500 feet of the
station elevation. Similarly, temperatures are not forecast for
any station within 2,500 feet of the station elevation.

'''



def ExploitStationData( stationData , numberOfLevels ):
    pass
    assert( isinstance( stationData , str ))
    assert( isinstance( numberOfLevels , int ))
    stationDataDict = {}

    print( stationData )
    if len ( str ( stationData ) ) > 3:
        stationName = str(stationData)[0:3]
        print ( "Station name = {0}".format(stationName) )
        stationDataDict['name'] = stationName
        
        '''1st level data is always composed of 4 digits '''
        firstLevelData = str(stationData)[4:4]
        stationDataDict["firstLevel"] = firstLevelData
            
        levelsData = []
        stationData = stationData[4:]
        stationArr = str(stationData).split(" ")
        for elem in stationArr:
            if len( str(elem).strip()) > 0:
                levelsData.append( str(elem).strip() )
                
                
        ''' insert empty elements '''
        for n in range ( numberOfLevels - len(levelsData) ):      
            levelsData.insert( n , " " )
            
        stationDataDict['levelsData'] = levelsData
        
    else:
        print ( "Error = cannot find station name")
    return stationDataDict

if __name__ == '__main__':
    stationData = "ABI      9900+17 0507+13 0414+08 9900-08 3416-19 363832 363440 352550"
    numberOfLevels = 9
    stationDataDict = ExploitStationData(  stationData , numberOfLevels )
    print ( stationDataDict )
    
    stationData = "ABQ              3415+17 3315+10 3310-05 3318-17 323032 324142 312551"
    numberOfLevels = 9
    stationDataDict = ExploitStationData(  stationData , numberOfLevels )
    print ( stationDataDict )