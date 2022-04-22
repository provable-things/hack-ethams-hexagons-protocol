//SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

import "@openzeppelin/contracts/access/Ownable.sol";

contract UsingHexagons is Ownable {
    uint256 public constant ID_LENS = 0;
    uint256 public constant ID_TWITTER = 1;

    address public lensProtocolModule;
    mapping (bytes32 => bool) private processedNotificationIds;

    constructor() {}

    function setLensProtocolModule(address _lensProtocolModule) external onlyOwner {
        lensProtocolModule = _lensProtocolModule;
    }

    function notify(
        uint256 _protocolId,
        uint256 _id,
        address _owner,
        bytes calldata _data,
        bytes calldata _proof
    ) public {
        bytes32 notificationId = keccak256(abi.encode(_protocolId, _id));
        require(processedNotificationIds[notificationId] == false, "Request already processed");
        require(_verify(_protocolId, _proof), "Invalid proof");
        _onNotification(_protocolId, _owner, _data);
        processedNotificationIds[notificationId] = true;
    }

    function _onNotification(
        uint256 _protocolId,
        address _owner,
        bytes calldata _data
    ) internal virtual {}

    function _verify(uint256 _protocolId, bytes calldata _proof) private view returns (bool) {
        if (_protocolId == ID_LENS) {
            return msg.sender == lensProtocolModule;
        }
        return true;
    }
}
