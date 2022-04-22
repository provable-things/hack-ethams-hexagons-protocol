const { ethers } = require('hardhat')

const main = async () => {
  const DemoNFT = await ethers.getContractFactory('DemoNFT')

  console.info('Deploying DemoNFT...')
  const demoNFT = await DemoNFT.deploy()

  console.info('DemoNFT deployed to:', demoNFT.address)
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error)
    process.exit(1)
  })
