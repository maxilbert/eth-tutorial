from web3 import Web3, HTTPProvider
import time
from eth_account import Account
import rlp


def connect():
    WS = HTTPProvider('https://ropsten.infura.io/v3/80600ab9eedf4cd59f5efcb85ed93ede')
    w3 = Web3([WS])
    if w3.isConnected() and not w3.eth.syncing:
        print("Connected to: " + w3.version.node)
    elif w3.eth.syncing:
        print("Connected to: " + w3.version.node + ", but it is syncing")
        exit(255)
    else:
        exit(255)
    return w3


def build_tx(sender: Account, receiver_addr, value: int, w3: Web3, gas=21000, data=''):
    nonce = w3.eth.getTransactionCount(sender.address)
    print("Sender nonce: ", nonce)
    tx = {
        'to': receiver_addr,
        'value': value,
        'gasPrice': 2000000000,
        'gas': gas,
        'nonce': nonce,
        'chainId': 3,
        'data': data
    }
    print('Transaction: ', tx)
    return tx


def sign_tx(tx: dict, sender: Account, w3: Web3):
    tx_signed = w3.eth.account.signTransaction(tx, sender.privateKey)
    #tx_signed = sender.signTransaction(tx)
    print("Raw TX: ", tx_signed.rawTransaction.hex())
    print("Signature r: ", tx_signed.r)
    print("Signature s: ", tx_signed.s)
    print("Signature v: ", tx_signed.v)
    return tx_signed


def send_signed_tx(tx_signed: dict, w3: Web3):
    tx_hash = w3.toHex(w3.eth.sendRawTransaction(tx_signed.rawTransaction))
    print("TX hash: ", tx_hash)
    return wait_for_receipt(tx_hash, w3)


def build_tx_to_contract(sender: Account, contract, func: str, w3: Web3, args):
    nonce = w3.eth.getTransactionCount(sender.address)
    print("Sender nonce: ", nonce)
    tx = contract.functions[func](
        *args
    ).buildTransaction({
        'chainId': 3,
        'gas': 700000,
        'gasPrice': 5000000000,
        'nonce': nonce,
    })
    print(tx)
    return tx


def build_tx_to_deploy_contract(sender: Account, contract, w3: Web3, args):
    nonce = w3.eth.getTransactionCount(sender.address)
    print("Sender nonce: ", nonce)
    tx = contract.constructor(
        *args
    ).buildTransaction({
        'chainId': 3,
        'gas': 7000000,
        'gasPrice': 5000000000,
        'nonce': nonce,
    })
    print(tx)
    return tx


def precompute_contract_addr(sender: Account, w3: Web3):
    nonce = w3.eth.getTransactionCount(sender.address)
    sender = int(sender.address, 16)
    # Last 20 bytes or the last 40 hexadecimal characters
    contract_address = w3.sha3(rlp.encode([sender, nonce]))[-20:]
    print("Contract address (predicated): ", w3.toChecksumAddress(contract_address))
    return w3.toChecksumAddress(contract_address)


def wait_for_receipt(tx_hash, w3: Web3):
    while True:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        time.sleep(1)
