// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract ClassBankFixed {
    mapping(address => uint256) public balanceOf;

    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 amount = balanceOf[msg.sender];
        require(amount > 0, "ClassBank: nothing to withdraw");
        balanceOf[msg.sender] = 0;
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "ClassBank: payment failed");
    }
}
