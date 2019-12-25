# -*- coding: utf-8 -*-
"""
Created on 9/13/2019

This is to collect the functions/tools used in different scenarios.

@author: Yuxing
"""

import numpy as np
import pandas as pd

##################################################################################################

def handle_non_numerical_data(df, text_digit_vals = dict()):
    '''
    This function transforms the non-numerical values in the dataframe into integers.
    
    text_digit_vals: dictionary (column name to mapping) of dictionary (mapping from string to digits)
    
    If the "text_digit_vals" is provided, then this will be directly used, such as converting test data
    using the same dictionary from the training data.
    
    If it's not provided, then the function collects the unique values for those columns which 
    are not integer or float values,and assign an integer values: 0,1,2,3... to each string.
    
    The output is a dataframe with these columns transformed, and the map used.
    '''
    if not isinstance(df, pd.DataFrame):
        df = pd.DataFrame(df)
    
    columns = df.columns.values
    
    # the mapping from string to int is provided. It's likely we are processing test data.
    if len(text_digit_vals) > 0:
        for column in columns:
            def convert_to_int(val):
                # convert val in each column into integers
                if val in text_digit_vals[column]:
                    return text_digit_vals[column][val]
                else:
                    return np.nan
            if df[column].dtype != np.int64 and df[column].dtype != np.float64:
                df[column] = list(map(convert_to_int, df[column]))
     
    # the mapping from string to int is not provided. It's likely we are processing training data.
    else:
        
        text_digit_vals = dict()
        from copy import deepcopy
        
        for column in columns:
            col_map = dict()
            
            def convert_to_int2(val):
                # convert val in each column into integers
                return col_map[val]

            if df[column].dtype != np.int64 and df[column].dtype != np.float64:
                column_contents = df[column].values.tolist()
                unique_elements = set(column_contents)
                x = 0
                for unique in unique_elements:
                    if unique not in text_digit_vals:
                        col_map[unique] = x
                        x+=1

                df[column] = list(map(convert_to_int2, df[column]))
                
            text_digit_vals[column] = deepcopy(col_map)
                
    return df, text_digit_vals

##################################################################################################


# http://superfluoussextant.com/making-gifs-with-python.html

# make gif from the saved figures
import glob
import moviepy.editor as mpy

gif_name = 'trail_2'
fps = 3
file_list = glob.glob('*.png') # Get all the pngs in the current directory
list.sort(file_list, key=lambda x: int(x.split('_')[1].split('.png')[0])) # Sort the images by #, this may need to be tweaked for your use case
clip = mpy.ImageSequenceClip(file_list, fps=fps)
clip.write_gif('{}.gif'.format(gif_name), fps=fps)


