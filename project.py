# This is my module for my Time Series Mini Project

import pandas as pd
import numpy as np
from datetime import timedelta, datetime
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

################### Data Acquistion ###########################

def get_raleigh():
    df = pd.read_csv('GlobalLandTemperaturesByCity.csv.zip')
    df = df[df['City']=='Raleigh']
    return df

############## Initial Prep ###################################

def to_datetime(df, col):
    df[col] = pd.to_datetime(df[col]).sort_values()
    return df

def index_reset(df, col):
    df = df.set_index(col).sort_index()
    return df

def drop_nulls(df):
    df = df.dropna()
    return df

def drop_cols(df):
    df = df.drop(columns=(['City', 'Country', 'Latitude', 'Longitude']))
    return df

def rename_cols(df):
    df = df.rename(columns=({'AverageTemperature': 'avg_temp', 'AverageTemperatureUncertainty': 'avg_temp_uncertainty'}))
    return df

def drop_oldies(df):
    df = df.loc['1900':]
    return df

def initial_prep(df, col):
    df = to_datetime(df, col)
    df = index_reset(df, col)
    df = drop_nulls(df)
    df = drop_cols(df)
    df = rename_cols(df)
    df = drop_oldies(df)
    return df

def add_month_col(df):
    df['month'] = df.index.strftime('%m-%b')
    return df

def correlation(y, lag):
    return pd.concat([y, y.shift(lag)], axis=1).dropna().corr().iloc[0, 1]

def evaluate(target_var):
    '''
    This function will take the actual values of the target_var from validate, 
    and the predicted values stored in yhat_df, 
    and compute the rmse, rounding to 0 decimal places. 
    it will return the rmse. 
    '''
    rmse = round(sqrt(mean_squared_error(validate[target_var], yhat_df[target_var])), 0)
    return rmse

def plot_and_eval(target_var):
    '''
    This function takes in the target var name (string), and returns a plot
    of the values of train for that variable, validate, and the predicted values from yhat_df. 
    it will als lable the rmse. 
    '''
    plt.figure(figsize = (12,4))
    plt.plot(train[target_var], label='Train', linewidth=1)
    plt.plot(validate[target_var], label='Validate', linewidth=1)
    plt.plot(yhat_df[target_var])
    plt.title(target_var)
    rmse = evaluate(target_var)
    print(target_var, '-- RMSE: {:.0f}'.format(rmse))
    plt.show()
    
# function to store the rmse so that we can compare
def append_eval_df(model_type, target_var):
    '''
    this function takes in as arguments the type of model run, and the name of the target variable. 
    It returns the eval_df with the rmse appended to it for that model and target_var. 
    '''
    rmse = evaluate(target_var)
    d = {'model_type': [model_type], 'target_var': [target_var],
        'rmse': [rmse]}
    d = pd.DataFrame(d)
    return eval_df.append(d, ignore_index = True)
