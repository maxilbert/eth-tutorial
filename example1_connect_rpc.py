from web3 import Web3, HTTPProvider


def connet():
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


if __name__ == "__main__":
    connet()
