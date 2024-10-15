'''
Created on 15 oct. 2024

@author: robert
'''

from trajectory.AdsBtrajectories.utils import readChallengeSet
from datetime import datetime


if __name__ == '__main__':
    
    print("Read challenge set file")
    
    df = readChallengeSet()
    if ( not df is None ) :

        print ( list ( df ) )
        print ( "number of rows = {0}".format ( len(df.index) ) )
        
        for index, row in df.iterrows():
            if ( index < 100 ):
                print("-----------")
                print(index, row['flight_id'],  row['aircraft_type'] , row['date'] )
                date = datetime.strptime(row['date'], '%d/%m/%Y' )
                print ( datetime.strptime(row['date'], '%d/%m/%Y' ) )
                print ( date.isoweekday() )
                print(f"The ISO day of the week is: {date.isoweekday()}")
                iso_year, iso_week, iso_weekday = date.isocalendar()
                
                print(f"ISO Year: {iso_year}, ISO Week Number: {iso_week}, ISO Weekday: {iso_weekday}")


