// SPDX-License-Identifier: MIT

// Smart contract that lets anyone deposit ETH into the contract
// Only the owner of the contract can withdraw the ETH
pragma solidity ^0.6.0;

// Get the latest ETH/USD price from chainlink price feed
import '@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol';
import '@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol';

contract FundMe {
  // safe math library check uint256 for integer overflows
  using SafeMathChainlink for uint256;

  //mapping to store which address depositeded how much ETH
  mapping(address => uint256) public addressToAmountFunded;
  // array of addresses who deposited
  address[] public funders;
  //address of the owner (who deployed the contract)
  address public fundRaiser;
  uint256 public fundRaiseCreationTime;
  uint256 public lockPeriod;
  AggregatorV3Interface public priceFeed;

  constructor(address _priceFeed, uint256 _lockPeriod) public {
    priceFeed = AggregatorV3Interface(_priceFeed);
    // the first person to deploy the contract is the fundRaiser
    fundRaiser = msg.sender;
    fundRaiseCreationTime = now;
    lockPeriod = _lockPeriod;
  }

  function fund() public payable {
    // 18 digit number to be compared with donated amount
    uint256 minimumUSD = 20 * 10**18;
    //is the donated amount less than 20 USD?
    require(getConversionRate(msg.value) >= minimumUSD, 'Not enough eth');
    //if all good, add to mapping and funders array
    addressToAmountFunded[msg.sender] += msg.value;
    funders.push(msg.sender);
  }

  function getPrice() private view returns (uint256) {
    (, int256 answer, , , ) = priceFeed.latestRoundData();
    // ETH/USD rate in 18 digit
    return uint256(answer * 10000000000);
  }

  // 1000000000
  function getConversionRate(uint256 ethAmount) private view returns (uint256) {
    uint256 ethPrice = getPrice();
    uint256 ethAmountInUsd = (ethPrice * ethAmount) / 100000000;
    // the actual ETH/USD conversation rate, after adjusting the extra 0s.
    return ethAmountInUsd;
  }

  function getEntranceFee() public view returns (uint256) {
    // minimumUSD
    uint256 minimumUSD = 20 * 10**18;
    uint256 price = getPrice();
    uint256 precision = 1 * 10**18;
    return (minimumUSD * precision) / price;
  }

  modifier onlyOwner() {
    //is the message sender owner of the contract?
    require(msg.sender == fundRaiser);
    _;
  }

  // onlyOwner modifer will first check the condition inside it
  // and if true, withdraw function will be executed
  function withdraw() public payable onlyOwner {
    require(
      now - fundRaiseCreationTime > lockPeriod * 60,
      "You can't withdraw your funds yet !"
    );
    msg.sender.transfer(address(this).balance);

    //iterate through all the mappings and make them 0
    //since all the deposited amount has been withdrawn
    for (uint256 funderIndex = 0; funderIndex < funders.length; funderIndex++) {
      address funder = funders[funderIndex];
      addressToAmountFunded[funder] = 0;
    }
    //funders array will be initialized to 0
    funders = new address[](0);
  }
}
