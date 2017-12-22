module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
    networks: {
      development: {
        host: process.env.RPC_HOST || "localhost",
        port: process.env.RPC_PORT || 8545,
        network_id: "*",
        gas: 4612388,
        from: process.env.DEPLOYER_ADDRESS
      }
  }
};