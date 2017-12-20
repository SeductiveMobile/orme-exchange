var PricingStrategy = artifacts.require("PricingStrategy");

contract('PricingStrategy', function (accounts) {
    it('should set 10000000 ORMEs available', function () {
        var contract = null;
        return PricingStrategy.deployed().then(function (instance) {
            contract = instance;
            return contract.setAvailableORMEInGwei(1000000000);
        }).then(function () {
            return contract.availableORMEInGwei.call();
        }).then(function (availableORMEInGwei) {
            assert.equal(availableORMEInGwei.toNumber(), 1000000000, "ORMEs amount wasn't correctly set.");
        });
    });

    it('should set 10 BTC (100,000,000 Satoshi) available', function () {
        var contract = null;
        return PricingStrategy.deployed().then(function (instance) {
            contract = instance;
            return contract.setAvailableSatoshi(100000000);
        }).then(function () {
            return contract.availableSatoshi.call();
        }).then(function (availableSatoshi) {
            assert.equal(availableSatoshi.toNumber(), 100000000, "BTC amount wasn't correctly set.");
        });
    });

    it('should calculate price for token correctly', function () {
        var contract = null;
        return PricingStrategy.deployed().then(function (instance) {
            contract = instance;
            return contract.setAvailableSatoshi(10000000000);
        }).then(function (instance) {
            return contract.setAvailableORMEInGwei(10000000000000000);
        }).then(function () {
            return contract.calculateSatoshiPrice.call(1000);
        }).then(function (value) {
            assert.equal(value.toNumber() , 1000000000, "Price calculated incorrectly");
        });
    });
});