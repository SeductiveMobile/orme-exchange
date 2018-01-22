var PricingStrategy = artifacts.require("./PricingStrategy.sol");
var Formula = artifacts.require('Formula.sol');

module.exports = function(deployer) {
  deployer.deploy(Formula)
      .then(function() {
  return deployer.deploy(PricingStrategy, Formula.address);
  });
};

