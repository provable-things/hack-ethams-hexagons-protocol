# demo-nft

&nbsp;

***

&nbsp;

## :guardsman: Smart Contract Tests

```
❍ npm install
```

```
❍ npm run test
```


&nbsp;

***

&nbsp;

## :white_check_mark: How to publish & verify

Create an __.env__ file with the following fields:

```
ETH_MAINNET_NODE=
ETHERSCAN_API_KEY=
ETH_MAINNET_PRIVATE_KEY=
```


### publish


```
❍ npx hardhat run --network eth scripts/deploy-script.js
```

### verify

```
❍ npx hardhat verify --network eth DEPLOYED_CONTRACT_ADDRESS "Constructor argument 1"
```