// SPDX-License-Identifier: GPL-3.0

pragma solidity ^0.8.3;

contract sivacoin_ico{
    
    //  max Sivacoins available for sales
    uint public max_sivacoins = 1000000;
    
    // INR to Sivacoins conversion rate 
    uint public inr_to_sivacoins = 1000;
    
    // total Sivacoins bought by investors
    uint public total_sivavoins_bought = 0;
    
    // mapping from investors address to its equity in Sivacoins and INR
    mapping(address => uint) equity_sivacoins;
    mapping(address => uint) equity_inr;
    
    // checking if an investor can buy Sivacoins
    modifier can_buy_sivacoins(uint inr_invested) {
        require (inr_invested * inr_to_sivacoins + total_sivavoins_bought <= max_sivacoins);
        _;
    }
    
    // getting the equity in Sivacoins of an investor
    function equity_in_sivacoins(address investor) external view returns (uint) {
        return equity_sivacoins[investor];
    }
    
     function equity_in_inr(address investor) external view returns (uint) {
        return equity_inr[investor];
    }
    
    // buying Sivacoins
    function buy_sivacoins(address investor, uint inr_invested) external can_buy_sivacoins(inr_invested) {
        uint sivacoins_bought = inr_invested * inr_to_sivacoins;
        equity_sivacoins[investor] += sivacoins_bought;
        equity_inr[investor] = equity_sivacoins[investor] / inr_to_sivacoins;
        total_sivavoins_bought += sivacoins_bought;
    }
    
    // sell Sivacoins 
    function sell_sivacoins(address investor, uint sivacoins_sold) external  {
        equity_sivacoins[investor] -= sivacoins_sold;
        equity_inr[investor] = equity_sivacoins[investor] / inr_to_sivacoins;
        total_sivavoins_bought -= sivacoins_sold;
    }
    
}

