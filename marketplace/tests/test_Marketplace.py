import pytest
from brownie import Wei, accounts, Marketplace
import os
from dotenv import load_dotenv

load_dotenv()

kWh_Contract_address = os.environ["kWh_Contract_address"]
Marketplace_Contract_address = os.environ["Marketplace_Contract_address"]
offer_num = 1

def test_create_offer():
    Price = int(1e16 * 1)
    offer = Marketplace.at(Marketplace_Contract_address).createOffer(
        kWh_Contract_address,1,Price,{"from":accounts[0]}
    )
    marketplace = Marketplace.at(Marketplace_Contract_address).offers(offer_num,{"from":accounts[1]})
    
    Amount_Energy = marketplace[1]
    Price_Unit = marketplace[2]
    Price = marketplace[3]
    for_Sale = marketplace[5]

    assert Price_Unit == 1e16
    assert Amount_Energy == 1
    assert Price == 1e16 * 1
    assert for_Sale == True



def test_change_Price_Unit_owner():
    Price = int(1e17 * 1)
    Price_Unit_before_change = Marketplace.at(Marketplace_Contract_address).offers(offer_num,{"from":accounts[0]})[2]
    change_Price = Marketplace.at(Marketplace_Contract_address).changePrice(offer_num,Price,{"from":accounts[0]})
    Price_Unit_after_change = Marketplace.at(Marketplace_Contract_address).offers(offer_num,{"from":accounts[0]})[2]
    
    assert Price_Unit_before_change != Price_Unit_after_change
    assert Price_Unit_before_change == 1e16
    assert Price_Unit_after_change == 1e17

def test_Buying():
    Seller_account_balance_before = accounts[0].balance()
    Buyer_account_balance_before = accounts[1].balance()
    Price = Marketplace.at(Marketplace_Contract_address).offers(offer_num,{"from":accounts[0]})[3]
    Price = int(1e17 * 1)
    Marketplace.at(Marketplace_Contract_address).buy(
        offer_num, kWh_Contract_address,{"from":accounts[1],
        "value": Price})

    for_Sale_after = Marketplace.at(Marketplace_Contract_address).offers(offer_num,{"from":accounts[0]})[5]  
    Seller_account_balance_after = accounts[0].balance()
    Buyer_account_balance_after = accounts[1].balance() 

    assert for_Sale_after == False
    assert Seller_account_balance_after == Seller_account_balance_before + Price
    assert Buyer_account_balance_after == Buyer_account_balance_before - Price


"""
def test_change_Price_Unit_not_owner():
    Price_before_change = Marketplace.at(Marketplace_Contract_address).offers(offer_num,{"from":accounts[0]})[2]
    marketplace = Marketplace.at(Marketplace_Contract_address).buy(offer_num,1,{"from":accounts[1]})
    Price_after_change = Marketplace.at(Marketplace_Contract_address).offers(offer_num,{"from":accounts[0]})[2]

    #assert marketplace.revert_msg == "You dind't create the offer"
"""