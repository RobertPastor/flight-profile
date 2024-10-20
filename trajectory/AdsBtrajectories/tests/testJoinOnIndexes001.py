'''
Created on 20 oct. 2024

@author: robert
'''

import pandas as pd
import numpy as np


if __name__ == '__main__':

    columns = ['A','B']
    np_data = np.array([[1,2] , [1,5] , [2,3]])
    df1 = pd.DataFrame(np_data,columns=columns)
    
    df1.reset_index(drop=True, inplace=True)

    print ( df1.shape )
    print ( list ( df1 ) )
    print ( df1.head() )
    
    columns = ['C']
    np_data = np.array([[8] , [9] , [10]])
    
    df2 = pd.DataFrame(np_data,columns=columns)
    df2.reset_index(drop=True, inplace=True)
    
    print ( df2.shape )
    print ( list ( df2 ) )
    print ( df2.head() )
    
    df3 = pd.merge( df1, df2, left_index=True, right_index=True)
    print ( df3.shape )
    print ( list ( df3 ) )
    print ( df3.head() )
