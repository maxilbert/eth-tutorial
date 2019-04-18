from example2_transfer_eth import *


if __name__ == "__main__":

    keys = ["0x49A84BB8270017202E8B49079CC9C54120CD0705E8C38D847BECD31FCB9B1105",
            "0xE9832B5B33A5F62EC6F41D1D7CD499F9650E73F9111324FEBE239311EFE5E237"]

    '''
    pragma solidity ^0.5.1;
    
    contract SimpleDataStorage {
    
        address public owner;
    
        uint256 public data;
    
        constructor () public {
            owner = msg.sender;
        }
    
        function store (uint256 d) public  {
            require (msg.sender == owner);
            data = d;
        }
    
    }
    '''
    # Complied binary code of SimpleDataStorage contract
    bin = '0x608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506101cf806100606000396000f3fe608060405260043610610051576000357c0100000000000000000000000000000000000000000000000000000000900480636057361d1461005657806373d4a13a146100915780638da5cb5b146100bc575b600080fd5b34801561006257600080fd5b5061008f6004803603602081101561007957600080fd5b8101908080359060200190929190505050610113565b005b34801561009d57600080fd5b506100a6610178565b6040518082815260200191505060405180910390f35b3480156100c857600080fd5b506100d161017e565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561016e57600080fd5b8060018190555050565b60015481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff168156fea165627a7a7230582042b71c3c46a7f59b63b2965f2dc5b51955d0b9ec504a5a13c1385d23fdb48a2d0029'

    w3 = connet()

    sender = Account.privateKeyToAccount(keys[0])
    print("Sender: ", sender.address)

    tx = build_tx(sender.address, '', 0, w3, 470000, bin)

    tx_signed = sign_tx(tx, sender, w3)

    receipt = send_signed_tx(tx_signed, w3)
    print("Included by block: ", receipt['blockNumber'])
    print('Contract address: ', receipt['contractAddress'])
