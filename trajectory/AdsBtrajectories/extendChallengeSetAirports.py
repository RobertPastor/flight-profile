'''
Created on 15 oct. 2024

@author: robert

'''

from trajectory.AdsBtrajectories.utils import readChallengeSet
from trajectory.AdsBtrajectories.Airports.AirportDatabaseFile import AirportsDatabase


if __name__ == '__main__':
    
    print ( "Read airports database ")
    
    airportsDatabase = AirportsDatabase()
    airportsDBOk = airportsDatabase.read()
    print ( airportsDBOk )
    
    print("Read challenge set file")
    
    df = readChallengeSet()
    if ( not df is None ) and ( airportsDBOk == True):

        print ( list ( df ) )
        print ( "number of rows = {0}".format ( len(df.index) ) )
        
        print ( "--- start adding adep ades informations ----")
        ''' create a new column '''
        df["adep_elevation_meters"] = df.apply(lambda row: airportsDatabase.getAirportElevationMeters(row['adep']), axis=1)
        df["ades_elevation_meters"] = df.apply(lambda row: airportsDatabase.getAirportElevationMeters(row['ades']), axis=1)
        
        df['adep_latitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLatitudeDegrees(row['adep']), axis=1)
        df['adep_longitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLongitudeDegrees(row['adep']), axis=1)

        df['ades_latitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLatitudeDegrees(row['ades']), axis=1)
        df['ades_longitude_degrees'] = df.apply(lambda row: airportsDatabase.getAirportLongitudeDegrees(row['ades']), axis=1)
        
        df['adep_ades_GC_Nm'] = df.apply(lambda row: airportsDatabase.computeDistanceNm( row['adep'] , row['ades']), axis=1)

        
        print ("------- end adding adep ades informations ----------")
        
        for index, row in df.iterrows():
            if ( index < 100 ):
                print("-----------")
                print(index, row['flight_id'],  row['aircraft_type'] , row['adep'] , row["adep_elevation_meters"])
                print(index, row['flight_id'],  row['aircraft_type'] , row['ades'] , row["ades_elevation_meters"])
                print(index ,row['flight_id'],  row['aircraft_type'] , row['adep'] , row['adep_latitude_degrees'], row['adep_longitude_degrees'])
                print(index ,row['flight_id'],  row['aircraft_type'] , row['ades'] , row['ades_latitude_degrees'], row['ades_longitude_degrees'])
            else:
                break
        
        
