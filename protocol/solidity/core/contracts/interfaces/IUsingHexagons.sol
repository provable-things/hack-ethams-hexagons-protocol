//SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

interface IUsingHexagons {
    function addLensProtocolModule(address _lensProtocolModule) external;

    function sendHexagonsProtocolMessage(
        uint256 _protocolId,
        bytes32 _queryId,
        address _author,
        bytes calldata _data,
        bytes calldata _proof
    ) external;
}
