'''
Created on 15 oct. 2024

@author: robert
'''

from trajectory.AdsBtrajectories.utils import readChallengeSet
from trajectory.AdsBtrajectories.utils import readSubmissionSet
from trajectory.AdsBtrajectories.utils import extendDataSetWithAirportData
from trajectory.AdsBtrajectories.utils import extendDataSetWithDates


from sklearn import ensemble
from sklearn.metrics import mean_squared_error , root_mean_squared_error
from trajectory.AdsBtrajectories.utils import encodeCategoryColumn
import pandas as pd


def convert_airlines_keys(unique_airlines_values , rowValue):
    order = 0
    for unique_airline_value in unique_airlines_values:
        if ( unique_airline_value == rowValue ):
            return "airline" + "_" + str(order)
        order = order + 1
    return 0

if __name__ == '__main__':
    
    df_challenge = readChallengeSet()
    print ( list ( df_challenge ) )
    print( df_challenge.shape )
    
    df_challenge = extendDataSetWithDates (df_challenge)
    print ( df_challenge.shape )
    
    df_submission = readSubmissionSet()
    print ( list ( df_submission ) )
    print( df_submission.shape )
    
    df_submission = extendDataSetWithDates ( df_submission )
    print ( df_submission.shape )
    
    print( "--- concat challenge and submission ---")
    df = pd.concat([df_challenge,df_submission], ignore_index=True)
    print ( df.shape )
    print ( list ( df ))
    print ( "number of rows = {0}".format ( len(df.index) ) )

    print ("---- add airports extension ---")
    df = extendDataSetWithAirportData(df)
    print ( list ( df ) )
    print ( "number of rows = {0}".format ( len(df.index) ) )
        
    ''' drop unused columns '''
    ''' airline column must be dropped because string cannot be converted to float '''
    df = df.drop(columns=['flight_id', 'callsign', 'actual_offblock_time','arrival_time'])
    print ( list ( df ))
    
    print ("--- encode airline ---")
    unique_airlines_keys = df['airline'].unique()
    print("unique airlines = {0}".format((unique_airlines_keys)))
    print("number of unique airlines = {0}".format(len(unique_airlines_keys)))
        

    df['airline'] = df['airline'].apply( lambda x : convert_airlines_keys(unique_airlines_keys, x) )
        
    ''' encoding airline, aircraft type and wtc  '''
    
    oheAirline , df_encoded_airline , final_df = encodeCategoryColumn( df , 'airline' )
    oheAircraftType , df_encoded_aircraft_type, final_df = encodeCategoryColumn( final_df , 'aircraft_type')
    oheWTC , df_encoded_wtc , final_df = encodeCategoryColumn(final_df  , 'wtc')
    
    print ( list ( final_df ))
    print(final_df.head(10))
    
    print ( '--- keep only records with tow being not null ---')
    tow_not_null_df = final_df[final_df['tow'].notnull()]
    
    print ("---- build the train dataset ---")
    ''' Creating a dataframe with 80% values of original dataframe '''
    train_df = tow_not_null_df.sample(frac = 0.8)
    print ( train_df.shape  )
    
    print ("---- get the test dataset  ---")

    test_df = tow_not_null_df.drop(train_df.index)
    print ( test_df.shape )
    
    print ("--- drop tow row in train ---")
    X_train = train_df.drop(columns=['tow'])
    print ( X_train.shape )

    print ("--- Y train ---")
    # Keep only 'team' and 'points' column
    Y_train = train_df[train_df['tow'].notnull()]
    Y_train = Y_train[['tow']]
    print ( Y_train.shape )
    
    reg = ensemble.GradientBoostingRegressor()
    reg.fit(X_train, Y_train)
    
    print ("---- build X_test ---")
    
    X_test = test_df.drop(columns=['tow'])
    print ( X_test.shape )

    print ("--- build Y test to compare with ---")
    Y_test = test_df[['tow']]
    print ( Y_test.shape )

    print ("--- compute Y predictions from X test --- ")
    Y_predict = reg.predict(X_test)
    print ( Y_predict.shape )
    
    print("--- compute RMSE ---")
    rmse = root_mean_squared_error( Y_test, Y_predict )
    print("The root mean squared error (MSE) on test set: {:.4f}".format(rmse))

    mse = mean_squared_error ( Y_test , Y_predict )
    print("The mean squared error (MSE) on test set: {:.4f}".format(mse))

    print ("--- inverse transform ---")
    


