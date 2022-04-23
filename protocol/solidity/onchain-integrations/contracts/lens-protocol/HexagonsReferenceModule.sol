//SPDX-License-Identifier: MIT
pragma solidity 0.8.10;

import {IReferenceModule} from "./IReferenceModule.sol";
import {ILensHub} from "./ILensHub.sol";
import {IUsingHexagons} from "../interfaces/IUsingHexagons.sol";
import {Constants} from "../libraries/Constants.sol";

contract HexagonsReferenceModule is IReferenceModule {
    address public token;
    address public hub;

    constructor(address _hub, address _token) {
        token = _token;
    }

    function initializeReferenceModule(
        uint256 profileId,
        uint256 pubId,
        bytes calldata data
    ) external pure override returns (bytes memory) {
        return new bytes(0);
    }

    function processComment(
        uint256 profileId,
        uint256 profileIdPointed,
        uint256 pubIdPointed,
        bytes calldata data
    ) external override {
        address owner = ILensHub(hub).getDispatcher(profileId);
        IUsingHexagons(token).sendHexagonsProtocolMessage(
            Constants.PROTOCOL_LENS,
            keccak256(abi.encode(profileId, profileIdPointed, pubIdPointed)),
            owner,
            data,
            ""
        );
    }

    function processMirror(
        uint256 profileId,
        uint256 profileIdPointed,
        uint256 pubIdPointed,
        bytes calldata data
    ) external view override {}
}
