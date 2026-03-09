from account import Account
from transaction import Transaction
from exceptions import InsufficientFundsError


class CurrentAccount(Account):
    def __init__(self, account_id, account_holder, initial_balance=0, monthly_fee=200, overdraft_limit=5000):
        super().__init__(account_id, account_holder, initial_balance)
        self.monthly_fee = monthly_fee
        self.overdraft_limit = overdraft_limit

    def apply_monthly_update(self):
        self._Account__balance -= self.monthly_fee
        transaction = Transaction.create(self.monthly_fee, 'debit', 'Monthly fee', tags=['fee'])
        self.history.append(transaction)

    def withdraw(self, amount):
        self.validate_amount(amount)
        available_balance = self.balance + self.overdraft_limit
        if available_balance < amount:
            raise InsufficientFundsError("Insufficient balance including overdraft limit", error_code=1004)
        self._Account__balance -= amount
        transaction = Transaction.create(amount, 'debit', 'Withdrawal', tags=['withdrawal'])
        self.history.append(transaction)
        return transaction

    def get_account_type(self) -> str:
        return 'Current'
