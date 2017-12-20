pragma solidity ^0.4.0;

import "zeppelin/contracts/math/SafeMath.sol";
import "zeppelin/contracts/ownership/Ownable.sol";

contract PricingStrategy is Ownable {

    using SafeMath for uint;

    uint256 public availableSatoshi;
    uint256 public availableORMEInGwei;

    address public tokenAddress;

    function PricingStrategy() { }

    function calculateTokensPrice(uint256 _tokens) public constant returns (uint256) {
        uint256 ratio = calculateRatio();
        return _tokens.div(ratio);
    }

    function calculateSatoshiPrice(uint256 _satoshi) public constant returns (uint256) {
        uint256 ratio = calculateRatio();
        return _satoshi.mul(ratio);
    }

    function calculateRatio() internal constant returns (uint256) {
        return availableORMEInGwei.div(availableSatoshi);
    }

    function setAvailableSatoshi(uint256 _availableSatoshi) external onlyOwner {
        availableSatoshi = _availableSatoshi;
    }

    function setAvailableORMEInGwei(uint256 _availableORMEInGwei)  external onlyOwner {
        availableORMEInGwei = _availableORMEInGwei;
    }
}

