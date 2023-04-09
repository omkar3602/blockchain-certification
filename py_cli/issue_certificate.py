import json
from web3 import Web3, HTTPProvider

try:
    blockchain_address = 'http://127.0.0.1:7545'
    
    web3 = Web3(HTTPProvider(blockchain_address))
    
    if web3.is_connected():
        print("-" * 50)
        print("Connection Successful")
        print("-" * 50)
    else:
        print("Connection Failed")
    
    caller = "0x68FFD6C6695E64fDe44cF491cb4619E05D592C2c"
    private_key = "0x09a73407c5078b3d159599da07104589cb93a74acac7fcafa2f4e465147836ca"

    nonce = web3.eth.get_transaction_count(caller)

    compiled_contract_path = 'build/contracts/Certification.json'
    
    deployed_contract_address = '0x4A6b1D2fB52e054806c8543C73d2E41F9D64cC4e'
    
    with open(compiled_contract_path) as file:
        contract_json = json.load(file) 
        
        contract_abi = contract_json['abi']
    
    contract = web3.eth.contract(address = deployed_contract_address, abi = contract_abi)
    



    to = input("Enter the address of the receiver: ")
    name = input("Enter the name of the receiver: ")
    competitionName = input("Enter the name of the competition: ")



    Chain_id = web3.eth.chain_id

    call_function = contract.functions.issueCertificate(to, name, competitionName).build_transaction({"chainId": Chain_id, "from": caller, "nonce": nonce})

    signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)

    send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)



    print(tx_receipt)
except ValueError as e:
    print(e)