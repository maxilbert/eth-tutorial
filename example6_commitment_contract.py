from example5_deploy_contract_with_args import *

if __name__ == "__main__":

    w3 = connet()
    keys =["0x49A84BB8270017202E8B49079CC9C54120CD0705E8C38D847BECD31FCB9B1105",
            "0xE9832B5B33A5F62EC6F41D1D7CD499F9650E73F9111324FEBE239311EFE5E237"]
    sender = Account.privateKeyToAccount(keys[0])


    msg = 'Hello, world!'
    rnd = 53248509432865038609438560456
    comm = w3.soliditySha3(['string', 'bytes32'], [msg, w3.soliditySha3(['uint256'], [rnd])])

    # Complied binary code of SimpleDataStorage contract
    #addr
    bin = '0x6080604052600060010260005534801561001857600080fd5b506040516020806103318339810180604052602081101561003857600080fd5b810190808051906020019092919050505080600081905550506102d1806100606000396000f3fe608060405260043610610046576000357c01000000000000000000000000000000000000000000000000000000009004806343afdaaf1461004b578063708b473014610076575b600080fd5b34801561005757600080fd5b50610060610148565b6040518082815260200191505060405180910390f35b34801561008257600080fd5b506101466004803603604081101561009957600080fd5b81019080803590602001906401000000008111156100b657600080fd5b8201836020820111156100c857600080fd5b803590602001918460018302840111640100000000831117156100ea57600080fd5b91908080601f016020809104026020016040519081016040528093929190818152602001838380828437600081840152601f19601f8201169050808301925050505050505091929192908035906020019092919050505061014e565b005b60005481565b6000828260405160200180828152602001915050604051602081830303815290604052805190602001206040516020018083805190602001908083835b6020831015156101b0578051825260208201915060208101905060208303925061018b565b6001836020036101000a038019825116818451168082178552505050505050905001828152602001925050506040516020818303038152906040528051906020012090508060005414151561020457600080fd5b7ff040279f20c4475afca9a566d33b14e09c92fcb6460fb4121fadf563ab9ecc1f836040518080602001828103825283818151815260200191508051906020019080838360005b8381101561026657808201518184015260208101905061024b565b50505050905090810190601f1680156102935780820380516001836020036101000a031916815260200191505b509250505060405180910390a150505056fea165627a7a7230582031705072ad3eada26201a0df9a34d8fc8b1a29dbf2303b54cff1c2f5c2f45d460029'
    abi = '[{"constant":true,"inputs":[],"name":"comm","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"message","type":"string"},{"name":"rnd","type":"uint256"}],"name":"reveal","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"c","type":"bytes32"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":false,"name":"msg","type":"string"}],"name":"Reveal","type":"event"}]'
    Commitment = w3.eth.contract(abi=abi, bytecode=bin)


    # Deploy a contract with committing
    deploy_tx = build_tx_deploy_contract(sender, Commitment, w3, [comm])
    deploy_tx_signed = sign_tx(deploy_tx, sender, w3)
    deploy_receipt = send_signed_tx(deploy_tx_signed, w3)
    print("Included by block: ", deploy_receipt['blockNumber'])
    print('Contract address: ', deploy_receipt['contractAddress'])

    Commitment = w3.eth.contract(abi=abi, bytecode=bin, address=deploy_receipt['contractAddress'])
    reveal_tx = build_tx_to_contract(sender, Commitment, 'reveal', w3, [msg, rnd])
    reveal_tx_signed = sign_tx(reveal_tx, sender, w3)
    receipt = send_signed_tx(reveal_tx_signed, w3)
    print("Included by block: ", receipt['blockNumber'])
    print('Contract address: ', receipt['contractAddress'])


'''
pragma solidity ^0.5.1;
    
contract Commitment {
    
    bytes32 public comm = 0x0;
    event Reveal(string msg);

    
    constructor (bytes32 c) public {
        comm = c;
    }
    
    function reveal (string memory message, uint256 rnd) public  {
        bytes32 comm_1= keccak256(
            abi.encodePacked(
                message, keccak256(abi.encodePacked(rnd))
            )
        );
        require(comm == comm_1);
        emit Reveal(message);
    }
    
}
'''