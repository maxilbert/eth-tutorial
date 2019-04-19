from utils import *

if __name__ == "__main__":
    keys = ["0xBD0FC2D2C54F836B6C9C90B66AFBB66F382CD7DA51FD62F8B236887436E94956",
            "0x79EBEE964F761090AC92E8B88DE48983A418C3071A61006D038BA17330298D88"]

    '''
    pragma solidity ^0.5.1;
    
    contract SimpleDataStorage {
    
        address public owner;

        uint256 public data;
    
        constructor (uint arg) public {
            owner = msg.sender;
            data = arg;
        }
    
        function store (uint256 d) public  {
            require (msg.sender == owner);
            data = d;
        }
    
    }
    '''

    # Complied binary code of SimpleDataStorage contract
    bin = '0x608060405234801561001057600080fd5b506040516020806102678339810180604052602081101561003057600080fd5b8101908080519060200190929190505050336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff16021790555080600181905550506101cf806100986000396000f3fe608060405260043610610051576000357c0100000000000000000000000000000000000000000000000000000000900480636057361d1461005657806373d4a13a146100915780638da5cb5b146100bc575b600080fd5b34801561006257600080fd5b5061008f6004803603602081101561007957600080fd5b8101908080359060200190929190505050610113565b005b34801561009d57600080fd5b506100a6610178565b6040518082815260200191505060405180910390f35b3480156100c857600080fd5b506100d161017e565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561016e57600080fd5b8060018190555050565b60015481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff168156fea165627a7a72305820a8de91442e7ea80ec8618d52d4d50e5d80f34c88c398cf2c863465a7e933ad660029'
    abi = '[{"constant":false,"inputs":[{"name":"d","type":"uint256"}],"name":"store","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"data","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"arg","type":"uint256"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]'
    w3 = connect()
    Storage = w3.eth.contract(abi=abi, bytecode=bin)

    sender = Account.privateKeyToAccount(keys[0])
    print("Sender: ", sender)

    tx = build_tx_to_deploy_contract(sender, Storage, w3, [112358])
    tx_signed = sign_tx(tx, sender, w3)
    contract_addr = precompute_contract_addr(sender, w3)

    receipt = send_signed_tx(tx_signed, w3)
    print("Included by block: ", receipt['blockNumber'])
    print('Contract address (deployed): ', receipt['contractAddress'])
    assert (contract_addr == receipt['contractAddress'])
