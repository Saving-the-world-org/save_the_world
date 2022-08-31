# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
from csv import writer
from sqlalchemy import inspect, create_engine
connection_string = 'sqlite:///./src/data/stw_data.db'
engine = create_engine(connection_string)
insp = inspect(engine)

def init_data():
    cities_df = pd.read_csv(Path("./src/data/cities.csv"))
    donations_df = pd.read_csv(Path("./src/data/donations_ho.csv"))
    organizations_df = pd.read_csv(Path("./src/data/organizations_ho.csv"))
    transactions_df = pd.read_csv(Path("./src/data/transactions_ho.csv"))
    cities_df.to_sql('CITIES', engine, index=False, if_exists='replace')
    donations_df.to_sql('DONATIONS', engine, index=False, if_exists='replace')
    organizations_df.to_sql('ORGANIZATIONS', engine, index=False, if_exists='replace')
    transactions_df.to_sql('TRANSACTIONS', engine, index=False, if_exists='replace')

def get_data(query):
    df = pd.read_sql_query(query, con=engine)
    return df
    
"""
These will be our local db management CRUD functions
"""
def create_transaction(recipient_name, tx_hashHex, timestamp, recipient_account, ipfs_link, donor_account, 
                    category, lat_long, resource_name, initial_appraisal_value):

    Row=[recipient_name, tx_hashHex, timestamp, recipient_account, ipfs_link, donor_account, 
                category, lat_long, resource_name, initial_appraisal_value]
    
    # Open our existing CSV file in append mode
    with open(Path("./src/data/Transactions_ho.csv"), "a") as f_object:
        writer_object = writer(f_object)
        writer_object.writerow(Row)
        f_object.close()
    return

def read_transaction(query):

    return

def update_transaction(query):

    return

def delete_transaction(query):

    return
    
