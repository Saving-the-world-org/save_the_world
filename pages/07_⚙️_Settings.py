# -*- coding: utf-8 -*-
import logging
import streamlit as st
from src.utils.dataio import get_data, init_data
import streamlit.components.v1 as components
 
# Begin Streamlit calls
st.set_page_config(layout="wide")

def main():
    #Header information 
    st.title("System Settings and Data", anchor=None)
    st.markdown("Manage database, users, etc.")
    st.markdown("---")

    btn =  st.button("RESET ALL db tables")
    if btn:
        # re-initialize the database
        init_data()
        # Display the tables
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

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    main()
