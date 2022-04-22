//SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import {ERC721Enumerable, ERC721} from "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import {Strings} from "@openzeppelin/contracts/utils/Strings.sol";
import {UsingHexagons} from "./UsingHexagons.sol";

contract DemoNFT is ERC721Enumerable, UsingHexagons {
    using Strings for uint256;

    struct Info {
        uint256 hair;
    }

    mapping(uint256 => Info) public tokenInfo;
    string public baseUri;

    constructor() ERC721("Demo NFT", "DNFT") UsingHexagons() {}

    function tokenURI(uint256 _tokenId) public view override returns (string memory) {
        require(_exists(_tokenId), "DemoNFT: URI query for nonexistent token");

        Info storage info = tokenInfo[_tokenId];

        string memory baseURI = _baseURI();
        return bytes(baseURI).length > 0 ? string(abi.encodePacked(baseURI, _tokenId.toString(), "/", info.hair)) : "";
    }

    function mint() external {
        uint256 tokenId = totalSupply();
        tokenInfo[tokenId] = Info(0);
        _mint(msg.sender, tokenId);
    }

    function setBaseURI(string calldata _baseUri) external onlyOwner {
        baseUri = _baseUri;
    }

    function _baseURI() internal view override returns (string memory) {
        return baseUri;
    }

    function _onNotification(
        uint256 _protocolId,
        address _owner,
        bytes calldata _data
    ) internal override {}
}
