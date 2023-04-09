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

    compiled_contract_path = 'build/contracts/Certification.json'
    
    deployed_contract_address = '0x4A6b1D2fB52e054806c8543C73d2E41F9D64cC4e'
    
    with open(compiled_contract_path) as file:
        contract_json = json.load(file) 
        
        contract_abi = contract_json['abi']
    
    contract = web3.eth.contract(address = deployed_contract_address, abi = contract_abi)
    
    
    # hash = input("Enter the hash of the block: ")

    # info = contract.functions.viewCertificates().call(block_identifier=hash)
    # print(info)


    hash = input("Enter the hash of the transaction: ")
    
    info_dict = web3.eth.get_transaction(hash)

    certificate = contract.decode_function_input(info_dict.input)

    ts = web3.eth.get_block(web3.eth.get_transaction(hash).blockNumber).timestamp

    from datetime import datetime
    print(certificate, datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y'))
except ValueError as e:
    print(e)