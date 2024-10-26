import unittest, os
from unittest.mock import patch
from datetime import datetime
from src.exceptions import InsufficientFundError, WithdrawralTimeRestrictionError, DayRestrictionError
from src.bank_account import BankAccount

class BankAccountTest(unittest.TestCase):
    
    def setUp(self) -> None:
        self.account = BankAccount(balance = 1000, log_file = "transaction_log.txt")
        self.target_account = BankAccount(balance=500)

    def tearDown(self) -> None:
        if os.path.exists(self.account.log_file):
            os.remove(self.account.log_file)

    def _count_lines(self, filename):
        with open(filename, "r") as f:
            return len(f.readlines())

    def test_deposit(self):
        new_balance = self.account.deposit(500)
        self.assertEqual(new_balance, 1500, "El balance no es igual")
    
    @patch("src.bank_account.datetime")
    def test_withdraw(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 23, 10)
        new_balance = self.account.withdraw(500)
        self.assertEqual(new_balance, 500, "El balance no es igual")
    
    def test_transfer(self):
        self.account.transfer(200, self.target_account)
        self.assertEqual(self.account.get_balance(), 800)
        self.assertEqual(self.target_account.get_balance(), 700)


    def test_get_balance(self):
        self.assertEqual(self.account.get_balance(), 1000)

    def test_transaction_log(self):
        self.account.deposit(500)
        self.assertTrue(os.path.exists("transaction_log.txt"))

    def test_count_transactions(self):
        assert self._count_lines(self.account.log_file) == 1
        self.account.deposit(500)
        assert self._count_lines(self.account.log_file) == 2  

    @patch("src.bank_account.datetime")
    def test_withdraw_insufficient_funds(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 23, 10)
        with self.assertRaises(InsufficientFundError):
            self.account.withdraw(1500) 
    
    @patch("src.bank_account.datetime")
    def test_transfer_insufficient_funds(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 23, 10)
        with self.assertRaises(ValueError):
            self.account.transfer(2000, self.target_account)

    @patch("src.bank_account.datetime")
    def test_withdraw_during_bussines_hours(self,mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 23, 10)
        new_balance = self.account.withdraw(100)
        self.assertEqual(new_balance, 900)        

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_before_business_hours(self,mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 23, 7) 
        with self.assertRaises(WithdrawralTimeRestrictionError):
            self.account.withdraw(100)

    @patch("src.bank_account.datetime")
    def test_withdraw_disallow_after_business_hours(self,mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 23, 20)
        with self.assertRaises(WithdrawralTimeRestrictionError):
            self.account.withdraw(100)
    
    @patch("src.bank_account.datetime")
    def test_withdraw_on_saturday(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 28, 10)  
        with self.assertRaises(DayRestrictionError):
            self.account.withdraw(100)

    @patch("src.bank_account.datetime")
    def test_withdraw_on_sunday(self, mock_datetime):
        mock_datetime.now.return_value = datetime(2023, 10, 29, 10)  
        with self.assertRaises(DayRestrictionError):
            self.account.withdraw(100)

    @patch("src.bank_account.datetime")
    def test_withdraw_on_weekday(self, mock_datetime):     
        mock_datetime.now.return_value = datetime(2023, 10, 23, 10)  
        self.account.withdraw(100)
        self.assertEqual(self.account.get_balance(), 900)

    def test_deposit_many_ammounts(self):
        test_cases = [
            {"ammount":  100, "expected": 1100},
            {"ammount": 3000, "expected": 4000},
            {"ammount": 4500, "expected": 5500},

        ]

        for case in test_cases:
            with self.subTest(case = case):
                self.account = BankAccount(balance=1000, log_file="transactions.txt")
                new_balance = self.account.deposit(case["ammount"])
                self.assertEqual(new_balance, case["expected"])