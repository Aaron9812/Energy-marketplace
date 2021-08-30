import os
from dotenv import load_dotenv
from web3 import Web3

load_dotenv()
node_provider = os.environ["Node_Provider_local"]
web3_connection = Web3(Web3.HTTPProvider(node_provider))

#save smart contract abis for latter interaction
KW_ABI = '[{"inputs":[],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"requested","type":"uint256"},{"internalType":"uint256","name":"balance","type":"uint256"}],"name":"BalancetoSmall","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"user","type":"address"},{"indexed":false,"internalType":"uint64","name":"number_Tokens","type":"uint64"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"reciver","type":"address"},{"indexed":false,"internalType":"uint64","name":"number_Tokens","type":"uint64"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"sender","type":"address"},{"indexed":false,"internalType":"address","name":"reciver","type":"address"},{"indexed":false,"internalType":"uint64","name":"number_Tokens","type":"uint64"}],"name":"Sent","type":"event"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"balances","outputs":[{"internalType":"uint128","name":"","type":"uint128"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"},{"internalType":"uint64","name":"number_Tokens","type":"uint64"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"user","type":"address"}],"name":"getBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"reciver","type":"address"},{"internalType":"uint64","name":"number_Tokens","type":"uint64"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"minter","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"receiver","type":"address"},{"internalType":"uint64","name":"number_Tokens","type":"uint64"}],"name":"send","outputs":[],"stateMutability":"nonpayable","type":"function"}]'
MARKETPLACE_ABI ='[{"inputs":[{"internalType":"uint256","name":"Price","type":"uint256"},{"internalType":"uint256","name":"valueSent","type":"uint256"}],"name":"BalanceAmountError","type":"error"},{"inputs":[{"internalType":"uint256","name":"offerID","type":"uint256"},{"internalType":"bool","name":"forSale","type":"bool"}],"name":"EnergyAlreadyBought","type":"error"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"creator","type":"address"},{"indexed":false,"internalType":"uint256","name":"Price","type":"uint256"}],"name":"OfferCreated","type":"event"},{"inputs":[{"internalType":"uint128","name":"offerID","type":"uint128"},{"internalType":"address","name":"kWh_contract","type":"address"}],"name":"buy","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[{"internalType":"address","name":"kWh_contract","type":"address"},{"internalType":"address","name":"user","type":"address"}],"name":"callBalance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"kWh_contract","type":"address"},{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"reciver","type":"address"},{"internalType":"uint64","name":"number_Tokens","type":"uint64"}],"name":"callSend","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint128","name":"offerID","type":"uint128"},{"internalType":"uint64","name":"kWhAmount","type":"uint64"}],"name":"changeEnergyAmount","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"uint128","name":"offerID","type":"uint128"},{"internalType":"uint64","name":"PriceUnit","type":"uint64"}],"name":"changePrice","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"kWh_contract","type":"address"},{"internalType":"uint64","name":"kWhAmount","type":"uint64"},{"internalType":"uint64","name":"PriceUnit","type":"uint64"}],"name":"createOffer","outputs":[{"internalType":"uint128","name":"offerID","type":"uint128"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"getTotal_Offers","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint128","name":"","type":"uint128"}],"name":"offers","outputs":[{"internalType":"addresspayable","name":"creator","type":"address"},{"internalType":"uint64","name":"kWhAmount","type":"uint64"},{"internalType":"uint64","name":"PriceUnit","type":"uint64"},{"internalType":"uint64","name":"Price","type":"uint64"},{"internalType":"uint256","name":"Created","type":"uint256"},{"internalType":"bool","name":"forSale","type":"bool"}],"stateMutability":"view","type":"function"}]'

GLOBAL_GAS = 4500000
GLOBAL_GAS_PRICE = web3_connection.toWei(8, "gwei")
kwH_Token = web3_connection.eth.contract(
        address=os.environ["kWh_Contract_address"],
        abi=KW_ABI
    )


