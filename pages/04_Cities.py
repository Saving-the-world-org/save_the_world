import logging
import streamlit as st
from src.utils.dataio import get_data
import streamlit.components.v1 as components

# Begin Streamlit calls
st.set_page_config(layout="wide")

def main(df):
    #Header information 
    st.title("Organization Locations", anchor=None)
    st.subheader("These are the locatins of our affiliate organizations.")
    st.caption("TODO: This page might go away.  But it can be used as a template for creating other pages.", unsafe_allow_html=False)
    st.write(df)

def load_data():
    query_str = "SELECT * FROM CITIES;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
