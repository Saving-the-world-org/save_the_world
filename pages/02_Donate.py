# -*- coding: utf-8 -*-
import datetime
import logging
from turtle import color
import streamlit as st
import streamlit.components.v1 as components
from src.utils.dataio import get_data, create_transaction
from src.utils.minter import *
from src.utils.pinata import pin_image
from web3 import Web3
from dotenv import load_dotenv

# Load the required variables from .env file
load_dotenv()

contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
contract_abi = os.getenv("ABI_PATH")
ipfs_uri = os.getenv("IPFS_URI")
recipient_df = get_data("SELECT Organization, City, Address from ORGANIZATIONS")
categories_df = get_data("SELECT DISTINCT Category from DONATIONS")
resources_df = get_data("SELECT Category, Item, QtySize, USD, Tags from DONATIONS")
donor_account = os.getenv("PUBLIC_KEY")
# Instantiate a web3 object inline
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))


# Begin Streamlit calls
st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def load_contract():
    # Load the contract address into an object using the ABI code and smart contract address
    with open(contract_abi) as f:
        this_abi = json.load(f)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    contract = w3.eth.contract(
        address=contract_address,
        abi=this_abi
    )
    return contract

contract = load_contract()

col1, col2 = st.columns([3, 1])

def main(df):

    with col1:
        # Header information 
        st.title("Make a Donation", anchor=None)
        st.write("WIP page for testing minting process with local image files instead of streamlit uploaded file.")

        # Selectbox for recipient Org-City-Address (JOIN & SPLIT columns to create data relationships)
        recipient_df["org"] = recipient_df[["Organization", "City", "Address"]].agg(" - ".join, axis=1)
        orgs = recipient_df.org.unique()
        recipient = st.selectbox("Donation Recipient", options=orgs)
        recipient_name = recipient.split(" - ")[0]
        recipient_city = recipient.split(" - ")[1]
        recipient_account = recipient.split(" - ")[2]

        # Selectbox for Category
        category = st.selectbox("Donation Category", options=categories_df)

        # Selectbox for Resources - (JOIN & SPLIT columns to create data relationships)
        resources_df["USD"] = resources_df["USD"].astype(str)
        resources_df["item"] = resources_df[["Item", "QtySize", "USD"]].agg(" - ".join, axis=1)
        this_cat = resources_df[resources_df['Category'].str.contains(category)]
        items = this_cat.item.unique()
        resource = st.selectbox("Resource", options=items)

        # Value retrieved from resource selectbox and SPLIT to get the last value column `USD`
        resource_name = resource.split("-")[0]
        initial_appraisal_value = int(float(resource.split("-")[2]))

        # Value retrieved from resource selectbox
        city = st.text_input("City", recipient_city, type="default", help=None, disabled=True)

        # READ ALL THE BYTES of new image file template to upload to ipfs!
        image_file = open(Path(f"src/images/tokens/{category}.png"),"rb")

        if st.button("Donate"):
            # Timestamp when button is clicked (can't hurt right?)
            now = datetime.datetime.now()
            date_time = now.strftime("%Y/%m/%d %H:%M:%S")
            # Use function to call Pinata API to pin the resource to the public IPFS
            resource_ipfs_hash, resource_cid = pin_image(resource_name, image_file)

            # Set up the transaction and make the function call to the deployed contract
            resource_uri = f"ipfs://{resource_ipfs_hash}"
            tx_hash = contract.functions.safeMintResource(
                recipient_account,
                resource_uri,
                donor_account,
                category,
                city,
                resource_name,
                int(initial_appraisal_value)
            ).transact({'from': donor_account, 'gas': 1000000})
            # get the reciept, then display transaction data to user.
            receipt = w3.eth.waitForTransactionReceipt(tx_hash)
            st.markdown(f"#### Transaction has been successfully mined.")
            st.write(f"Timestamp: {date_time}")
            st.write(f"TX Hash: {tx_hash}")
            st.write(f"Pinata Links: [IPFS Metadata]({ipfs_uri}{resource_ipfs_hash}) [IPFS Image]({ipfs_uri}{resource_cid})")
            st.write(f"Resource CID: {resource_cid}")
            st.write(f"Recipient Account: {recipient_account}")
            st.write(f"Category: {category}")
            st.write(f"City: {city}")
            st.write(f"Resource: {resource_name}")
            st.write(f"Appraisal Value: {initial_appraisal_value}")
            st.image(f"{ipfs_uri}{resource_cid}")
            st.write("---")
            st.write(f"Transaction Recipt: ")
            st.write(dict(receipt))
            st.write("---")
            # TODO: sync with local database for reporting etc
            # create_transaction(recipient_name, tx_hashHex, date_time, recipient_account, ipfs_link, donor_account, category, city, resource_name, initial_appraisal_value)
 

    with col2:
        # Populate the top right column with selected organization's logo
        if recipient_name == "Action Against Hunger":
            logo = "src/images/logos/Action_Against_Hunger_logo.png"
        elif recipient_name == "Oxfam":
            logo = "src/images/logos/Oxfam_logo.png"
        elif recipient_name == "Care International":
            logo = "src/images/logos/care_international_logo.png"
        elif recipient_name == "World Food Program":
            logo = "src/images/logos/world_food_program_logo.png"
        elif recipient_name == "International Rescue Committee":
            logo = "src/images/logos/International_Rescue_Committee_Logo.png"
        elif recipient_name == "World Vision":
            logo = "src/images/logos/World_Vision_logo.png"
        elif recipient_name == "Unicef":
            logo = "src/images/logos/UNICEF_logo.png"
        elif recipient_name == "Direct Relief":
            logo = "src/images/logos/Direct_Relief_logo.webp"
        elif recipient_name == "Transaprent Hands":
            logo = "src/images/logos/transparent_hands_logo.webp"

        else:
            logo = "src/images/content/_na.png"

        st.image(logo, use_column_width=True)
        st.write("---")

        # Populate the right bottom column with an image of the item to be minted
        if category =="Water":
            cat = "src/images/tokens/water.png"
        elif category =="Food":
            cat = "src/images/tokens/food.png"
        elif category =="Clothing":
            cat = "src/images/tokens/clothing.png"
        elif category =="Shelter":
            cat = "src/images/tokens/shelter.png"
        elif category =="Education":
            cat = "src/images/tokens/education.png"
        elif category =="Health":
            cat = "src/images/tokens/health.png"
        else:
            cat = "src/images/content/_na.png"
      
        st.image(cat, use_column_width=True)



def load_data():
    # Populate a dataframe from SQL table to use on this page.
    query_str = "SELECT * FROM DONATIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
