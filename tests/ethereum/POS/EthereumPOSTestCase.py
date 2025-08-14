#!/usr/bin/env python3
# encoding: utf-8

import time
import unittest as ut
from tests.ethereum.POS.SEEDBlockchain import Wallet
from seedemu import *
import time
import docker
from tests import SeedEmuTestCase

class EthereumPOSTestCase(SeedEmuTestCase):
    @classmethod
    def setUpClass(cls) -> None:
        super().setUpClass()
        
        cls.wallet1 = Wallet(chain_id=1337)
        for name in ['Alice', 'Bob', 'Charlie', 'David', 'Eve']:
            cls.wallet1.createAccount(name)
        
        cls.wallet2 = Wallet(chain_id=1337)
        cls.wallet3 = Wallet(chain_id=1337)

        cls.result = True
        return
        
    
    def test_pos_geth_connection(self):
        url_1 = 'http://10.151.0.71:8545'
        url_2 = 'http://10.152.0.71:8545'
        url_3 = 'http://10.153.0.71:8545'

        i = 1
        current_time = time.time()
        while True:
            self.printLog("\n----------Trial {}----------".format(i))
            if time.time() - current_time > 600:
                self.printLog("TimeExhausted: 600 sec")
                break
            try:
                self.wallet1.connectToBlockchain(url_1, isPOA=False)
                self.printLog("Connection Succeed: ", url_1)
                self.wallet2.connectToBlockchain(url_2, isPOA=False)
                self.printLog("Connection Succeed: ", url_2)
                self.wallet3.connectToBlockchain(url_3, isPOA=False)
                self.printLog("Connection Succeed: ", url_3)
                break
            except Exception as e:
                self.printLog(e)
                time.sleep(20)
                i += 1
        self.assertTrue(self.wallet1._web3.isConnected())
        self.assertTrue(self.wallet2._web3.isConnected())
        self.assertTrue(self.wallet3._web3.isConnected())


    def test_pos_send_transaction(self):
        recipient = self.wallet1.getAccountAddressByName('Bob')
        txhash = self.wallet1.sendTransaction(recipient, 0.1, sender_name='David', wait=True, verbose=False)
        self.assertTrue(self.wallet1.getTransactionReceipt(txhash)["status"], 1)

    @classmethod
    def get_test_suite(cls):
        test_suite = ut.TestSuite()
        test_suite.addTest(cls('test_pos_geth_connection'))
        test_suite.addTest(cls('test_pos_send_transaction'))
        return test_suite
if __name__ == "__main__":
        test_suite = EthereumPOSTestCase.get_test_suite()
        res = ut.TextTestRunner(verbosity=2).run(test_suite)
    
        EthereumPOSTestCase.printLog("----------Test %d--------=")
        num, errs, fails = res.testsRun, len(res.errors), len(res.failures)
        EthereumPOSTestCase.printLog("score: %d of %d (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))
        
