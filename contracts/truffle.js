module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
    networks: {
    development: {
      host: process.env.RPC_HOST || "localhost",
      port: 8545,
      network_id: "*"
    }
  }
};
