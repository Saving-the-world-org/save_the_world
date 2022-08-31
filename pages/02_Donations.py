import logging
import streamlit as st
import streamlit.components.v1 as components
from src.utils.dataio import get_data
from src.utils.minter_ho import *
from src.utils.pinata import pin_file_to_ipfs, pin_json_to_ipfs, convert_data_to_json, pin_image
from web3 import Web3

from dotenv import load_dotenv
load_dotenv()

contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
contract_abi = os.getenv("ABI_PATH")
ipfs_uri = os.getenv("IPFS_URI")

# Define web3 and load contract
w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))

# Begin Streamlit calls
st.set_page_config(layout="wide")

@st.cache(allow_output_mutation=True)
def load_contract():
    with open(contract_abi) as f:
        this_abi = json.load(f)
    contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
    contract = w3.eth.contract(
        address=contract_address,
        abi=this_abi
    )
    return contract

contract = load_contract()

recipient_df = get_data("SELECT Organization, City, Address from ORGANIZATIONS")
categories_df = get_data("SELECT DISTINCT Category from DONATIONS")
resources_df = get_data("SELECT Category, Item, QtySize, USD, Tags from DONATIONS")

def main(df):
    #Header information 
    st.title("Donations", anchor=None)
    st.subheader("This page will connect to your Metamask wallet to allow fast transactions. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    st.caption("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", unsafe_allow_html=False)
    donor_account = os.getenv("PUBLIC_KEY")
    st.write(f"Donor account: {donor_account}")

    # Selectbox for recipient Org-City-Address
    recipient_df["org"] = recipient_df[["Organization", "City", "Address"]].agg(" - ".join, axis=1)
    orgs = recipient_df.org.unique()
    recipient = st.selectbox("Donation Recipient", options=orgs)
    recipient_name = recipient.split(" - ")[0]
    recipient_city = recipient.split(" - ")[1]
    recipient_account = recipient.split(" - ")[2]
    # st.write(f"Name: ", recipient_name)
    # st.write(f"City: ", recipient_city)
    # st.write(f"Account: ", recipient_account)

    # Selectbox for Category
    category = st.selectbox("Donation Category", options=categories_df)
    # st.write(f"Selected Donation Category: ", category)

    # Selectbox for Resource
    resources_df["USD"] = resources_df["USD"].astype(str)
    # Concatenate columns for select box
    resources_df["item"] = resources_df[["Item", "QtySize", "USD"]].agg(" - ".join, axis=1)
    # Restrict to items within selected category
    this_cat = resources_df[resources_df['Category'].str.contains(category)]
    items = this_cat.item.unique()
    resource = st.selectbox("Resource", options=items)
    # st.write(f"Selected Resource:", resource)

    # Value retrieved from resource selectbox
    resource_name = resource.split("-")[0]
    initial_appraisal_value = int(float(resource.split("-")[2]))
    # initial_appraisal_value = st.text_input("Value (USD)", appraised_value, type="default", help=None, disabled=True)

    # Value retrieved from resource selectbox
    lat_long = st.text_input("City", recipient_city, type="default", help=None, disabled=True)

    # Prepopulated and disabled user input
    st.text_input("Status", value="Pre-Mint", type="default", help=None, disabled=True)

    # NOTE: Do we want to pass on enabling image minting too? I think that's a different use
    #       casefrom what we're doing.
    file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if st.button("Donate"): 
        resource_ipfs_hash = pin_image(resource_name, file)
        resource_uri = f"ipfs://{resource_ipfs_hash}"
        tx_hash = contract.functions.safeMintResource(
            recipient_account,
            resource_uri,
            donor_account,
            category,
            lat_long,
            resource_name,
            int(initial_appraisal_value)
        ).transact({'from': donor_account, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[Artwork IPFS Gateway Link]({ipfs_uri}{resource_ipfs_hash})")
        """
        TODO: Add logging and local data storgae here. Then move code into an external function.
        """
        # query = """INSERT INTO TRANSACTIONS VALUES(
        #     Organization,
        #     TransactionHash,
        #     TimeStamp,
        #     recipient_account,
        #     resource_uri,
        #     donor_account,
        #     category,
        #     lat_long,
        #     resource_name,
        #     int(initial_appraisal_value);
        #     """
        # save_transaction(query)

def load_data():
    query_str = "SELECT * FROM DONATIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
