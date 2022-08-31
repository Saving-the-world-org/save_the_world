import logging
import streamlit as st
import streamlit.components.v1 as components
from src.utils.dataio import get_data
from src.utils.minter import *
from src.utils.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json

from dotenv import load_dotenv
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
    st.subheader("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    st.caption("work in progress ", unsafe_allow_html=False)
    st.write(df)

def load_data():
    query_str = "SELECT * FROM DONATIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
