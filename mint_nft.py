from web3 import Web3
import random
import hashlib
import json
import eth_account

# Connect to Avalanche Fuji Testnet
w3 = Web3(Web3.HTTPProvider('https://api.avax-test.network/ext/bc/C/rpc'))

wallet_address = '0x4cE09F18425b3EA3DedFa5d07419224bb51FDf3a'  
private_key = '0x8bd9c9a722284277bfb283491035f3b83d1b53d08a4a86d4e5f7533d20859272'
acct = eth_account.Account.from_key(private_key)
contract_address = '0x85ac2e065d4526FBeE6a2253389669a12318A412'

# Load ABI from NFT.abi file
with open('NFT.abi', 'r') as abi_file:
    abi = json.load(abi_file)

# Create contract instance
nft_contract = w3.eth.contract(address=contract_address, abi=abi)

def claim_nft(wallet_address, nonce):
    # Convert nonce to bytes32
    nonce_bytes32 = w3.toBytes(nonce)  

    gas_price_wei = 100 * (10 ** 9)

    # Build transaction
    tx = nft_contract.functions.claim(wallet_address, nonce_bytes32).build_transaction({
        "from": acct.address,
        "nonce": w3.eth.get_transaction_count(acct.address),
        "gas": 200000,  
        "gasPrice": gas_price_wei, 
    })
    
    # Sign the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, private_key)

    # Send the transaction
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    
    # Wait for transaction receipt
    tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
    
    print(f"Transaction successful with hash: {tx_hash.hex()}")
    return tx_receipt

# Generate a random nonce and claim NFT
nonce = random.randint(1, 1000000)
claim_nft(wallet_address, nonce)
