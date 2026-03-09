from exceptions import AccountNotFoundError


class User:
    def __init__(self, user_id, name, email):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.__accounts = {}

    def add_account(self, account):
        if account.account_id in self.__accounts:
            raise ValueError(f"Account {account.account_id} already exists")
        self.__accounts[account.account_id] = account

    def get_account(self, account_id):
        if account_id not in self.__accounts:
            raise AccountNotFoundError(f"Account {account_id} not found", error_code=1006)
        return self.__accounts[account_id]

    def remove_account(self, account_id):
        if account_id in self.__accounts:
            del self.__accounts[account_id]

    def total_balance(self):
        total = 0
        for account in self.__accounts.values():
            if account.get_account_type() != 'Loan':
                total += account.balance
        return total

    def net_worth(self):
        total_balance = self.total_balance()
        loan_debt = 0
        for account in self.__accounts.values():
            if account.get_account_type() == 'Loan':
                loan_debt += abs(account.balance)
        return total_balance - loan_debt

    def get_all_summaries(self):
        return [account.get_summary() for account in self.__accounts.values()]

    def apply_all_monthly_updates(self):  ## chat gpt 
        errors = []
        for account in self.__accounts.values():
            try:
                account.apply_monthly_update()
            except Exception as e:
                errors.append(e)
        return errors
    




    def __str__(self):
        return f"User({self.user_id}, {self.name}, {len(self.__accounts)} accounts)"
