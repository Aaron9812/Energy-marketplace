import os
from dotenv import load_dotenv
from brownie import kWhToken, accounts


load_dotenv()

def main():
    """
    Deploys kwhToken Contract to Ganache 
    """
    kWh = kWhToken.deploy({"from":accounts[9]})
    return kWh


if __name__ == "__main__":
    main()