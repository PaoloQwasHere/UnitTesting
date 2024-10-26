import unittest

#from UnitTesting.tests.test_bank_account import BankAccountTest
from tests.test_bank_account import BankAccountTest

def bank_account_suite():
    suite = unittest.TestSuite()
    suite.addTest(BankAccountTest("test_deposit"))
    suite.addTest(BankAccountTest("test_withdraw"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(bank_account_suite())