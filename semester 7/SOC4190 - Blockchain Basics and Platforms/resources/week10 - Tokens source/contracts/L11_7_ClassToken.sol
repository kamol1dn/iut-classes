// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts@5.6.1/token/ERC20/ERC20.sol";

contract ClassToken is ERC20 {
    constructor() ERC20("ClassToken", "CLS") {
        _mint(msg.sender, 1000 * 10 ** 18);
    }
}
