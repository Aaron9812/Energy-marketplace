// SPDX-License-Identifier: UNLICENSED
pragma solidity 0.8.7;

contract Marketplace{
    struct Offer {
        address payable creator;
        uint64 kWhAmount;
        uint64 PriceUnit;
        uint64 Price;
        uint Created;
        bool forSale;
    }

    uint128 total_Offers;
    mapping(uint128 => Offer) public offers;
    
    event OfferCreated(address creator, uint Price);

    error BalanceAmountError(uint Price, uint valueSent);
    error EnergyAlreadyBought(uint offerID, bool forSale);
    
    function createOffer(
        address kWh_contract,
        uint64 kWhAmount,
        uint64 PriceUnit 
    ) public returns (uint128 offerID){
        require(callBalance(kWh_contract, msg.sender) >= kWhAmount, "You don't have enought energy to sell this much");    
            Offer storage offer = offers[total_Offers];

            offer.creator = payable(msg.sender);
            offer.kWhAmount = kWhAmount;
            offer.PriceUnit = PriceUnit;
            offer.Price = PriceUnit * kWhAmount;
            offer.Created = block.timestamp;
            offer.forSale = true;

            callSend(kWh_contract, msg.sender, address(this), offer.kWhAmount);    
            emit OfferCreated(msg.sender, offer.Price);
            
            total_Offers +=1;
            return total_Offers - 1;
        }


        function changeEnergyAmount(uint128 offerID, uint64 kWhAmount) public{
            Offer storage offer = offers[offerID];
            require(msg.sender == offer.creator, "You dind't create the offer");
            offer.kWhAmount = kWhAmount;
            offer.Price = kWhAmount * offer.PriceUnit;
        }

        
        function changePrice(uint128 offerID, uint64 PriceUnit) public{
            Offer storage offer = offers[offerID];
            require(msg.sender == offer.creator, "You dind't create the offer");
            offer.PriceUnit = PriceUnit;
            offer.Price = offer.kWhAmount * offer.PriceUnit;
        }


        function buy(uint128 offerID, address kWh_contract) public payable {
            Offer storage offer = offers[offerID];

            if(offer.forSale == false)
            revert EnergyAlreadyBought({
                offerID: offerID,
                forSale: false
            });
           
            if(offer.Price != msg.value)
            revert BalanceAmountError({
                Price: offer.Price,
                valueSent: msg.value
            });

            offer.creator.transfer(offer.Price);
            callSend(kWh_contract, address(this), msg.sender, offer.kWhAmount);
            offer.kWhAmount = 0;
            offer.PriceUnit = 0;
            offer.Price = 0;
            offer.forSale = false;
        }   


        function getTotal_Offers() public view returns (uint){
            return total_Offers;
        } 


        function callBalance(address kWh_contract, address user) public view returns (uint){
            kWhToken Balance = kWhToken(kWh_contract);
            return Balance.getBalance(user);
        }


        function callSend(address kWh_contract, address sender, address reciver, uint64 number_Tokens) public {
            kWhToken Balance = kWhToken(kWh_contract);
            Balance.send(sender, reciver, number_Tokens);
        }
}

contract kWhToken {
    address public minter;
    mapping (address => uint128) public balances;

    event Sent(address sender, address reciver, uint64 number_Tokens);
    event Burn(address user, uint64 number_Tokens);
    event Mint(address reciver, uint64 number_Tokens);

    error BalancetoSmall(uint requested, uint balance);

    constructor(){
        minter = msg.sender;
    }


    function mint(address reciver, uint64 number_Tokens) public{
        require(msg.sender == minter, "You are not allowed to create Tokens");
        balances[reciver] += number_Tokens;

        emit Mint(reciver, number_Tokens);
    }


    function send(address sender,address receiver, uint64 number_Tokens) public{
        if(number_Tokens > balances[sender])
            revert BalancetoSmall({
                requested: number_Tokens,
                balance: balances[sender]
            });

        balances[sender] -= number_Tokens;
        balances[receiver] += number_Tokens;

        emit Sent(sender, receiver, number_Tokens);
    }


    function burn(address user, uint64 number_Tokens) public{
        require(number_Tokens <= balances[msg.sender], "You need to buy more energy");
        balances[user] -= number_Tokens;

        emit Burn(user, number_Tokens);
    }   
    
    
    function getBalance(address user) external view returns (uint) {
       return balances[user];
    }
}


