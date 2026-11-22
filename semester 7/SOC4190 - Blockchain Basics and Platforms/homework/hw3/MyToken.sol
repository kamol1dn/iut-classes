// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts@5.6.1/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    constructor() ERC20("Yusupov Coin", "YUS") {
        _mint(msg.sender, 110123 * 10 ** 18);
    }
}
