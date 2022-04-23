//SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IDemoNFT {
    function tokenURI(uint256 _tokenId) external view returns (string memory);

    function mint() external;

    function setBaseURI(string calldata _baseUri) external;

    function sendHexagonsProtocolMessage(
        uint256 _protocolId,
        uint256 _id,
        address _author,
        bytes calldata _data,
        bytes calldata _proof
    ) external;
}
