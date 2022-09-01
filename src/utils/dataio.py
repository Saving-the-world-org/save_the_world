# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from pathlib import Path
from csv import writer
from sqlalchemy import inspect, create_engine

connection_string = 'sqlite:///./src/data/stw_data.db'
engine = create_engine(connection_string)
insp = inspect(engine)

cities_file = Path("./src/data/cities.csv")
donations_file = Path("./src/data/donations.csv")
organizations_file = Path("./src/data/organizations.csv")
transactions_file = Path("./src/data/transactions.csv")

def init_data(): 
    cities_df = pd.read_csv(cities_file)
    donations_df = pd.read_csv(donations_file)
    organizations_df = pd.read_csv(organizations_file)
    transactions_df = pd.read_csv(transactions_file)

    cities_df.to_sql('CITIES', engine, index=False, if_exists='replace')
    donations_df.to_sql('DONATIONS', engine, index=False, if_exists='replace')
    organizations_df.to_sql('ORGANIZATIONS', engine, index=False, if_exists='replace')
    transactions_df.to_sql('TRANSACTIONS', engine, index=False, if_exists='replace')

def get_data(query):
    df = pd.read_sql_query(query, con=engine)
    return df
    
def create_transaction(recipient_name, tx_hashHex, timestamp, recipient_account, ipfs_link, donor_account, category, city, resource_name, initial_appraisal_value):

    # Row=[recipient_name, tx_hashHex, timestamp, recipient_account, ipfs_link, donor_account, category, city, resource_name, initial_appraisal_value]

    insert_data=f"""
    INSERT INTO TRANSACTIONS ('recipient_name', 'tx_hash', 'timestamp', 'recipient_account', 'resource_uri', 'donor_account', 'category', 'city', 'resource_name', 'USD') 
    VALUES ('{recipient_name}', '{tx_hashHex}', '{timestamp}', '{recipient_account}', '{ipfs_link}', '{donor_account}', '{category}', '{city}', '{resource_name}', '{initial_appraisal_value}');
    """
    engine.execute(insert_data)

    ## This approach didn't work since the process wouldn't release the file
    # transactions_file = Path("./src/data/transactions_ho.csv")
    # with open(transactions_file,'w', newline='') as file_object:
    #     writer_object = writer(file_object)
    #     writer_object.writerow(Row)
    #     file_object.close()
    # # Keep the SQL table in sync with teh local csv file ;)
    # df = pd.read_csv(transactions_file)
    # df.to_sql('TRANSACTIONS', engine, index=False, if_exists='append')

    return

def read_transaction(query):

    return

def update_transaction(query):

    return

def delete_transaction(query):

    return
    
