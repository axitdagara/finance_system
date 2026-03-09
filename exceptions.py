class FinanceException(Exception):
    def __init__(self, message, error_code=None):
        super().__init__(message)
        self.message = message
        self.error_code = error_code

    def __str__(self):
        if self.error_code is not None:
            return f"[Code {self.error_code}] {self.message}"
        return self.message

class InsufficientFundsError(FinanceException):

    pass

class InvalidAmountError(FinanceException):
    
    pass

class AccountNotFoundError(FinanceException):
    
    pass

class UnauthorizedAccessError(FinanceException):
    
    pass
