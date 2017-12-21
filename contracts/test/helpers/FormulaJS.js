

function calculateSmartTokensForConnectors(supply, balance, weight, amount) {
    return supply*(Math.pow((1+amount/balance),(weight/1000000))-1);
}

function calculateConnectorsForSmartTokens(supply, balance, weight, amount) {
    return balance*(1-Math.pow((1-amount/supply),(1000000/weight)));
}

module.exports = {
    calculateSmartTokensForConnectors: calculateSmartTokensForConnectors,
    calculateConnectorsForSmartTokens: calculateConnectorsForSmartTokens
};