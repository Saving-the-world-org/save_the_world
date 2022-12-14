# -*- coding: utf-8 -*-
import logging
import streamlit as st
import streamlit.components.v1 as components
from src.utils.dataio import get_data
from src.utils.minter import *
from dotenv import load_dotenv

# Load the environment variables
load_dotenv()
contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
contract_abi = os.getenv("ABI_PATH")
ipfs_uri = os.getenv("IPFS_URI")
recipient_df = get_data("SELECT * from DONATIONS")

# Begin Streamlit calls
st.set_page_config(layout="wide")

def main(df):
    #Header information 
    st.title("Resources", anchor=None)
    st.subheader("Available items for donation.")
    st.caption("TODO: Perhaps make this page show a row for each type of resource, then a breakdown of size/qty available... instead of showing a table.", unsafe_allow_html=False)
    st.write(df)

def load_data():
    # Get all current resources from the donations table in the database
    query_str = "SELECT * FROM DONATIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
