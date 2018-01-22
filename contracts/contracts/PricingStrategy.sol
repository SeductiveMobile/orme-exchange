pragma solidity ^0.4.0;

import "zeppelin/contracts/math/SafeMath.sol";
import "zeppelin/contracts/ownership/Ownable.sol";
import './FormulaInterface.sol';

contract PricingStrategy is Ownable {

    FormulaInterface public formula;

    using SafeMath for uint;

    uint256 public availableSatoshi;
    uint256 public availableORMEInGwei;
    uint32 public connectorWeight;

    address public tokenAddress;

    function PricingStrategy(FormulaInterface _formula) {
        formula = _formula;
    }

    function calculateORMEsForConnectors(uint256 _depositAmount) public constant returns (uint256) {
        return formula.calculatePurchase(availableORMEInGwei, availableSatoshi, connectorWeight, _depositAmount);
    }

    function calculateConnectorsForORMEIs(uint256 _sellAmount) public constant returns (uint256) {
        return formula.calculateSale(availableORMEInGwei, availableSatoshi, connectorWeight, _sellAmount);
    }

    function setAvailableSatoshi(uint256 _availableSatoshi) external onlyOwner {
        availableSatoshi = _availableSatoshi;
    }

    function setAvailableORMEInGwei(uint256 _availableORMEInGwei)  external onlyOwner {
        availableORMEInGwei = _availableORMEInGwei;
    }

    function setConnectorWeight(uint32 _connectorWeight)  external onlyOwner {
        connectorWeight = _connectorWeight;
    }
}

