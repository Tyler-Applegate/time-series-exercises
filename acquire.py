# This is my Time Series Data Acquisition Module

########################### General Imports ####################################
import pandas as pd
import requests
import os

########################### New Data Acquistion ###############################

def new_items():
    '''
    This function is specific to Zach's lol grocery dataset. It will itirate through each
    page of items and return a pandas DataFrame of all items.
    '''
    items_list = []
    base_url = 'https://python.zach.lol/api/v1'
    response = requests.get(base_url + '/items')
    data = response.json()
    n = data['payload']['max_page']

    for i in range(1,n+1):
        url = 'https://python.zach.lol/api/v1/items?page='+str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['items']
        items_list += page_items
        
    return pd.DataFrame(items_list)

def new_stores():
     '''
    This function is specific to Zach's lol grocery dataset. It will itirate through each
    page of stores and return a pandas DataFrame of all stores.
    '''   
    items_list = []
    base_url = 'https://python.zach.lol/api/v1'
    response = requests.get(base_url + '/stores')
    data = response.json()
    n = data['payload']['max_page']

    for i in range(1, n+1):
        url = 'https://python.zach.lol/api/v1/stores?page='+str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['stores']
        items_list += page_items

    return pd.DataFrame(item_list)

def new_sales():
     '''
    This function is specific to Zach's lol grocery dataset. It will itirate through each
    page of sales and return a pandas DataFrame of all sales.
    '''   
    items_list = []
    base_url = 'https://python.zach.lol/api/v1'
    response = requests.get(base_url + '/sales')
    data = response.json()
    n = data['payload']['max_page']

    for i in range(1,n+1):
        url = 'https://python.zach.lol/api/v1/sales?page='+str(i)
        response = requests.get(url)
        data = response.json()
        page_items = data['payload']['sales']
        items_list += page_items
        
    return pd.DataFrame(items_list)

def new_opsd():
    OPSD = pd.read_csv('https://raw.githubusercontent.com/jenfly/opsd/master/opsd_germany_daily.csv')
    return OPSD

############################# Data to CSV ####################################

def items_csv():
    items = get_items()
    return items.to_csv('grocery_items.csv')

def stores_csv():
    stores = get_stores()
    return stores.to_csv('grocery_stores.csv')

def sales_csv():
    sales = get_sales()
    return sales.to_csv('grocery_sales.csv')

def opsd_csv():
    opsd = get_opsd()
    return opsd.to_csv('opsd_germany.csv')

######################## Merge Data #############################################

def all_groceries():
    
    items_df = pd.read_csv('grocery_items.csv')
    stores_df = pd.read_csv('grocery_stores.csv')
    sales_df = pd.read_csv('grocery_sales.csv')
    sales_stores_df = pd.merge(sales_df, stores_df, left_on='store', right_on='store_id', how='left')
    sales_stores_items_df = pd.merge(sales_stores_df, items_df, left_on='item', right_on='item_id', how='left')
    sales_stores_items_df = sales_stores_items_df.drop(columns=['Unnamed: 0_x', 'Unnamed: 0_y', 'Unnamed: 0'])
    
    return sales_stores_items_df

######################## Get Data from CSV #####################################

def get_items():
    
    if os.path.isfile('grocery_items.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('grocery_items.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_items()
        # Cache data
        df.to_csv('grocery_items.csv')

    return df

def get_stores():
    
    if os.path.isfile('grocery_stores.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('grocery_stores.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_stores()
        # Cache data
        df.to_csv('grocery_stores.csv')

    return df

def get_sales():
    
    if os.path.isfile('grocery_sales.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('grocery_sales.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_sales()
        # Cache data
        df.to_csv('grocery_sales.csv')

    return df

def get_opsd():
    
    if os.path.isfile('opsd_germany.csv'):
        # If csv file exists read in data from csv file.
        df = pd.read_csv('opsd_germany.csv', index_col=0)
        
    else:
        # Read fresh data from db into a DataFrame
        df = new_opsd()
        # Cache data
        df.to_csv('opsd_germany.csv')

    return df

####################### Playland Playtime Functions #################################

#Function to take in any csv and create a dataframe
def csv_to_dataframe(url, key1, key2=None):
    # Let's take an example url and make a get request
    response = requests.get(url)
    #create dictionary object
    data= response.json()
    if key2 != None:
        data_list = response.json()[key1][key2]
    else:
        data_list = response.json()[key1]
        df= pd.DataFrame(data_list)
    return df

