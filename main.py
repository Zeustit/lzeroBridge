from web3 import Web3
from eth_account import Account
from decimal import Decimal
import struct
import ctypes

RPC = [
    {'chain': 'Ethereum     ', 'chain_id': 1, 'rpc': 'https://rpc.ankr.com/eth'},
    {'chain': 'Goerli     ', 'chain_id': 5, 'rpc': 'https://goerli.blockpi.network/v1/rpc/public'},
    {'chain': 'Optimism Goerli Testnet     ', 'chain_id': 420, 'rpc': 'https://optimism-goerli.public.blastapi.io'},
    {'chain': 'Arbitrum One ', 'chain_id': 421613, 'rpc': 'https://goerli-rollup.arbitrum.io/rpc'},
]
ABI = '[{"inputs":[{"internalType":"address","name":"_weth","type":"address"},{"internalType":"address","name":"_oft","type":"address"},{"internalType":"address","name":"_swapRouter","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"oft","outputs":[{"internalType":"contract IOFTCore","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolFee","outputs":[{"internalType":"uint24","name":"","type":"uint24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"to","type":"address"},{"internalType":"address payable","name":"refundAddress","type":"address"},{"internalType":"address","name":"zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"adapterParams","type":"bytes"}],"name":"swapAndBridge","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapRouter","outputs":[{"internalType":"contract ISwapRouter","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"weth","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'
contract_address = '0x0A9f824C05A74F577A536A8A0c673183a872Dff4'
# private key
caller = '52e528d5f523ca7a97181e2eb3d67cc35f959dbe88e4442201d2565f31d09133'


def check_balance(address, chain_number):
    web3 = Web3(Web3.HTTPProvider(RPC[chain_number]['rpc']))
    balance = web3.eth.get_balance(web3.to_checksum_address(address))

    print(balance)


if __name__ == '__main__':

    # print('Enter min eth amount to send:')
    # min_amount = input()
    #
    # print('Enter max eth amount to send:')
    # max_amount = input()

    web3 = Web3(Web3.HTTPProvider('https://goerli.blockpi.network/v1/rpc/public'))
    # web3 = Web3(Web3.HTTPProvider('https://optimism-goerli.public.blastapi.io'))
    contract_instance = web3.eth.contract(address=contract_address, abi=ABI)
    check_balance('0x87d620A1aED74357b59fE2d05c41Bfa895caEcc8', 1)
    check_balance('0x87d620A1aED74357b59fE2d05c41Bfa895caEcc8', 2)
    check_balance('0x87d620A1aED74357b59fE2d05c41Bfa895caEcc8', 3)

    # initialize the chain id, we need it to build the transaction for replay protection
    # Chain_id = web3.eth.chain_id

    # Call your function
    address = web3.eth.account.from_key(caller).address
    eth_account = web3.eth.account.from_key(caller)
    # address = '0x87d620A1aED74357b59fE2d05c41Bfa895caEcc8'
    checksum_address = web3.to_checksum_address(address)
    print("gas:", web3.eth.gas_price)
    amountIn = web3.to_wei(Decimal('0.1'), 'ether')
    amountOutMin = web3.to_wei(Decimal('0.001'), 'ether')
    dstChainId = ctypes.c_uint16(420).value
    adapterParams = bytes('20000', 'utf-8')
    call_function = contract_instance.functions.swapAndBridge(amountIn, amountOutMin, dstChainId, checksum_address, checksum_address, checksum_address, adapterParams).build_transaction(
         {"chainId": 5, "from": checksum_address, "nonce": 5, "gasLimit":  web3.eth.gas_price, "value": web3.to_wei(Decimal('0.1'), 'ether'), "timeout": 600})

    # Sign transaction
    signed_tx = web3.eth.account.sign_transaction(call_function, private_key=caller)

    # Send transaction
    send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt) # Optional