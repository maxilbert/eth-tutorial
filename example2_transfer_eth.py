import time
from eth_account import Account
from example1_connect_rpc import connet


def build_tx(sender, receiver, value, w3, gas=21000, data=''):
    nonce = w3.eth.getTransactionCount(sender)
    print("Sender nonce: ", nonce)
    tx = {
        'to': receiver,
        'value': value,
        'gasPrice': 2000000000,
        'gas': gas,
        'nonce': nonce,
        'chainId': 3,
        'data': data
    }
    print('Transaction: ', tx)
    return tx


def sign_tx(tx, sender, w3):
    #tx_signed = sender.signTransaction(tx)
    tx_signed = w3.eth.account.signTransaction(tx, sender.privateKey)
    print("Raw TX: ", tx_signed.rawTransaction.hex())
    print("Signature r: ", tx_signed.r)
    print("Signature s: ", tx_signed.s)
    print("Signature v: ", tx_signed.v)
    return tx_signed


def send_signed_tx(tx_signed, w3):
    tx_hash = w3.toHex(w3.eth.sendRawTransaction(tx_signed.rawTransaction))
    print("TX hash: ", tx_hash)
    return wait_for_receipt(tx_hash, w3)


def wait_for_receipt(tx_hash, w3):
    while True:
        tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
        if tx_receipt:
            return tx_receipt
        time.sleep(1)


if __name__ == "__main__":
    w3 = connet()
    keys = ["0x49A84BB8270017202E8B49079CC9C54120CD0705E8C38D847BECD31FCB9B1105",
            "0xE9832B5B33A5F62EC6F41D1D7CD499F9650E73F9111324FEBE239311EFE5E237"]

    sender = Account.privateKeyToAccount(keys[0])
    print("Sender: ", sender.address)

    receiver = Account.privateKeyToAccount(keys[1])
    print("Receiver: ", receiver.address)

    tx = build_tx(sender.address, receiver.address, 1000000000000000000, w3)

    tx_signed = sign_tx(tx, sender, w3)

    receipt = send_signed_tx(tx_signed, w3)
    print("Included by block: ", receipt['blockNumber'])
