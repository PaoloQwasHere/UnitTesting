from datetime import datetime
from src.exceptions import InsufficientFundError, WithdrawralTimeRestrictionError, DayRestrictionError

class BankAccount:
    def __init__(self, balance = 0, log_file = None):
        self.balance = balance
        self.log_file = log_file
        self._log_transaction("Cuenta creada")

    def _log_transaction(self,message):
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(f"{message}\n")

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self._log_transaction(f"Cantidad depositada {amount}. Nuevo balance: {self.balance}")
        return self.balance
    
    def withdraw(self, amount):
        now = datetime.now()
        if now.hour < 8 or now.hour > 17:
            raise WithdrawralTimeRestrictionError("Withdrawal are only allowed from 8am to 5pm")

        now = datetime.now()
        if now.weekday() >= 5:
            raise DayRestrictionError("Withdrawals are not allowed on weekends")

        if amount > self.balance:
            raise InsufficientFundError(
                f"Withdrawal of {amount} exceeds balance {self.balance}"
            )

        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            self._log_transaction(f"Retiro {amount}. Nuevo balance: {self.balance}")
        return self.balance
    
    def transfer(self, amount, target_account):
        if amount > 0 and self.balance >= amount:
            self.balance -= amount
            target_account.deposit(amount)
        else:
            self._log_transaction(f"Transferencia fallida por monto {amount}. Saldo disponible {self.balance}")
            raise ValueError("No tienes saldo suficiente para transferir")
        return self.balance
        

    def get_balance(self):
        self._log_transaction(f"Revision de balance. Balance actual {self.balance}")
        return self.balance
