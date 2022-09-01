# -*- coding: utf-8 -*-
import logging
import streamlit as st
from src.utils.dataio import get_data, init_data
import streamlit.components.v1 as components
from sqlalchemy import inspect, create_engine

st.set_page_config(layout="wide")

def main():
    #Header information 
    st.title("Local Data", anchor=None)
    st.markdown("Manage database, users, etc.")
    st.markdown("---")
    org_query="SELECT * FROM ORGANIZATIONS;"
    org_df = get_data(org_query)
    donations_query="SELECT * FROM DONATIONS;"
    donations_df = get_data(donations_query)
    transactions_query="SELECT * FROM TRANSACTIONS;"
    transactions_df = get_data(transactions_query)
    cities_query="SELECT * FROM CITIES;"
    cities_df = get_data(cities_query)
    st.write("ORGANIZATION")
    st.dataframe(org_df)
    st.write("---")
    st.write("TRANSACTIONS")
    st.dataframe(transactions_df)
    st.write("---")
    st.write("DONATIONS")
    st.dataframe(donations_df)
    st.write("---")
    st.write("CITIES")
    st.dataframe(cities_df)


@st.cache
def load_data():
    return
    # transaction_query = "SELECT * FROM TRANSACTIONS LIMIT 50;"
    # df = get_data(transaction_query)
    # return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    # df = load_data()
    main()
