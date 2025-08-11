#!/usr/bin/env python3

from internet import MiniInternetTestCase
from ethereum import EthereumPOATestCase, EthereumPOSTestCase, EthereumPOWTestCase
from options import SEEDEmuOptionSystemTestCase
from ethUtility import EthUtilityPOATestCase
import argparse
import unittest
import os

parser = argparse.ArgumentParser()
parser.add_argument("platform", nargs='?', default="amd")
parser.add_argument("--ci", action='store_true', help="Run POS & MiniInternet only")
args = parser.parse_args()

# Set an environment variable
os.environ['platform'] = args.platform

test_case_list = [
    MiniInternetTestCase,
    EthereumPOATestCase,
    EthereumPOSTestCase,
    EthereumPOWTestCase,
    EthUtilityPOATestCase,
    SEEDEmuOptionSystemTestCase,
]

if args.ci:
    test_case_list = [
        MiniInternetTestCase,
        EthereumPOSTestCase,
    ]

for test_case in test_case_list:
    test_suite = test_case.get_test_suite()
    res = unittest.TextTestRunner(verbosity=2).run(test_suite)
    test_case.printLog("==============================")
    test_case.printLog("{} Test Ends".format(test_case.__name__))
    test_case.printLog("==============================")

    num, errs, fails = res.testsRun, len(res.errors), len(res.failures)
    test_case.printLog("score: %d of %d (%d errors, %d failures)" % (num - (errs+fails), num, errs, fails))
