import logging
import numpy as np
import pandas as pd

import streamlit as st
from src.utils.dataio import get_data
import streamlit.components.v1 as components
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

# from bokeh.models.widgets import Div

mahscript = """
    <script>
        function haveSomeClass(){
            var elements = window.parent.document.querySelectorAll('.css-1q8dd3e')
            elements[0].innerText = 'reloaded';
            elements[0].disabled = true;
        }
    </script
     """

def main(df):
    #Header information 
    st.title("Explore Organizations")
    st.subheader("You can donate to...")

    for i in org_df.index.drop_duplicates():
        col1, col2 = st.columns(2)
        with col1:
            # city = get_city_for_org(i)
            org = org_df.iloc[i]["Organization"]
            st.subheader(org, get_city_for_org(i))
            st.write("Phone Number: " + get_phone_for_org(i))
            st.write("Credibility Rating (out of 5): " + get_cred_for_org(i) )
            if st.button(f"Donate to {org}", i):
                pass
                # js = "window.location.href = '/Donations_Test_ho'"  # Current tab
                # html = '<img src onerror="{}">'.format(js)
                # div = Div(text=html)
                # st.bokeh_chart(div)

        with col2:
            # get_url_for_org_img(i)
            # short_name = i.replace(" ", "")
            # url = "https://github.com/Saving-the-world-org/saving_the_world_app/blob/edcd26a335fe3c6e99f17cd194a5491f913be26d/images/" + short_name + ".png"
            # st.write(url)
            # st.image(url, caption = i)
            # st.markdown(f"<img src=\"{get_url_for_org_img(i)}\" style=\"max-width:200px; max-height:200px;\" />", unsafe_allow_html=True)
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
