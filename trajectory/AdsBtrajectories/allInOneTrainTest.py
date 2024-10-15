'''
Created on 15 oct. 2024

@author: rober
'''

from trajectory.AdsBtrajectories.utils import readChallengeSet
from trajectory.AdsBtrajectories.utils import readSubmissionSet
from trajectory.AdsBtrajectories.utils import extendDataSetWithAirportData
from trajectory.AdsBtrajectories.utils import extendDataSetWithDates


if __name__ == '__main__':

    df = readSubmissionSet()
    print ( list ( df ) )
    print ( "number of rows = {0}".format ( len(df.index) ) )


    df = extendDataSetWithAirportData(df)
    print ( list ( df ) )
    print ( "number of rows = {0}".format ( len(df.index) ) )
    
    df = extendDataSetWithDates (df)
    
    print ( list ( df ) )
    print ( "number of rows = {0}".format ( len(df.index) ) )
    
    for index, row in df.iterrows():
        print ("-------------")
        if ( index < 10 ):
            print(index , row)
        else:
            break


