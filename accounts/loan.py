from account import Account
from transaction import Transaction
from exceptions import UnauthorizedAccessError


class LoanAccount(Account):
    def __init__(self, account_id, account_holder, principal, emi_amount, remaining_months, repayment_account_id=None):
        super().__init__(account_id, account_holder, initial_balance=0)
        self.principal = principal
        self.emi_amount = emi_amount
        self.remaining_months = remaining_months
        self.repayment_account_id = repayment_account_id
        self._Account__balance = -principal  

    def deposit(self, amount):
        raise UnauthorizedAccessError("Loan accounts do not accept deposits", error_code=1005)

    def apply_monthly_update(self):
        if self.remaining_months > 0:
            self._Account__balance += self.emi_amount  
            self.remaining_months -= 1
            transaction = Transaction.create(self.emi_amount, 'debit', 'EMI payment', tags=['emi'])
            self.history.append(transaction)

    def get_account_type(self) -> str:
        return 'Loan'

    def loan_summary(self):
        return {
            'principal': self.principal,
            'emi': self.emi_amount,
            'months_remaining': self.remaining_months,
            'total_remaining': max(0, abs(self.balance)),
            'repayment_account_id': self.repayment_account_id
        }
