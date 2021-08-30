import os
from dotenv import load_dotenv
from brownie import kWhToken, accounts, Marketplace

load_dotenv()

def deploy_kWh_Token():
    """
    Deploys kwhToken Contract to Ganache 
    """
    kWh = kWhToken.deploy({"from":accounts[9]})
    return kWh


def deploy_marketplace():
    """
    Deploys Marketplace Contract to Ganache 
    """
    marketplace = Marketplace.deploy({"from":accounts[9]})
    return marketplace


def main():
    deploy_kWh_Token()
    deploy_marketplace()

if __name__ == "__main__":
    main()