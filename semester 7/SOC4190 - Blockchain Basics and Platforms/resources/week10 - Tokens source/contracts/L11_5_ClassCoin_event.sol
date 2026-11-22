// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract ClassCoin {
    mapping(address => uint256) public balanceOf;

    event Transfer(address indexed from,
                   address indexed to, uint256 amount);

    constructor() {
        balanceOf[msg.sender] = 1000;
    }

    function transfer(address to, uint256 amount) public {
        require(balanceOf[msg.sender] >= amount,
                "ClassCoin: not enough coins");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
    }
}
