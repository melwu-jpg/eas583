from web3 import Web3
from web3.contract import Contract
from web3.providers.rpc import HTTPProvider
from web3.middleware import geth_poa_middleware #Necessary for POA chains
import json
import sys
from pathlib import Path

source_chain = 'avax'
destination_chain = 'bsc'
contract_info = "contract_info.json"

def connectTo(chain):
    if chain == 'avax':
        api_url = f"https://api.avax-test.network/ext/bc/C/rpc" #AVAX testnet

    if chain == 'bsc':
        api_url = f"https://data-seed-prebsc-1-s1.binance.org:8545/" #BSC testnet

    if chain in ['avax','bsc']:
        w3 = Web3(Web3.HTTPProvider(api_url))
        w3.middleware_onion.inject(geth_poa_middleware, layer=0)
    return w3

def getContractInfo(chain):
    """
        Load the contract_info file into a dictinary
        This function is used by the autograder and will likely be useful to you
    """
    p = Path(__file__).with_name(contract_info)
    try:
        with p.open('r')  as f:
            contracts = json.load(f)
    except Exception as e:
        print( "Failed to read contract info" )
        print( "Please contact your instructor" )
        print( e )
        sys.exit(1)

    return contracts[chain]


def scanBlocks(chain):
    """
        chain - (string) should be either "source" or "destination"
        Scan the last 5 blocks of the source and destination chains
        Look for 'Deposit' events on the source chain and 'Unwrap' events on the destination chain
        When Deposit events are found on the source chain, call the 'wrap' function the destination chain
        When Unwrap events are found on the destination chain, call the 'withdraw' function on the source chain
    """

    if chain not in ['source','destination']:
        print( f"Invalid chain: {chain}" )
        return

    #YOUR CODE HERE

    #Connect to chain
    if chain == 'source':
        w3 = connectTo(source_chain)
        contract_info = getContractInfo('source')
        event_name = 'deposit'
        action_function = wrap

    if chain == 'destination':
        w3 = connectTo(destination_chain)
        contract_info = getContractInfo('destination')
        event_name = 'unwrap'
        action_function = withdraw
    
    #Access the contract
    contract = w3.eth.contract(address=contract_info['address'],abi=contract_info['abi'])

    #Scan the 5 blocks
    latest_block = w3.eth.block_number #gets the last block?
    start_block = latest_block - 5
    event_filter = contract.events.event_name.create_filter(fromBlock = start_block, toBlock = 'latest')

    #Get events in the filter
    while True:
      events = event_filter.get_new_entries()
      if events:
        for event in events:
          action_function(event, contract_info)
      time.sleep(8)


# def deployRegisterToken():
#     source_contract = connect_to('avax').eth.contract('xxx',abi='xxx')

def wrap(event, contract_info):
    w3 = connectTo(destination_chain)
    contract = w3.eth.contract(address=contract_info['address'],abi=contract_info['abi'])


    wrap_function = contract.functions.wrap(
        event.args['amount'], event.args['from'], event.args['token']
    )

    warden_address = contract_info['WARDEN_ROLE']
    private_key = "0x8bd9c9a722284277bfb283491035f3b83d1b53d08a4a86d4e5f7533d20859272" 
    # acct = w3.eth.account.privateKeyToAccount(private_key)
    acct = source_w3.eth.account.from_key(private_key)

    tx = contract.functions.wrap(proof, random_leaf).build_transaction({
        'chainId': 97, 
        'gas': 2000000,
        'gasPrice': w3.to_wei('5', 'gwei'),
        'nonce': w3.eth.get_transaction_count(acct.address),
        'from': acct.address  
    })

    signed_tx = w3.eth.account.sign_transaction(tx, acct.key)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

def withdraw(event, contract_info):
    w3 = connectTo(source_chain)
    contract = w3.eth.contract(address=contract_info['address'], abi=contract_info['abi'])

    withdraw_function = contract.functions.withdraw(
        event.args['amount'], event.args['to'], event.args['token']
    )

    warden_address = contract_info['WARDEN_ROLE']
    private_key = "0x8bd9c9a722284277bfb283491035f3b83d1b53d08a4a86d4e5f7533d20859272" 
    
    tx = withdraw_function.build_transaction({
        'from': warden_address,
        'gas': 2000000,
        'gasPrice': w3.toWei('5', 'gwei'),
        'nonce': w3.eth.get_transaction_count(warden_address),
    })

    signed_tx = w3.eth.account.sign_transaction(tx, private_key)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
