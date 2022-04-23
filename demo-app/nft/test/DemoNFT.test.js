const { use, expect } = require('chai')
const { ethers, upgrades } = require('hardhat')
const { solidity } = require('ethereum-waffle')
const BigNumber = require('bignumber.js')
use(solidity)

const BASE_URI = 'https://base.uri/'
let demoNFT, owner, PRICE

describe('DemoNFT', function () {
  beforeEach(async () => {
    const DemoNFT = await ethers.getContractFactory('DemoNFT')

    const accounts = await ethers.getSigners()
    owner = accounts[0]

    demoNFT = await DemoNFT.deploy()
  })

  it('should be able to set the base uri', async () => {
    await demoNFT.setBaseURI(BASE_URI)
    expect(await demoNFT.baseURI()).to.be.equal(BASE_URI)
  })

  it('should be able to mint one token', async () => {
    await demoNFT.mint()
    expect(await demoNFT.ownerOf(0)).to.be.equal(owner.address)
    await demoNFT.mint()
    expect(await demoNFT.ownerOf(1)).to.be.equal(owner.address)
  })

  it('should be able to set the hairs', async () => {
    await demoNFT.mint()
    await demoNFT.setHairFor('brown', 0)
    const [hair] = await demoNFT.getInfoOf(0)
    expect(hair).to.be.equal('brown')
  })
})
