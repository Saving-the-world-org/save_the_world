# save_the_world

## Requirements

- Streamlit
- Python
- Truffle Suite (Ganache)
- Web3 (Solidity)

## Quickstart

Change PROJECT23.env to .env and fill any required values to get started:

    ``` (.env file)
    ...
    SMART_CONTRACT_ADDRESS="<YOUR_SMART_CONTRACT_ADDRESS>"
    PINATA_API_KEY="<YOUR_PINATA_API_KEY>"
    PINATA_SECRET_API_KEY="<YOUR_PINATA_SECRET_API_KEY>"
    NETWORK="development"
    WEB3_PROVIDER_URI="http://127.0.0.1:7545"
    ...

    ```

### STW Token Storage

The minted tokens are stored in the pinata.cloud ipfs platform.

Here are the URLs which were used to store the token and image metadata on pinata.cloud:
- https://gateway.pinata.cloud/ipfs/QmT3dxsNK2wmNb1KRUtZMxr456VFzLE36RivdhYG9nVb3Z

- https://gateway.pinata.cloud/ipfs/bafkreictziodueto6xhrmvtjkdwvnuyrn3yqg5zu5bzwixfufrfmyomaeq
      

``` (transaction packet)
{"name":"Relief Package ","image":"QmT3dxsNK2wmNb1KRUtZMxr456VFzLE36RivdhYG9nVb3Z"}
```
---
