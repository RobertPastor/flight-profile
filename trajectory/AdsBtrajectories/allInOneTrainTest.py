'''
Created on 15 oct. 2024

@author: rober
'''

from trajectory.AdsBtrajectories.utils import readChallengeSet
from trajectory.AdsBtrajectories.utils import readSubmissionSet
from trajectory.AdsBtrajectories.utils import extendDataSetWithAirportData
from trajectory.AdsBtrajectories.utils import extendDataSetWithDates

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer

from sklearn import ensemble
from sklearn.metrics import mean_squared_error , root_mean_squared_error


from numpy import mean
from numpy import std

import pandas as pd

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
    df = df.drop(columns=['flight_id', 'callsign', 'actual_offblock_time','arrival_time', 'airline'])
    print ( list ( df ))
    
    #for index, row in df.iterrows():
    #    print ("-------------")
    #    if ( index < 10 ):
    #       print(index , row)
    #    else:
    #        break
        
    ''' encoding aircraft type and wtc  '''
    columnNameList = ['aircraft_type','wtc']
    transformer = make_column_transformer( (OneHotEncoder(), columnNameList ), remainder='passthrough')
    
    transformed = transformer.fit_transform(df)
    print ( transformer.get_feature_names_out() )

    #transformed_df = pd.DataFrame(transformed, columns=columnNameList)
    transformed_df = pd.DataFrame(transformed, columns=transformer.get_feature_names_out())
    
    print ( list ( transformed_df ))
    print(transformed_df.head(10))
    
    print ( '--- keep only records with tow being not null ---')
    tow_not_null_df = transformed_df[transformed_df['remainder__tow'].notnull()]
    
    print ("---- build the train dataset ---")
    # Creating a dataframe with 80%
    # values of original dataframe
    train_df = tow_not_null_df.sample(frac = 0.8)
    print ( train_df.shape  )
    
    print ("---- get the test dataset  ---")

    test_df = tow_not_null_df.drop(train_df.index)
    print ( test_df.shape )
    
    print ("--- drop tow row in train ---")
    X_train = train_df.drop(columns=['remainder__tow'])
    print ( X_train.shape )

    print ("--- Y train ---")
    # Keep only 'team' and 'points' column
    Y_train = train_df[train_df['remainder__tow'].notnull()]
    Y_train = Y_train[['remainder__tow']]
    print ( Y_train.shape )
    
    reg = ensemble.GradientBoostingRegressor()
    reg.fit(X_train, Y_train)
    
    print ("---- build X_test ---")
    
    X_test = test_df.drop(columns=['remainder__tow'])
    print ( X_test.shape )

    print ("--- build Y test to compare with ---")
    Y_test = test_df[['remainder__tow']]
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
    


