from web3 import Web3, HTTPProvider
from ethereum.utils import *

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

receiver_addr = w3.toChecksumAddress(w3.toHex(privtoaddr(keys[1])))
print("Receiver: ", receiver_addr)

nonce = w3.eth.getTransactionCount(sender_addr)
print(nonce)

tx = {
    'to': receiver_addr,
    'value': 10000000000000000000,
    'gasPrice': 5000000000,
    'gas': 21000,
    'nonce': nonce,
    'chainId': 3
}
#tx['gas'] = w3.eth.estimateGas(tx)

signed_tx = w3.eth.account.signTransaction(tx, keys[0])
print("Raw TX: ", signed_tx.rawTransaction)
print("Signature r: ", signed_tx.r)
print("Signature s: ", signed_tx.s)
print("Signature v: ", signed_tx.v)

tx_hash = w3.toHex(w3.eth.sendRawTransaction(signed_tx.rawTransaction))
print("TX hash: ", tx_hash)
