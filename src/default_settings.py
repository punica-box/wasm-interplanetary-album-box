import binascii
import os

import json

from ontology.contract.neo.abi.abi_info import AbiInfo
from ontology.sdk import Ontology
from ontology.wallet.wallet_manager import WalletManager

ROOT_FOLDER = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WALLET_PATH = os.path.join(ROOT_FOLDER, 'wallet', 'wallet.json')
STATIC_FOLDER = os.path.join(ROOT_FOLDER, 'src', 'static')
CONTRACTS_FOLDER = os.path.join(ROOT_FOLDER, 'contracts')
TEMPLATE_FOLDER = os.path.join(STATIC_FOLDER, 'templates')
ASSETS_FOLDER = os.path.join(STATIC_FOLDER, 'assets')
try:
    os.mkdir(ASSETS_FOLDER)
except FileExistsError:
    pass
ALBUM_FOLDER = os.path.join(STATIC_FOLDER, 'album')
try:
    os.mkdir(ALBUM_FOLDER)
except FileExistsError:
    pass
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'bmp'}
IPFS_HOST = '127.0.0.1'
IPFS_PORT = 5001
GAS_LIMIT = 30000000
GAS_PRICE = 500
ONT_RPC_ADDRESS = 'http://polaris3.ont.io:20336'
CONTRACT_ADDRESS_HEX = '166c697011bf3d028287849cb20d96eafd43943f'
ONTOLOGY = Ontology()
ONTOLOGY.rpc.set_address(ONT_RPC_ADDRESS)
WALLET_MANAGER = WalletManager()
WALLET_MANAGER.open_wallet(WALLET_PATH)
