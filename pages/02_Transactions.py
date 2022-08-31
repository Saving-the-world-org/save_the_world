import logging
import streamlit as st
from src.utils.dataio import get_data
import streamlit.components.v1 as components

# Begin Streamlit calls
st.set_page_config(layout="wide")

def main(df):
    #Header information 
    st.title("Transactions", anchor=None)
    st.subheader("Incididunt ut labore et dolore magna aliqua.")
    st.write(df)

def load_data():
    query_str = "SELECT * FROM TRANSACTIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
