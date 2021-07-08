# This is my module for my Time Series Mini Project

import pandas as pd
import numpy as np
from datetime import timedelta, datetime

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
