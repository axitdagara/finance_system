from abc import ABC, abstractmethod
from collections import namedtuple
from exceptions import InvalidAmountError, InsufficientFundsError
from transaction import Transaction
from dataclasses import dataclass

AccountSummary = namedtuple("AccountSummary",
                            ["account_id", "account_type", "balance", "total_transactions"])  ## chat gpt 


class Account(ABC):
    _total_accounts = 0
    
    def __init__(self, account_id, account_holder, initial_balance=0.0):
        self.account_id = account_id
        self.account_holder = account_holder
        self.__balance = initial_balance
        self.history = []
        Account._total_accounts += 1
        if initial_balance > 0:
            transaction = Transaction.create(initial_balance, 'credit', 'Initial deposit', tags=['initial'])

            self.history.append(transaction)


    @property
    def balance(self):
        return self.__balance
    
    @abstractmethod
    def apply_monthly_update(self):
        pass

    @abstractmethod
    def get_account_type(self) -> str:
        pass

    @staticmethod
    def validate_amount(amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise InvalidAmountError("Amount must be a positive number", error_code=1002)

    def deposit(self, amount):
        self.validate_amount(amount)
        self.__balance += amount
        transaction = Transaction.create(amount, 'credit', 'Deposit', tags=['deposit'])
        self.history.append(transaction)
        return transaction

    def withdraw(self, amount):
        self.validate_amount(amount)
        if self.__balance < amount:
            raise InsufficientFundsError("Insufficient balance", error_code=1001)
        self.__balance -= amount
        transaction = Transaction.create(amount, 'debit', 'Withdrawal', tags=['withdrawal'])
        self.history.append(transaction)
        return transaction

    def get_statement(self, month=None):
        return self.history if month is None else [txn for txn in self.history if txn.timestamp.month == month]  ## chat gpt

    
    def get_summary(self):
        return AccountSummary(
        account_id=self.account_id,
        account_type=self.get_account_type(),
        balance=self.balance,
        total_transactions=len(self.history)
    )
    
    @staticmethod
    def validate_amount(amount):
        if not isinstance(amount, (int, float)) or amount <= 0:
            raise InvalidAmountError("Amount must be a positive number", error_code=1002)


    def __str__(self):
        return f"Account({self.account_id}, {self.get_account_type()}, Balance: {self.balance})"

    def __eq__(self, other):
        if not isinstance(other, Account):
            return False
        return self.account_id == other.account_id
