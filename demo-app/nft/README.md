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
POLYGON_MAINNET_NODE=
POLYGONSCAN_API_KEY=
POLYGON_MAINNET_PRIVATE_KEY=
```


### publish


```
❍ npx hardhat run --network polygon scripts/deploy-script.js
```

### verify

```
❍ npx hardhat verify --network polygon DEPLOYED_CONTRACT_ADDRESS "Constructor argument 1"
```