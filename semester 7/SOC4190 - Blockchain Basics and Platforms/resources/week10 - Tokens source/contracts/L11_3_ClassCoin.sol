// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract ClassCoin {
    mapping(address => uint256) public balanceOf;

    constructor() {
        balanceOf[msg.sender] = 1000;
    }

    function transfer(address to, uint256 amount) public {
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
    }
}
