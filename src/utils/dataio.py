# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
from csv import writer
from sqlalchemy import inspect, create_engine

# Establish and define database connection
connection_string = 'sqlite:///./src/data/stw_data.db'
engine = create_engine(connection_string)
insp = inspect(engine)

# Initialization data for demo and reproducable output
cities_file = Path("./src/data/cities.csv")
donations_file = Path("./src/data/donations.csv")
organizations_file = Path("./src/data/organizations.csv")
transactions_file = Path("./src/data/transactions.csv")

def init_data():
    """
    Purpose:
        Initialize system data from local CSV files for reproducability
    Input:
        None
    Output (pd.DataFrame):
        Produces pandas DataFrames and corresponding SQL tables in SQLlite db file.
    
    """
    cities_df = pd.read_csv(cities_file)
    donations_df = pd.read_csv(donations_file)
    organizations_df = pd.read_csv(organizations_file)
    transactions_df = pd.read_csv(transactions_file)

    cities_df.to_sql('CITIES', engine, index=False, if_exists='replace')
    donations_df.to_sql('DONATIONS', engine, index=False, if_exists='replace')
    organizations_df.to_sql('ORGANIZATIONS', engine, index=False, if_exists='replace')
    transactions_df.to_sql('TRANSACTIONS', engine, index=False, if_exists='replace')

def get_data(query):
    """
    Purpose:
        To return a dataframe to be used on the caller's page.
    Input (Str):
        Any SQL query string to perform on db
    Returns (pd.DataFrame):
        Pandas dataframe object

    """
    df = pd.read_sql_query(query, con=engine)
    return df
    
def create_transaction(recipient_name, tx_hashHex, timestamp, recipient_account, ipfs_link, donor_account, category, city, resource_name, initial_appraisal_value):
    """
    Purpose:
        Function to collect data from page UI and feed into SQL query and INSERT into the local database.
    Input:
        field values from pages/02_Donate.py page
    Returns:
        Inserts a row into TRANSACTIONS SQL table
    """

    insert_data=f"""
    INSERT INTO TRANSACTIONS ('recipient_name', 'tx_hash', 'timestamp', 'recipient_account', 'resource_uri', 'donor_account', 'category', 'city', 'resource_name', 'USD') 
    VALUES ('{recipient_name}', '{tx_hashHex}', '{timestamp}', '{recipient_account}', '{ipfs_link}', '{donor_account}', '{category}', '{city}', '{resource_name}', '{initial_appraisal_value}');
    """
    engine.execute(insert_data)

    return
