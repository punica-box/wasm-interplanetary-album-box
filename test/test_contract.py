import binascii
import time
import unittest
from os import path

from ontology.contract.wasm.params_builder import WasmParamsBuilder
from ontology.crypto.ecies import ECIES
from ontology.sdk import Ontology
from ontology.contract.wasm.invoke_function import WasmInvokeFunction
from ontology.utils.event import Event


class TestSmartContract(unittest.TestCase):
    def setUp(self):
        self.sdk = Ontology()
        self.sdk.rpc.connect_to_test_net()
        test_dir = path.dirname(__file__)
        wallet_path = path.join(path.dirname(test_dir), 'wallet', 'wallet.json')
        self.sdk.wallet_manager.open_wallet(wallet_path)
        self.gas_price = 500
        self.gas_limit = 25000000
        self.contract_address = '166c697011bf3d028287849cb20d96eafd43943f'
        self.ont_id = 'did:ont:AHBB3LQNpqXjCLathy7vTNgmQ1cGSj8S9Z'
        self.ont_id_ctrl_address = 'AHBB3LQNpqXjCLathy7vTNgmQ1cGSj8S9Z'
        self.ont_id_ctrl_acct = self.sdk.wallet_manager.get_control_account_by_b58_address(self.ont_id,
                                                                                           self.ont_id_ctrl_address,
                                                                                           'password')

    def test_put_one_item(self):
        ipfs_address = 'QmVwRs3tMPwi8vHqZXfxdgbcJXdmrgViGiy77o9ohef6ss'
        ext = '.jpg'
        aes_iv, encode_g_tilde, encrypted_ipfs_address = ECIES.encrypt_with_cbc_mode(ipfs_address.encode('ascii'),
                                                                                     self.ont_id_ctrl_acct.get_public_key_bytes())
        put_one_item_func = WasmInvokeFunction('put_one_item')
        put_one_item_func.set_params_value(self.ont_id_ctrl_acct.get_address(), ipfs_address, ext, aes_iv.hex(),
                                           encode_g_tilde.hex())
        tx = self.sdk.wasm_vm.make_invoke_transaction(self.contract_address, put_one_item_func,
                                                      self.ont_id_ctrl_acct.get_address(), self.gas_price,
                                                      self.gas_limit)
        tx.sign_transaction(self.ont_id_ctrl_acct)
        tx_hash = self.sdk.rpc.send_raw_transaction(tx)
        self.assertEqual(64, len(tx_hash))
        time.sleep(12)
        event = self.sdk.rpc.get_contract_event_by_tx_hash(tx_hash)
        states = Event.get_event_from_event_list_by_contract_address(event['Notify'], self.contract_address)
        self.assertEqual(1, len(states))

    def test_get_item_list(self):
        get_item_list_func = WasmInvokeFunction('get_item_list')
        get_item_list_func.set_params_value(self.ont_id_ctrl_acct.get_address())
        tx = self.sdk.wasm_vm.make_invoke_transaction(self.contract_address, get_item_list_func,
                                                      self.ont_id_ctrl_acct.get_address(), self.gas_price,
                                                      self.gas_limit)
        tx.sign_transaction(self.ont_id_ctrl_acct)
        result = self.sdk.rpc.send_raw_transaction_pre_exec(tx).get('Result')
        builder = WasmParamsBuilder(bytes.fromhex(result))
        struct_len = builder.read_var_uint()
        for _ in range(struct_len):
            print(builder.pop_str())
            print(builder.pop_str())
            print(builder.pop_str())
            print(builder.pop_str())


if __name__ == '__main__':
    unittest.main()
