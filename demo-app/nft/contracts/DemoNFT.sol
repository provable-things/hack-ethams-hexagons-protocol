//SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721Enumerable.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./UsingHexagons.sol";

contract DemoNFT is ERC721Enumerable, Ownable, UsingHexagons {
    using Strings for uint256;

    struct Info {
        uint256 hair;
    }

    mapping(uint256 => Info) public tokenInfo;

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

    function _onNotification(
        uint256 _protocolId,
        address _owner,
        bytes calldata _data
    ) internal override {}
}
