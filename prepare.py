# This is my Data Preparation Module for Time Series

import pandas as pd
import requests
import numpy as np
from datetime import timedelta, datetime

################## Grocery Functions #################################

def to_datetime(df, col):
    df[col] = pd.to_datetime(df[col]).sort_values()
    return df

def index_reset(df, col):
    df = df.set_index(col).sort_index()
    return df

def day_of_week(df):
    df['day_of_week'] = df.index.day_name()
    return df

def add_month_col(df):
    df['month'] = df.index.month_name()
    return df

def update_sales(df):
    df = df.rename(columns=({'sale_amount': 'sale_qty'}))
    df['sale_qty'] = df['sale_qty'].astype(int)
    return df

def create_sales_total(df):
    df['sales_total'] = df['sale_qty'] * df['item_price']
    return df

def prep_groceries(df, col):
    df = to_datetime(df, col)
    df = index_reset(df, col)
    df = day_of_week(df)
    df = add_month_col(df)
    df = update_sales(df)
    df = create_sales_total(df)
    return df


############ OPSD Functions ####################################

def to_datetime(df, col):
    df[col] = pd.to_datetime(df[col]).sort_values()
    return df

def index_reset(df, col):
    df = df.set_index(col).sort_index()
    return df

def make_year(df):
    df = df.index.year
    return df

def fill_missing(df):
    df = df.fillna(value=0)

def prep_opsd(df, col):
    df = to_datetime(df, col)
    df = index_reset(df, col)
    df = add_month_col(df)
    df = make_year(df)
    df = fill_missing(df)
    return df

