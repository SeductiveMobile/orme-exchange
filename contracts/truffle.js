//var Web3 = require('web3');
//var web3 = new Web3(new Web3.providers.HttpProvider('http://' + process.env.RPC_HOST + ':' + process.env.RPC_PORT));
//console.log('>> Unlocking account ');
//web3.personal.unlockAccount(process.env.DEPLOYER_ADDRESS, process.env.DEPLOYER_PASSPHRASE, 36000);

module.exports = {
  // See <http://truffleframework.com/docs/advanced/configuration>
  // to customize your Truffle configuration!
    networks: {
      development: {
        host: process.env.RPC_HOST || "localhost",
        port: process.env.RPC_PORT || 8545,
        network_id: "*",
        gas: 4612388,
        from: process.env.DEPLOYER_ADDRESS,
      }
  }
};