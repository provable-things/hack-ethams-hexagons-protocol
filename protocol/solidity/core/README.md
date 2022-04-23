# using-hexagons

&nbsp;

***

&nbsp;

## :rocket: How to use it?

```js
pragma solidity ^0.8.10;

import {UsingHexagons} from "@hexagons-protocol/UsingHexagons.sol";

contract YourContract is UsingHexagons {
    
    function _onHexagonsProtocolMessage(
        uint256 _protocolId,
        address _author,
        bytes calldata _data
    ) internal override {
        ...
    }
}
```