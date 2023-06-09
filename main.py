import config
from web3 import Web3
from decimal import Decimal
import ctypes
from config import *

RPC = [
    {'chain': 'Ethereum     ', 'chain_id': 1, 'rpc': 'https://rpc.ankr.com/eth'},
    {'chain': 'Goerli     ', 'chain_id': 5, 'rpc': 'https://goerli.blockpi.network/v1/rpc/public'},
    {'chain': 'Optimism Goerli Testnet     ', 'chain_id': 420, 'rpc': 'https://optimism-goerli.public.blastapi.io'},
    {'chain': 'Arbitrum One ', 'chain_id': 421613, 'rpc': 'https://goerli-rollup.arbitrum.io/rpc'},
]
# ABI = '[{"inputs":[{"internalType":"address","name":"_weth","type":"address"},{"internalType":"address","name":"_oft","type":"address"},{"internalType":"address","name":"_swapRouter","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[],"name":"oft","outputs":[{"internalType":"contract IOFTCore","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"poolFee","outputs":[{"internalType":"uint24","name":"","type":"uint24"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"to","type":"address"},{"internalType":"address payable","name":"refundAddress","type":"address"},{"internalType":"address","name":"zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"adapterParams","type":"bytes"}],"name":"swapAndBridge","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"swapRouter","outputs":[{"internalType":"contract ISwapRouter","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"weth","outputs":[{"internalType":"contract IWETH","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'
ABI = '[{"inputs":[{"internalType":"address","name":"_oft","type":"address"},{"internalType":"address","name":"_nativeOft","type":"address"},{"internalType":"address","name":"_uniswapRouter","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"to","type":"address"},{"internalType":"address payable","name":"refundAddress","type":"address"},{"internalType":"address","name":"zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"adapterParams","type":"bytes"}],"name":"bridge","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"nativeOft","outputs":[{"internalType":"contract INativeOFT","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"oft","outputs":[{"internalType":"contract IOFTCore","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"uint256","name":"amountIn","type":"uint256"},{"internalType":"uint256","name":"amountOutMin","type":"uint256"},{"internalType":"uint16","name":"dstChainId","type":"uint16"},{"internalType":"address","name":"to","type":"address"},{"internalType":"address payable","name":"refundAddress","type":"address"},{"internalType":"address","name":"zroPaymentAddress","type":"address"},{"internalType":"bytes","name":"adapterParams","type":"bytes"}],"name":"swapAndBridge","outputs":[],"stateMutability":"payable","type":"function"},{"inputs":[],"name":"uniswapRouter","outputs":[{"internalType":"contract IUniswapV2Router02","name":"","type":"address"}],"stateMutability":"view","type":"function"}]'
contract_address = '0x0A9f824C05A74F577A536A8A0c673183a872Dff4'
zroPaymentAddress = '0x0000000000000000000000000000000000000000'

# private key


def check_balance(address, chain_number):
    web3 = Web3(Web3.HTTPProvider(RPC[chain_number]['rpc']))
    balance = web3.eth.get_balance(web3.to_checksum_address(address))

    print(balance)


if __name__ == '__main__':
    web3 = Web3(Web3.HTTPProvider('https://goerli.blockpi.network/v1/rpc/public'))
    # web3 = Web3(Web3.HTTPProvider('https://optimism-goerli.public.blastapi.io'))

    # Call your function
    address = web3.eth.account.from_key(config.key).address
    eth_account = web3.eth.account.from_key(config.key)

    contract_instance = web3.eth.contract(address=contract_address, abi=ABI)
    check_balance(address, 1)
    check_balance(address, 2)
    check_balance(address, 3)

    tx = {
        "from": address,
        "value": web3.to_wei(Decimal('1'), 'ether'),
        "nonce": web3.eth.get_transaction_count(address),
        "chainId": 5,
        "gasPrice": int(web3.eth.gas_price * 1.1)
    }
    try:
        tx['gas'] = web3.eth.estimate_gas(tx)
    except:
        print('e')

    amountIn = web3.to_wei(Decimal('1'), 'ether')
    amountOutMin = web3.to_wei(Decimal('0.01'), 'ether')
    dstChainId = ctypes.c_uint16(110).value
    adapterParams = bytes('20000', 'utf-8')
    print(amountIn)
    print(amountOutMin)
    # call_function = contract_instance.functions.swapAndBridge(amountIn, amountIn, dstChainId, address, address, zroPaymentAddress, b'').build_transaction(tx)
    call_function = contract_instance.functions.bridge(amountIn, dstChainId, address, address, zroPaymentAddress, b'').build_transaction(tx)

         # {"chainId": 5, "from": address, "nonce": 5, "gasLimit":  web3.eth.gas_price, "value": web3.to_wei(Decimal('0.01'), 'ether'), "timeout": 600})


    # Sign transaction
    signed_tx = web3.eth.account.sign_transaction(call_function, private_key=config.key)

    # Send transaction
    send_tx = web3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Wait for transaction receipt
    tx_receipt = web3.eth.wait_for_transaction_receipt(send_tx)
    print(tx_receipt)