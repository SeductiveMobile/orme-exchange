module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
    networks: {
      development: {
        host: process.env.ETHEREUM_RPC_HOST || "localhost",
        port: process.env.ETHEREUM_RPC_PORT || 8545,
        network_id: "*",
        gas: 4029024,
        from: process.env.ETHEREUM_DEPLOYER_ADDRESS,
      },
      testrpc: {
        host: process.env.ETHEREUM_RPC_HOST || "localhost",
        port: process.env.ETHEREUM_RPC_PORT || 8545,
        network_id: "*",
        gas: 4029024,
        from: process.env.ETHEREUM_DEPLOYER_ADDRESS,
      }
    },
    solc: {
        optimizer: {
            enabled: true,
            runs: 200
        }
    },
    rpc: {
      host: "localhost",
      port: 8545
    }
};