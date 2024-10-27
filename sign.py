import eth_account
from web3 import Web3
from eth_account.messages import encode_defunct


def sign(m):
    w3 = Web3()
    # create an eth account and recover the address (derived from the public key) and private key
    # your code here
    account = eth_account.Account.create()

    eth_address = account.address # Eth account
    private_key = account.privateKey

    # generate signature
    # your code here
    message = encode_defunct(text=m)

    signed_message = account.sign_message(message)

    assert isinstance(signed_message, eth_account.datastructures.SignedMessage)

    return eth_address, signed_message
