import logging
import streamlit as st
import streamlit.components.v1 as components
from src.utils.dataio import get_data
from src.utils.minter import *
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

recipient_df = get_data("SELECT recipient, address, balance from RECIPIENTS")

def main(df):
    #Header information 
    st.title("Donations", anchor=None)
    st.subheader("This page will connect to your Metamask wallet to allow fast transactions. Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.")
    st.caption("Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.", unsafe_allow_html=False)
    accounts = recipient_df["address"]
    recipient_account = st.selectbox("Select Recipient", options=accounts)
    st.write(f"Contract Address: {contract_address}")
 
    # with open(contract_abi) as f:
    #     this_abi = json.load(f)
    # st.write("ABI:")
    # st.write(this_abi)

    st.markdown("## Register New Resource")
    resource_name = st.text_input("Name")
    # donor_name = st.text_input("Donor")
    donor_account = os.getenv("PUBLIC_KEY")
    category = st.text_input("Category")
    # status = st.text_input("Status")
    lat_log = st.text_input("Coordinates (lat^long)")
    initial_appraisal_value = st.text_input("Value")
    file = st.file_uploader("Upload Image", type=["jpg", "jpeg", "png"])

    if st.button("Donate"):
        resource_ipfs_hash = pin_image(resource_name, file)
        resource_uri = f"ipfs://{resource_ipfs_hash}"
        # address,string,address,string,string,string,uint256
        tx_hash = contract.functions.safeMintResource(
            recipient_account,
            resource_uri,
            donor_account,
            category,
            lat_log,
            resource_name,
            int(initial_appraisal_value)
        ).transact({'from': donor_account, 'gas': 1000000})
        receipt = w3.eth.waitForTransactionReceipt(tx_hash)
        st.write("Transaction receipt mined:")
        st.write(dict(receipt))
        st.write("You can view the pinned metadata file with the following IPFS Gateway Link")
        st.markdown(f"[Artwork IPFS Gateway Link](https://gateway.pinata.cloud/ipfs/{resource_ipfs_hash})")

    # hvar = """
    #     <script>
    #         var elements = window.parent.document.querySelectorAll('.css-1q8dd3e')
    #         elements[0].innerText = 'reloaded';
    #         elements[0].disabled = true;
    #     </script>
    #     """
    # btn =  st.button("Mint")
    # if btn:
    #     minter(contract_address, contract_abi, recipient_account, token_metadata_url)
    #     components.html(hvar, height=0, width=0)

    # st.write(df)

def load_data():
    query_str = "SELECT * FROM DONATIONS;"
    df = get_data(query_str)
    return df

if __name__ == '__main__':
    logging.basicConfig(level=logging.CRITICAL)
    df = load_data()
    main(df)
