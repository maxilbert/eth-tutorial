import time
from web3 import Web3, HTTPProvider
from ethereum.utils import *


def wait_for_receipt(w3, tx_hash, poll_interval):
   while True:
       tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
       if tx_receipt:
         return tx_receipt
       time.sleep(poll_interval)

keys = ["0x49A84BB8270017202E8B49079CC9C54120CD0705E8C38D847BECD31FCB9B1105",
        "0xE9832B5B33A5F62EC6F41D1D7CD499F9650E73F9111324FEBE239311EFE5E237"]

WS = HTTPProvider('https://ropsten.infura.io/v3/80600ab9eedf4cd59f5efcb85ed93ede')
w3 = Web3([WS])
if w3.isConnected() and not w3.eth.syncing:
    print("Connected to: " + w3.version.node)
elif w3.eth.syncing:
    print("Connected to: " + w3.version.node + ", but it is syncing")
    exit(255)
else:
    exit(255)

sender_addr = w3.toChecksumAddress(w3.toHex(privtoaddr(keys[0])))
print("Sender: ", sender_addr)

nonce = w3.eth.getTransactionCount(sender_addr)
print(nonce)

# Complied binary code of SimpleDataStorage contract
addr = '0xc935aCFC949e221Db983a0e4A74B1a69A15B2952'
bin = '0x608060405234801561001057600080fd5b50336000806101000a81548173ffffffffffffffffffffffffffffffffffffffff021916908373ffffffffffffffffffffffffffffffffffffffff1602179055506101cf806100606000396000f3fe608060405260043610610051576000357c0100000000000000000000000000000000000000000000000000000000900480636057361d1461005657806373d4a13a146100915780638da5cb5b146100bc575b600080fd5b34801561006257600080fd5b5061008f6004803603602081101561007957600080fd5b8101908080359060200190929190505050610113565b005b34801561009d57600080fd5b506100a6610178565b6040518082815260200191505060405180910390f35b3480156100c857600080fd5b506100d161017e565b604051808273ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff16815260200191505060405180910390f35b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff1673ffffffffffffffffffffffffffffffffffffffff163373ffffffffffffffffffffffffffffffffffffffff1614151561016e57600080fd5b8060018190555050565b60015481565b6000809054906101000a900473ffffffffffffffffffffffffffffffffffffffff168156fea165627a7a7230582042b71c3c46a7f59b63b2965f2dc5b51955d0b9ec504a5a13c1385d23fdb48a2d0029'
abi = '[{"constant":false,"inputs":[{"name":"d","type":"uint256"}],"name":"store","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"data","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]'

SimpleDataStorage = w3.eth.contract(abi=abi, bytecode=bin, address=addr)

store_data_tx = SimpleDataStorage.functions.store(
    111
).buildTransaction({
    'chainId': 3,
    'gas': 70000,
    'gasPrice': 5000000000,
    'nonce': nonce,
})
print(store_data_tx)

signed_tx = w3.eth.account.signTransaction(store_data_tx, keys[0])
print("Raw TX: ", signed_tx.rawTransaction)
print("Signature r: ", signed_tx.r)
print("Signature s: ", signed_tx.s)
print("Signature v: ", signed_tx.v)

tx_hash = w3.toHex(w3.eth.sendRawTransaction(signed_tx.rawTransaction))
print("TX hash: ", tx_hash)


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
