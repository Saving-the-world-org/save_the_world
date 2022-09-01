# -*- coding: utf-8 -*-
import os
import logging
import streamlit as st
from src.utils.dataio import init_data, get_data
import streamlit.components.v1 as components
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()

contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
contract_abi = os.getenv("ABI_PATH")

# Begin Streamlit
st.set_page_config(layout="wide")

def main(df):
    # Page Header information
    st.title("Humanitarian Aid Supply Chain Tracker Tool", anchor=None)
    st.write("##### Authors: Phoebe Gunter, Harry Oestreicher, Abhishek Banerjee, Gabriel Paganin, Gerald Cortright, & Javier")
    st.write("This app enabled you to safetly track donating and receiving aid products on a blockchain. Portability allows users developers to deploy and interact with the ERC721 Smart Contract locally, then switch to almost any ethereum blockchain.")
    st.image("https://www.bbva.com/wp-content/uploads/en/2017/07/blockchain-humanitario.jpg", width=600)
    return

# @st.cache
def load_data():
    query_str = "SELECT * FROM DONATIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)