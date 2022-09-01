# -*- coding: utf-8 -*-
import logging
import numpy as np
import streamlit as st
import streamlit.components.v1 as components
from src.utils.dataio import get_data
from sqlalchemy import inspect, create_engine

connection_string = 'sqlite:///./src/data/stw_data.db'
engine = create_engine(connection_string)
insp = inspect(engine)

cities_df = get_data("SELECT * FROM CITIES;")
donations_df = get_data("SELECT * FROM DONATIONS;")
org_df = get_data("SELECT * FROM ORGANIZATIONS;")

# Begin Streamlit calls
st.set_page_config(layout="wide")

def get_city_for_org(org_name): 
    city_name = org_df.loc[org_name, 'City']
    return city_name

def get_phone_for_org(org_name): 
    phone = org_df.loc[org_name, 'Phone']
    #st.write(type(phone))
    if isinstance(phone, np.integer):
        phone = phone
    else:
        phone = phone[0]
    phone = str(phone)
    return phone

def get_cred_for_org(org_name): 
    cred = org_df.loc[org_name, 'Credibility']
    if isinstance(cred, np.integer):
        cred = cred
    else:
        cred = cred[0]
    cred = str(cred)
    return cred

def get_url_for_org_img(org_name): 
    url = org_df.loc[org_name, 'Url']
    return f"src/images/logos/{url}"

def main(df):
    #Header information 
    st.title("Explore Organizations")
    st.subheader("You can donate to...")

    for i in org_df.index.drop_duplicates():
        col1, col2 = st.columns(2)
        with col1:
            # city = get_city_for_org(i)
            org = org_df.iloc[i]["Organization"]
            st.write("City: " + get_city_for_org(i))
            st.write("Phone Number: " + get_phone_for_org(i))
            st.write("Credibility Rating (out of 5): " + get_cred_for_org(i) )
            if st.button(f"Donate to {org}", i):
                pass

        with col2:
            st.image(get_url_for_org_img(i), width=200)

        st.write("---")

def load_data():
    query_str = "SELECT * FROM ORGANIZATIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
