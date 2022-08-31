# -*- coding: utf-8 -*-
import os
import json
import requests
from dotenv import load_dotenv
from os import walk, path, sep
from requests import Session, Request

load_dotenv()

json_headers = {
    "Content-Type": "application/json",
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

file_headers = {
    "pinata_api_key": os.getenv("PINATA_API_KEY"),
    "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
}

def convert_data_to_json(content):
    data = {"pinataOptions": {"cidVersion": 1}, "pinataContent": content}
    return json.dumps(data)

def pin_file_to_ipfs(data):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinFileToIPFS",
        files={'file': data},
        headers=file_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_json_to_ipfs(json):
    r = requests.post(
        "https://api.pinata.cloud/pinning/pinJSONToIPFS",
        data=json,
        headers=json_headers
    )
    print(r.json())
    ipfs_hash = r.json()["IpfsHash"]
    return ipfs_hash

def pin_image(artwork_name, artwork_file):
    # Pin the file to IPFS with Pinata
    ipfs_file_hash = pin_file_to_ipfs(artwork_file) #.getvalue())

    # Build a token metadata file for the artwork
    token_json = {
        "name": artwork_name,
        "image": ipfs_file_hash
    }
    json_data = convert_data_to_json(token_json)

    # Pin the json to IPFS with Pinata
    json_ipfs_hash = pin_json_to_ipfs(json_data)

    return json_ipfs_hash, ipfs_file_hash


def pin_appraisal_report(report_content):
    json_report = convert_data_to_json(report_content)
    report_ipfs_hash = pin_json_to_ipfs(json_report)
    return report_ipfs_hash
    

# with this code i solved the problem. To understand the problem it was enough to upload directly from pinata and see what kind of call the browser was making.
# It could be seen how the request payload was different:
# The metadata was missing, in which the directory name must be contained
# For each file it is necessary to define the filename in the directory / filename format but the default request library sets the filename with only the file name, if you print the body you can notice this thing
# The code:

# from os import walk, path, sep
# from requests import Session, Request

def pinata_upload(image_file):
    # directory is the abs path of dir
    # files = []
    ipfs_url = "https://api.pinata.cloud/pinning/pinFileToIPFS"
    headers = {
        # 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36',
        "pinata_api_key": os.getenv("PINATA_API_KEY"),
        "pinata_secret_api_key": os.getenv("PINATA_SECRET_API_KEY"),
    }
    # directory.split(sep)[-1] is the name of directory
    # files.append(('pinataMetadata', (None, '{"name":"' + directory.split(sep)[-1] + '"}')))
    # for root, dirs, files_ in walk(path.abspath(directory)):
    #     for f in files_:
    #         complete_path = path.join(root, f)
    #         # sep.join(complete_path.split(sep)[-2:]) create the name of file with the syntax directory/filename
    #         files.append(('file', (sep.join(complete_path.split(sep)[-2:]), open(complete_path, 'rb'))))
    file = open(image_file, 'rb')
    request = Request(
        'POST',
        ipfs_url,
        headers=headers,
        files=file
    ).prepare()
    response = Session().send(request)
    print(response.request.url)
    print(response.request.headers)
    print(response.request.body)
    print(response.json())

    return resource_ipfs_hash, resource_cid

