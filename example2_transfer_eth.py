from utils import *

if __name__ == "__main__":
    w3 = connect()
    keys = ["0xBD0FC2D2C54F836B6C9C90B66AFBB66F382CD7DA51FD62F8B236887436E94956",
            "0x79EBEE964F761090AC92E8B88DE48983A418C3071A61006D038BA17330298D88"]

    sender = Account.privateKeyToAccount(keys[0])
    print("Sender: ", sender.address)

    receiver = Account.privateKeyToAccount(keys[1])
    receiver_addr = receiver.address
    print("Receiver: ", receiver_addr)

    tx = build_tx(sender, receiver_addr, 1000000000000000000, w3)

    tx_signed = sign_tx(tx, sender, w3)

    receipt = send_signed_tx(tx_signed, w3)
    print("Included by block: ", receipt['blockNumber'])
