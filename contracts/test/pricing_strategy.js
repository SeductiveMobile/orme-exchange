var Formula = artifacts.require('Formula.sol');
var PricingStrategy = artifacts.require("PricingStrategy");
const FormulaJS = require('./helpers/FormulaJS');

// TODO: Change MAX_ACCURACY to calculated gas
const MAX_ACCURACY = 1;

function outOfBoundsError(formulaValue, leftSide, rightSide) {
    return new Error(
        'Value ' + formulaValue +
        ' is out of bounds (' + (leftSide) +
        ' : ' + (rightSide) + ')');
}

function isInBounds(formulaValue, controlValue) {
    var leftSide = Math.max(controlValue - MAX_ACCURACY, 0);
    var rightSide = controlValue + MAX_ACCURACY;

    var inBounds = formulaValue >= leftSide && formulaValue <= rightSide;
    if (!inBounds) {
        return outOfBoundsError(formulaValue, leftSide, rightSide);
    }
}

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

    it('should set Weight to 100000', function () {
        var contract = null;
        return PricingStrategy.deployed().then(function (instance) {
            contract = instance;
            return contract.setConnectorWeight(100000);
        }).then(function () {
            return contract.connectorWeight.call();
        }).then(function (availableSatoshi) {
            assert.equal(availableSatoshi.toNumber(), 100000, "Weight wasn't correctly set.");
        });
    });


    it('should calculate quantity of satoshi for token correctly for any sell amount', function () {

        var size = 10;
        var bgn = 0;
        var end = 1000000;
        var gap = (end-bgn) / size

        // Weight is 100%
        var weight = 1000000;

        for (var n = 0; n <= size; n++) {
            var sellAmount = bgn + gap * n;
            var supply = 100000000000000;
            var balance = 10000000000;

            testSatoshiPrice(supply, balance, weight, sellAmount);
        }

    });

    it('should calculate quantity of satoshi for token correctly for weight from 100% to 10%', function () {
        var size = 10;

        // Max weight gap is 100%
        var maxWeight = 10000000;

        // Weight gap is 10%
        var gap = maxWeight / size;

        var sellAmount = 1000;
        var supply = 10000000000000000;
        var balance = 10000000000;

        for (var n = 0; n < size; n++) {
            var weight = maxWeight - gap * n;
            testSatoshiPrice(supply, balance, weight, sellAmount);
        }
    });

    function testSatoshiPrice(supply, balance, weight, amount) {
        var contract = null;
        return PricingStrategy.deployed().then(function (instance) {
            contract = instance;
            return contract.setAvailableSatoshi(balance);
        }).then(function (instance) {
            return contract.setAvailableORMEInGwei(supply);
        }).then(function (instance) {
            return contract.setConnectorWeight(weight);
        }).then(function () {
            return contract.calculateConnectorsForORMEIs(amount);
        }).then(function (value) {
            var formulaValueNumber = value.toNumber();
            var controlValue = FormulaJS.calculateConnectorsForSmartTokens(supply, balance, weight, amount);

            assert.ifError(isInBounds(formulaValueNumber, controlValue));

        });
    }

    it('should calculate quantity of token correctly for any deposit amount', function () {

        var size = 10;
        var bgn = 0;
        var end = 1000000;
        var gap = (end-bgn) / size

        // Weight is 100%
        var weight = 1000000;

        for (var n = 0; n <= size; n++) {
            var depositAmount = bgn + gap * n;
            var supply = 100000000000000;
            var balance = 10000000000;

            testTockenPrice(supply, balance, weight, depositAmount);
        }
    });

    it('should calculate quantity of token correctly for weight from 100% to 10%', function () {
        var size = 10;

        // Max weight gap is 100%
        var maxWeight = 10000000;

        // Weight gap is 10%
        var gap = maxWeight / size;

        var depositAmount = 1000;
        var supply = 10000000000000000;
        var balance = 10000000000;

        for (var n = 0; n < size; n++) {
            var weight = maxWeight - gap * n;
            testTockenPrice(supply, balance, weight, depositAmount);
        }
    });

    function testTockenPrice(supply, balance, weight, amount) {
        var contract = null;
        return PricingStrategy.deployed().then(function (instance) {
            contract = instance;
            return contract.setAvailableSatoshi(balance);
        }).then(function (instance) {
            return contract.setAvailableORMEInGwei(supply);
        }).then(function (instance) {
            return contract.setConnectorWeight(weight);
        }).then(function () {
            return contract.calculateORMEsForConnectors(amount);
        }).then(function (value) {
            var formulaValueNumber = value.toNumber();
            var controlValue = FormulaJS.calculateSmartTokensForConnectors(supply, balance, weight, amount);

            assert.ifError(isInBounds(formulaValueNumber, controlValue));

        });
    }
});