Marketplace = web3_connection.eth.contract(
        address=os.environ["Marketplace_Contract_address"],
        abi=MARKETPLACE_ABI
    ) 


class Offer(object):
    def __init__(self, owner, Amount_kWh, Unit_Price, id):
        """
        Class to display offers on platform
        """
        self.owner = owner
        self.Amount_kWh = Amount_kWh
        self.Unit_Price = Unit_Price
        self.Total_Price = Amount_kWh * Unit_Price
        self.id = id


def are_we_connecter():
    return(web3_connection.isConnected())


def get_nonce(ETH_address):
    return web3_connection.eth.get_transaction_count(ETH_address)


def login_user(user_address, user_key):
    """
    Login user by signing a trx with 1 wei
    """
    transaction_body = {
        "nonce": get_nonce(user_address),
        "to":os.environ["Address_9"],
        "value":1,
        "gas": GLOBAL_GAS,
        "gasPrice": GLOBAL_GAS_PRICE
    }
    try:
        web3_connection.eth.account.sign_transaction(transaction_body, user_key)
    except:
        return False
    return True


def get_Balance_kWh(user_address):  
    """
    Get kWh Account balance
    """
    addr = Web3.toChecksumAddress(user_address)
    balance_kWh = kwH_Token.functions.getBalance(addr).call()
    return balance_kWh


def get_Balance_eth(user_address):
    """
    Get Ether Account balance
    """
    addr = Web3.toChecksumAddress(user_address)
    balance_wei = web3_connection.eth.get_balance(addr)
    balance_eth = round(web3_connection.fromWei(balance_wei, "ether"),2)
    return balance_eth


def get_Offer(offer_num):
    """
    Get single offer as list
    """
    Offers = []
    offer_num = int(offer_num)
    result = Marketplace.functions.offers(offer_num).call()
    Offers.append(Offer(result[0],result[1],result[2]/1e18,offer_num))
    return Offers 


def create_Offer(user_address, ammount_kWh, price_unit):
    """
    Create offer for user
    """
    kWh_contract_address = Web3.toChecksumAddress(os.environ["kWh_Contract_address"])
    user_address = Web3.toChecksumAddress(user_address)
    amount = int(ammount_kWh)
    Price = web3_connection.toWei(price_unit, "ether")
    Marketplace.functions.createOffer(kWh_contract_address,amount,Price).transact({"from":user_address})


def change_Offer_price(offerID, user_address, price_unit):
    """
    Create offer for user
    """
    offerID = int(offerID)
    user_address = Web3.toChecksumAddress(user_address)
    Price = web3_connection.toWei(price_unit, "ether")
    Marketplace.functions.changePrice(offerID,Price).transact({"from":user_address})


def buy_Offer(user_address, offer_id):
    """
    Buy offer for user
    """
    kWh_contract_address = Web3.toChecksumAddress(os.environ["kWh_Contract_address"])
    user_address = Web3.toChecksumAddress(user_address)
    offer_id = int(offer_id)   
    offer_price = web3_connection.toWei(get_Offer(offer_id)[0].Total_Price, "ether") 
    Marketplace.functions.buy(offer_id,kWh_contract_address).transact({"from":user_address,"value":offer_price})


def get_user_Offers(user_address):
    """
    Get all offers for one user
    """
    num_offers = Marketplace.functions.getTotal_Offers().call()
    Offers = []

    for offer in range(0, num_offers):
        result = Marketplace.functions.offers(offer).call()
        if result[5] and result[0] == user_address:
            Offers.append(Offer(result[0],result[1],result[2]/1e18,offer))
    return Offers


def get_Offers():
    """
    Get all offers that are active
    """
    num_offers = Marketplace.functions.getTotal_Offers().call()
    Offers = []

    for offer in range(0, num_offers):
        result = Marketplace.functions.offers(offer).call()
        if result[5]:
            Offers.append(Offer(result[0],result[1],result[2]/1e18,offer))
    return Offers


if __name__ == "__main__":
    test = are_we_connecter()
    print(test)
