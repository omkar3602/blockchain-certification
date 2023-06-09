import json
from web3 import Web3, HTTPProvider
from dotenv import load_dotenv
import os
import web3.exceptions as exceptions
from datetime import datetime

def issue_certificate(address, name, competitionName, email):
    try:
        load_dotenv()
        blockchain_address = os.getenv('BLOCKCHAIN_ADDRESS')
        
        web3 = Web3(HTTPProvider(blockchain_address))
        
        if web3.is_connected():
            print("-" * 50)
            print("Connection Successful")
            print("-" * 50)
        else:
            print("Connection Failed")
        
        caller = os.getenv('CALLER_ADDRESS')
        private_key = os.getenv('PRIVATE_KEY')

        nonce = web3.eth.get_transaction_count(caller)

        compiled_contract_path = 'utils/contracts/Certification.json'
        
        deployed_contract_address = os.getenv('DEPLOYED_CONTRACT_ADDRESS')
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file) 
            
            contract_abi = contract_json['abi']
        
        contract = web3.eth.contract(address = deployed_contract_address, abi = contract_abi)
        

        Chain_id = web3.eth.chain_id
        call_function = contract.functions.issueCertificate(address, name, competitionName, email).build_transaction({"chainId": Chain_id, "from": caller, "nonce": nonce})

        signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)

        send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)


        return tx_receipt
    except exceptions.Web3Exception as e:
        print(e)
        return -1
    except ValueError as e:
        print(e)
        return -1

def addCertificateID(id):
    try:
        load_dotenv()
        blockchain_address = os.getenv('BLOCKCHAIN_ADDRESS')
        
        web3 = Web3(HTTPProvider(blockchain_address))
        
        if web3.is_connected():
            print("-" * 50)
            print("Connection Successful")
            print("-" * 50)
        else:
            print("Connection Failed")
        
        caller = os.getenv('CALLER_ADDRESS')
        private_key = os.getenv('PRIVATE_KEY')

        nonce = web3.eth.get_transaction_count(caller)

        compiled_contract_path = 'utils/contracts/Certification.json'
        
        deployed_contract_address = os.getenv('DEPLOYED_CONTRACT_ADDRESS')
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file) 
            
            contract_abi = contract_json['abi']
        
        contract = web3.eth.contract(address = deployed_contract_address, abi = contract_abi)
        

        Chain_id = web3.eth.chain_id
        call_function = contract.functions.addCertificateID(id).build_transaction({"chainId": Chain_id, "from": caller, "nonce": nonce})

        signed_tx = web3.eth.account.sign_transaction(call_function, private_key=private_key)

        send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

        tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)


        return tx_receipt
    except exceptions.Web3Exception as e:
        print(e)
        return -1
    except ValueError as e:
        print(e)
        return -1

def view_all():
    try:
        load_dotenv()
        blockchain_address = os.getenv('BLOCKCHAIN_ADDRESS')
        
        web3 = Web3(HTTPProvider(blockchain_address))
        
        if web3.is_connected():
            print("-" * 50)
            print("Connection Successful")
            print("-" * 50)
        else:
            print("Connection Failed")

        compiled_contract_path = 'utils/contracts/Certification.json'
        
        deployed_contract_address = os.getenv('DEPLOYED_CONTRACT_ADDRESS')
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file) 
            
            contract_abi = contract_json['abi']
        
        contract = web3.eth.contract(address = deployed_contract_address, abi = contract_abi)
        
        raw_certificates = contract.functions.viewCertificates().call()
        certificate_ids = contract.functions.viewCertificateIDs().call()

        certificates = []

        for certificate in raw_certificates:
            temp_certificate = []
            temp_certificate.append(certificate_ids[raw_certificates.index(certificate)][0])
            temp_certificate.append(certificate[0])
            temp_certificate.append(certificate[1])
            temp_certificate.append(certificate[2])
            temp_certificate.append(datetime.utcfromtimestamp(int(certificate[3])).strftime('%d %B %Y'))
            temp_certificate.append(certificate[4])
            certificates.append(temp_certificate)
        del raw_certificates

        return certificates
    
    except exceptions.Web3Exception as e:
        print(e)
        return -1
    except ValueError as e:
        print(e)



def view_certificate(id):

    try:
        load_dotenv()
        blockchain_address = os.getenv('BLOCKCHAIN_ADDRESS')
        
        web3 = Web3(HTTPProvider(blockchain_address))
        
        if web3.is_connected():
            print("-" * 50)
            print("Connection Successful")
            print("-" * 50)
        else:
            print("Connection Failed")

        compiled_contract_path = 'utils/contracts/Certification.json'
        
        deployed_contract_address = os.getenv('DEPLOYED_CONTRACT_ADDRESS')
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file) 
            
            contract_abi = contract_json['abi']
        
        contract = web3.eth.contract(address = deployed_contract_address, abi = contract_abi)
        
        
        info_dict = web3.eth.get_transaction(id)

        certificate = contract.decode_function_input(info_dict.input)
        ts = web3.eth.get_block(web3.eth.get_transaction(id).blockNumber).timestamp

        from datetime import datetime
        return [certificate[1]['name'], certificate[1]['competitionName'], datetime.utcfromtimestamp(ts).strftime('%d-%m-%Y'), certificate[1]['email']]
    except exceptions.Web3Exception as e:
        print(e)
        return -1
    except ValueError as e:
        print(e)
        return -1
    
def view_certificate_by_address(address):
    try:
        load_dotenv()
        blockchain_address = os.getenv('BLOCKCHAIN_ADDRESS')
        
        web3 = Web3(HTTPProvider(blockchain_address))
        
        if web3.is_connected():
            print("-" * 50)
            print("Connection Successful")
            print("-" * 50)
        else:
            print("Connection Failed")

        compiled_contract_path = 'utils/contracts/Certification.json'
        
        deployed_contract_address = os.getenv('DEPLOYED_CONTRACT_ADDRESS')
        
        with open(compiled_contract_path) as file:
            contract_json = json.load(file) 
            
            contract_abi = contract_json['abi']
        
        contract = web3.eth.contract(address = deployed_contract_address, abi = contract_abi)
        
        raw_certificates = contract.functions.viewCertificateByAddress(address).call()
        certificate_ids = contract.functions.viewCertificateIDByAddress(address).call()
        certificates = []
        if not raw_certificates == -1:
            for certificate in raw_certificates:
                if certificate[1] == '':
                    continue
                else:
                    temp_certificate = []
                    temp_certificate.append(certificate_ids[raw_certificates.index(certificate)][0])
                    temp_certificate.append(certificate[1])
                    temp_certificate.append(certificate[2])
                    temp_certificate.append(datetime.utcfromtimestamp(int(certificate[3])).strftime('%d %B %Y'))
                    certificates.append(temp_certificate)

        del raw_certificates

        return certificates



    except exceptions.Web3Exception as e:
        print(e)
        return -1
    except ValueError as e:
        print(e)
        return -1