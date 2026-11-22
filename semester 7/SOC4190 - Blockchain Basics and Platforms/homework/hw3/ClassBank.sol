// SPDX-License-Identifier: GPL-3.0
pragma solidity >=0.8.2 <0.9.0;

contract ClassBank {
    mapping(address => uint256) public balanceOf;

    function deposit() public payable {
        balanceOf[msg.sender] += msg.value;
    }

    function withdraw() public {
        uint256 amount = balanceOf[msg.sender];
        require(amount > 0, "ClassBank: nothing to withdraw");
        (bool ok, ) = msg.sender.call{value: amount}("");
        require(ok, "ClassBank: payment failed");
        balanceOf[msg.sender] = 0;
    }
}
