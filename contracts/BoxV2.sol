//SPDX-License-Identifier: MIT

pragma solidity ^0.8.8;

contract Box {
    uint256 private value;

    event ValueChanged(uint256);

    function store(uint256 newValue) public {
        value = newValue;
        emit ValueChanged(newValue);
    }

    function retreive() public view returns (uint256) {
        return value;
    }

    function increment() public {
        value += value;
        emit ValueChanged(value);
    }
}
