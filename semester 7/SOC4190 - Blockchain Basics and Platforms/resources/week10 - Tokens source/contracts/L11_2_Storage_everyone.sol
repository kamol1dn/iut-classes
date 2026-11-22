// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract Storage {
    mapping(address => uint256) public numberOf;

    function store(uint256 num) public {
        numberOf[msg.sender] = num;
    }

    function retrieve() public view returns (uint256) {
        return numberOf[msg.sender];
    }
}
