# save_the_world

Motive:

Currently, charitable foundations spend about 30% of donations in administrative expenses. Such event depletes the amount of resources delivered to people in need. Reducing the involvement of intermediary institutions will inevitably translate into more help for the intended recipients. 
Traditional charity systems have an intrinsic lack of transparency. Donors have no way to track or ensure assistance is getting to the right place. This has generated a high degree of mistrust towards charitable foundations. This could be improved by providing users with efficient ways to track donations and moreover, make each transaction distinguishable from the others. Such improvement would help restoring donor confidence and consequently, increase overall donations.

Saving the world solves both mentioned problems in traditional charity systems (admin costs and transparency). It provides an efficient blockchain system which processes and records transactions directly from donor to supplier. This last delivers resources directly to the end recipient without the need of intermediaries. In addition, each donation is completely trackable and stored as a non-fungible token.


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
