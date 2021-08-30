import time
import os
from dotenv import load_dotenv
from brownie import kWhToken, accounts


load_dotenv()
KWH_ADRESS = os.environ["kWh_Contract_address"]
MARKETPLACE_ADDRESS = os.environ["Marketplace_Contract_address"]
print(KWH_ADRESS)

def mint():
    kWhToken.at(KWH_ADRESS).mint(os.environ["Address_1"],500,{"from":accounts[9]})
    kWhToken.at(KWH_ADRESS).mint(os.environ["Address_2"],500,{"from":accounts[9]})
    kWhToken.at(KWH_ADRESS).mint(os.environ["Address_3"],500,{"from":accounts[9]})
    kWhToken.at(KWH_ADRESS).mint(os.environ["Address_4"],500,{"from":accounts[9]})

    
def check_Balances():
    bal_1 = kWhToken.at(KWH_ADRESS).balances(os.environ["Address_1"],{"from":accounts[0]})
    bal_2 = kWhToken.at(KWH_ADRESS).balances(os.environ["Address_2"],{"from":accounts[1]})
    bal_3 = kWhToken.at(KWH_ADRESS).balances(os.environ["Address_3"],{"from":accounts[2]})
    bal_4 = kWhToken.at(KWH_ADRESS).balances(os.environ["Address_4"],{"from":accounts[3]})
    bal_5 = kWhToken.at(KWH_ADRESS).balances(os.environ["Address_5"],{"from":accounts[3]})
    bal_SC = kWhToken.at(KWH_ADRESS).balances(MARKETPLACE_ADDRESS,{"from":accounts[3]})
    adr_1 = os.environ["Address_1"]
    adr_2 = os.environ["Address_2"]
    print(f"Account 0  ({adr_1}): {bal_1} kWh")
    print(f"Account 1  ({adr_2}): {bal_2} kWh")
    #print(f"Account 3: {bal_3}")
    #print(f"Account 4: {bal_4}")
    #print(f"Account 5: {bal_5}")
    print(f"Account SC ({MARKETPLACE_ADDRESS}): {bal_SC} kWh\n")

def main():
    while True:
        check_Balances()
        time.sleep(1)
    
    #mint()
    #check_Balances()