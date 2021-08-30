import os
from dotenv import load_dotenv
from brownie import Marketplace, accounts


load_dotenv()

def main():
    """
    Deploys Marketplace Contract to Ganache 
    """
    marketplace = Marketplace.deploy({"from":accounts[9]})
    return marketplace


if __name__ == "__main__":
    main()