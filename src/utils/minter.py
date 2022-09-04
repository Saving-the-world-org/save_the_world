# -*- coding: utf-8 -*-
import os
import json
import logging
from pathlib import Path
from typing import Dict, Any
from web3 import Web3
from dotenv import load_dotenv
load_dotenv()

contract_address = os.getenv("SMART_CONTRACT_ADDRESS")
contract_abi = os.getenv("ABI_PATH")
ipfs_uri = os.getenv("IPFS_URI")


def load_json(path_to_json: str) -> Dict[str, Any]:
    """
    Purpose:
        Load json files
    Args:
        path_to_json (String): Path to  json file
    Returns:
        Conf: JSON file if loaded, else None
    """
    try:
        with open(path_to_json, "r") as config_file:
            conf = json.load(config_file)
            return conf

    except Exception as error:
        logging.error(error)
        raise TypeError("Invalid JSON file")

def set_up_blockchain(contract: str, abi_path: str):
    """
    Purpose:
       Setup all blockchain environment variables
    Args:
        contract address (String): The deployed smart contract address
        path_to_json (String): Path to the ABI json file
    Returns:
        JSON Config: JSON file if loaded, else None
    """
    ############ Ethereum Setup ############
    PUBLIC_KEY = os.getenv("PUBLIC_KEY")
    PRIVATE_KEY = Web3.toBytes(hexstr=os.getenv("PRIVATE_KEY"))
    INFURA_KEY = os.getenv("INFURA_KEY")
    network = os.getenv("NETWORK")
    ABI = None
    CODE_NFT = None
    CHAIN_ID = None
    w3 = None
    open_sea_url = ""
    scan_url = ""
    eth_json = {}

    if network == "rinkeby":
        RINK_API_URL = f"https://rinkeby.infura.io/v3/{INFURA_KEY}"
        w3 = Web3(Web3.HTTPProvider(RINK_API_URL))
        ABI = load_json(abi_path)["abi"]  # get the ABI
        CODE_NFT = w3.eth.contract(address=contract, abi=ABI)  # The contract
        CHAIN_ID = 4
        open_sea_url = f"https://testnets.opensea.io/assets/{contract}/"
        scan_url = "https://rinkeby.etherscan.io/tx/"

    elif network == "mumbai":
        MUMBAI_API_URL = f"https://polygon-mumbai.infura.io/v3/{INFURA_KEY}"
        w3 = Web3(Web3.HTTPProvider(MUMBAI_API_URL))
        ABI = load_json(abi_path)["abi"]  # get the ABI
        CODE_NFT = w3.eth.contract(address=contract, abi=ABI)  # The contract
        CHAIN_ID = 80001
        open_sea_url = f"https://testnets.opensea.io/assets/{contract}/"
        scan_url = "https://explorer-mumbai.maticvigil.com/tx/"

    elif network == "matic_main":
        POLYGON_API_URL = f"https://polygon-mainnet.infura.io/v3/{INFURA_KEY}"
        w3 = Web3(Web3.HTTPProvider(POLYGON_API_URL))
        ABI = load_json(abi_path)["abi"]  # get the ABI
        CODE_NFT = w3.eth.contract(address=contract, abi=ABI)  # The contract
        CHAIN_ID = 137
        open_sea_url = f"https://opensea.io/assets/matic/{contract}/"
        scan_url = "https://polygonscan.com/tx/"

    elif network == "development":
        w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER_URI")))
        with open(Path('./contracts/compiled/save_the_world_abi.json')) as f:
            ABI = json.load(f)
        CODE_NFT = w3.eth.contract(address=contract, abi=ABI)  # The contract
        CHAIN_ID = 5777
        open_sea_url = f"https://opensea.io/assets/matic/{contract}/"
        scan_url = "https://polygonscan.com/tx/"

    else:
        logging.error("Invalid network")
        raise ValueError(f"Invalid {network}")

    logging.info(f"checking if connected w3...{w3.isConnected()}")

    eth_json["w3"] = w3
    eth_json["contract"] = CODE_NFT
    eth_json["chain_id"] = CHAIN_ID
    eth_json["open_sea_url"] = open_sea_url
    eth_json["scan_url"] = scan_url
    eth_json["public_key"] = PUBLIC_KEY
    eth_json["private_key"] = PRIVATE_KEY

    return eth_json
