// SPDX-License-Identifier: MIT
pragma solidity ^0.8.4;

import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/token/ERC721/ERC721.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/security/Pausable.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/access/AccessControl.sol";
import "https://github.com/OpenZeppelin/openzeppelin-contracts/blob/release-v4.7/contracts/utils/Counters.sol";

/// @custom:security-contact test@stwtoken.com
contract SaveTheWorldToken is ERC721, ERC721Enumerable, ERC721URIStorage, Pausable, AccessControl {
    using Counters for Counters.Counter;

    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant DONOR_ROLE = keccak256("DONOR_ROLE");
    bytes32 public constant PROCUREMENT_ROLE = keccak256("PROCUREMENT_ROLE");
    bytes32 public constant RECIPIENT_ROLE = keccak256("RECIPIENT_ROLE");

    Counters.Counter private _tokenIdCounter;

    constructor() ERC721("SaveTheWorldToken", "STW") {

        address minter = 0xCC5AE77FD7EbF3E33Df715329F4e257F19d6dd31;        // Account 2
        address pauser = 0x5FEFb33E39b3f63069F84801099C6EA665a7C7e4;        // Account 3
        address donor = 0x3A8720196d80ffAD5D7223FE1C3f0Dda460Ee29D;         // Account 4
        address procurement = 0x7cba210574ae9057Ba06DF0988CDE6cB332AA515;   // Account 5
        address recipient = 0x5aCF3B73b99A5F503c68D8Fe795b8233B3CeD41a;     // Account 6

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(MINTER_ROLE, minter);
        _grantRole(PAUSER_ROLE, pauser);
        _grantRole(DONOR_ROLE, donor);
        _grantRole(PROCUREMENT_ROLE, procurement);
        _grantRole(RECIPIENT_ROLE, recipient);

    }

    struct Resource {
        address to;
        string name;
        address donor;
        string category;
        string status;
        string lat_long;
        uint256 appraisalValue;
    }

    mapping(uint256 => Resource) public resourceCollection;

    function _baseURI() internal pure override returns (string memory) {
        return "ipfs:/";
    }

    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    function _beforeTokenTransfer(address from, address to, uint256 tokenId)
        internal
        whenNotPaused
        override(ERC721, ERC721Enumerable)
    {
        super._beforeTokenTransfer(from, to, tokenId);
    }

    function safeMintResource(
        address to,
        string memory uri,
        address donor,
        string memory category,
        string memory status,
        string memory lat_long,
        uint256 initialAppraisalValue
    ) public onlyRole(MINTER_ROLE) returns (uint256) {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
        resourceCollection[tokenId] = Resource(to, uri, donor, category, status, lat_long, initialAppraisalValue);
        return tokenId;
    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }

    function supportsInterface(bytes4 interfaceId)
        public
        view
        override(ERC721, ERC721Enumerable, AccessControl)
        returns (bool)
    {
        return super.supportsInterface(interfaceId);
    }
}