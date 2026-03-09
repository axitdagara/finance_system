from account import Account
from transaction import Transaction
from exceptions import InsufficientFundsError


class SavingsAccount(Account):
    def __init__(self, account_id, account_holder, initial_balance=0, interest_rate=4.5):
        super().__init__(account_id, account_holder, initial_balance)
        self.interest_rate = interest_rate

    def apply_monthly_update(self):
        interest_amount = self.balance * self.interest_rate / 12 / 100
        self._Account__balance += interest_amount
        transaction = Transaction.create(interest_amount, 'credit', 'Monthly interest', tags=['interest'])
        self.history.append(transaction)

    def withdraw(self, amount):
        self.validate_amount(amount)
        minimum_balance = 1000
        if self.balance - amount < minimum_balance:
            raise InsufficientFundsError(f"Minimum balance of Rs. {minimum_balance} must be maintained", error_code=1003)
        return super().withdraw(amount)

    def get_account_type(self) -> str:
        return 'Savings'
