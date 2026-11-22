// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract Storage {
    uint256 number;
    address public lastWriter;

    function store(uint256 num) public {
        number = num;
        lastWriter = msg.sender;
    }

    function retrieve() public view returns (uint256) {
        return number;
    }
}
