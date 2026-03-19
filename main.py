import os
import subprocess
import msvcrt
def wait_for_escape():
    print("\nPress ESC to return to menu.")

    while True:
        key = msvcrt.getch()
        if key == b'\x1b':   # ESC key                         ## CHAT GPT
            clear_screen()
            break
def clear_screen():
    subprocess.run('cls' if os.name == 'nt' else 'clear', shell=True)

from user import User
from accounts.savings import SavingsAccount
from accounts.current import CurrentAccount
from accounts.loan import LoanAccount
from exceptions import (
    FinanceException, 
    InvalidAmountError, 
    InsufficientFundsError, 
    AccountNotFoundError,
    UnauthorizedAccessError
)
from utils import format_currency, generate_report, load_transactions_from_file



def monthly_expense_analytics(user):
    try:
        month = int(input("Enter month (1-12): "))

        if month < 1 or month > 12:
            print("Invalid month.")
            return

        total_income = 0
        total_expense = 0

        for summary in user.get_all_summaries():
            account = user.get_account(summary.account_id)

            transactions = account.get_statement(month)

            for txn in transactions:
                if txn.type == "credit":
                    total_income += txn.amount
                elif txn.type == "debit":
                    total_expense += txn.amount

        savings = total_income - total_expense

        print("\nMonthly Financial Analytics\n")

        print(f"Total Income : {format_currency(total_income)}")
        print(f"Total Expense: {format_currency(total_expense)}")
        print(f"Savings      : {format_currency(savings)}")

    except ValueError:
        print("Invalid input.")  

def print_menu():

    print("Personal Finance Management System\n")
   
    print("1. View all accounts")
    print("2. Create new account")
    print("3. Deposit to account")
    print("4. Withdraw from account")
    print("5. View account statement")
    print("6. Apply monthly updates to all accounts")
    print("7. View full financial report")
    print("8. Monthly Expense Analytics")
    print("9. Set Monthly Budget")
    print("10. Exit")
    
    
    


def view_all_accounts(user):
    summaries = user.get_all_summaries()
    if not summaries:
        print("No accounts found.")
        return
    
  
    print("All Accounts\n")
   
    for summary in summaries:
        account = user.get_account(summary.account_id)
        print(f"ID: {summary.account_id}")
        print(f"Type: {summary.account_type}")
        print(f"Balance: {format_currency(summary.balance)}")
        print(f"Transactions: {summary.total_transactions}")
        if summary.account_type == 'Loan' and hasattr(account, 'loan_summary'):   # chat gpt
            loan_info = account.loan_summary()
            print(f"Principal: {format_currency(loan_info['principal'])}")
            print(f"EMI: {format_currency(loan_info['emi'])}")
            print(f"Months Remaining: {loan_info['months_remaining']}")
            if loan_info.get('repayment_account_id'):
                source_id = loan_info['repayment_account_id']
                try:
                    source_account = user.get_account(source_id)
                    print(f"EMI Source Account: {source_id} ({source_account.get_account_type()})")
                except FinanceException:
                    print(f"EMI Source Account: {source_id} (not found)")
        print()


def deposit_to_account(user,):
    try:
        account_id = input("Enter account ID: ").strip()
        amount = float(input("Enter amount to deposit: "))
      
        
        account = user.get_account(account_id)
        account.deposit(amount)
        print(f"Successfully deposited {format_currency(amount)} to account {account_id}")
        print(f"New balance: {format_currency(account.balance)}")
        print("\nUpdated Transactions:\n")
        for txn in account.get_statement():
            print(txn)
        
    except ValueError:
        print("Error: Invalid input. Please enter a valid amount.")
    except FinanceException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def withdraw_from_account(user, monthly_budget):
    try:
        account_id = input("Enter account ID: ").strip()
        amount = float(input("Enter amount to withdraw: "))
        
        account = user.get_account(account_id)
        account.withdraw(amount)
        print(f"Successfully withdrew {format_currency(amount)} from account {account_id}")
        print(f"New balance: {format_currency(account.balance)}")
        expense = calculate_monthly_expense(user)
        if monthly_budget and expense > monthly_budget:
            print("\n WARNING: Budget limit exceeded!")

        print("\nUpdated Transactions:\n")
        for txn in account.get_statement():
            print(txn)
    except ValueError:
        print("Error: Invalid input. Please enter a valid amount.")
    except FinanceException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def view_statement(user):
    try:
        account_id = input("Enter account ID: ").strip()
        month_input = input("Enter month (1-12) or press Enter to see all transactions: ").strip()
        
        account = user.get_account(account_id)
        month = None
        if month_input:
            month = int(month_input)
            if month < 1 or month > 12:
                print("Error: Month must be between 1 and 12")
                return
        
        transactions = account.get_statement(month)
        if not transactions:
            print("No transactions found.")
            return
        
        
        print(f"Statement for {account_id} (Month: {month if month else 'All'})\n")
        
        for txn in transactions:
            print(f"  {txn}\n")
            print(f'  {repr(txn)}\n')
        
        print(f"Total Transactions: {len(transactions)}")
    except ValueError:
        print("Error: Invalid input.")
    except FinanceException as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")


def apply_monthly_updates(user):
    print("\nApplying monthly updates to all accounts...")
    errors = user.apply_all_monthly_updates()
    
    if errors:
        print(f"Completed with {len(errors)} error(s):")
        for error in errors:
            print(f"  - {error}")
    else:
        print("All monthly updates applied successfully!")
    
    print("\nUpdated Account Balances:")
    for summary in user.get_all_summaries():
        account = user.get_account(summary.account_id)
        print(f"  {summary.account_id}: {format_currency(account.balance)}")


def view_financial_report(user):
    report = generate_report(user)
    
   
    print("Financial Report\n")
  
  
    print(f"User: {report['user']['name']} ({report['user']['user_id']})")
    print(f"Email: {report['user']['email']}")
    print()
    print(f"Total Balance: {format_currency(report['total_balance'])}")
    print(f"Net Worth: {format_currency(report['net_worth'])}")
    print()
    
    print("Account Summaries:\n")
 
    for summary in report['account_summaries']:
        print(f"  {summary['account_id']} ({summary['account_type']}): {format_currency(summary['balance'])}")
    
    print()
   
    print("Top 5 Transactions by Amount:\n")
    
    for i, txn in enumerate(report['top_5_transactions'],0 ):   ## chat gpt
        print(f"  {i}. {txn['description']}: {format_currency(txn['amount'])} ({txn['type']})")
        
        
def create_account(user):
    try:
        print("\nSelect Account Type")
        print("1. Savings Account")
        print("2. Current Account")
        print("3. Loan Account")

        choice = input("Enter choice: ").strip()

        account_id = input("Enter new Account ID: ").strip()

        if choice == '1':
            balance = float(input("Enter initial balance: "))
            rate = float(input("Enter interest rate (%): "))

            account = SavingsAccount(account_id, user.name, balance, interest_rate=rate)

        elif choice == '2':
            balance = float(input("Enter initial balance: "))
            fee = float(input("Enter monthly fee: "))
            overdraft = float(input("Enter overdraft limit: "))

            account = CurrentAccount(account_id, user.name, balance, monthly_fee=fee, overdraft_limit=overdraft)

        elif choice == '3':
            principal = float(input("Enter loan principal: "))
            emi = float(input("Enter EMI amount: "))
            months = int(input("Enter remaining months: "))

            eligible_accounts = [
                summary for summary in user.get_all_summaries()
                if summary.account_type in ('Savings', 'Current')
            ]

            if not eligible_accounts:
                print("Create a Savings or Current account first to link EMI deduction.")
                return

            print("\nSelect account for monthly EMI deduction")
            for index, summary in enumerate(eligible_accounts, 1):
                print(
                    f"{index}. {summary.account_id} ({summary.account_type}) "
                    f"- Balance: {format_currency(summary.balance)}"
                )

            source_choice = input("Enter option number: ").strip()
            if not source_choice.isdigit():
                print("Invalid selection.")
                return

            source_index = int(source_choice)
            if source_index < 1 or source_index > len(eligible_accounts):
                print("Invalid selection.")
                return

            repayment_account_id = eligible_accounts[source_index - 1].account_id

            account = LoanAccount(
                account_id,
                user.name,
                principal=principal,
                emi_amount=emi,
                remaining_months=months,
                repayment_account_id=repayment_account_id
            )

        else:
            print("Invalid account type.")
            return

        user.add_account(account)

        print("\nAccount created successfully!")
        print(f"Account ID: {account_id}")
        print(f"Type: {account.get_account_type()}")
        if account.get_account_type() == 'Loan' and getattr(account, 'repayment_account_id', None):
            print(f"Linked EMI Source: {account.repayment_account_id}")

    except Exception as e:
        print(f"Error: {e}")


def set_budget():
    try:
        budget = float(input("Enter your monthly budget: "))
        print(f"Budget set to {format_currency(budget)}")
        return budget
    except ValueError:
        print("Invalid amount.")
        return 0
    
    
    
    
from datetime import datetime

def calculate_monthly_expense(user):
    current_month = datetime.now().month
    total_expense = 0

    for summary in user.get_all_summaries():
        account = user.get_account(summary.account_id)

        transactions = account.get_statement(current_month)

        for txn in transactions:
            if txn.type == "debit":
                total_expense += txn.amount

    return total_expense

def main(): 
 
    user_dict = {
    "001": {
        "user": User("001", "Axit Dagara", "axit@gmail.com"),
        "password": "1234"
    }
}
    print("Welcome to Personal Finance Management System\n")

    user_id = input("Enter User ID: ")
    password = input("Enter Password: ")

    try:
       if user_id not in user_dict:
        raise AccountNotFoundError("User not found", error_code=1006)

       if password != user_dict[user_id]["password"]:
        raise UnauthorizedAccessError("Invalid password", error_code=1007)

       user = user_dict[user_id]["user"]

       print(f"\nWelcome {user.name} ({user.user_id})")

    except FinanceException as e:
       print(e)
    
       exit()
    monthly_budget = 0

   
    savings = SavingsAccount("SAV001", "Axit Dagara", 50000, interest_rate=4.5)
    current = CurrentAccount("CUR001", "Axit Dagara", 30000, monthly_fee=200, overdraft_limit=5000)
    loan = LoanAccount(
        "LOAN001",
        "Axit Dagara",
        principal=100000,
        emi_amount=5000,
        remaining_months=20,
        repayment_account_id="CUR001"
    )
    
    user.add_account(savings)
    user.add_account(current)
    user.add_account(loan)
    
    print("Welcome to Personal Finance Management System\n")
    print(f"User: {user.name} ({user.user_id})\n")
    print(f"Accounts created: {len(user.get_all_summaries())}\n")
    
    while True:
        
        try:
            clear_screen()  
            print_menu()
            choice = input("Enter your choice (1-10): \n").strip()
            
            if choice == '1':
                view_all_accounts(user)
                wait_for_escape()
            elif choice == '3':
            
                deposit_to_account(user, )
                wait_for_escape()
            elif choice == '2':
                create_account(user)
                wait_for_escape()       
            elif choice == '4':
                withdraw_from_account(user, monthly_budget)
                wait_for_escape()
            elif choice == '5':
                view_statement(user)
                wait_for_escape()
            elif choice == '6':
                apply_monthly_updates(user)
                wait_for_escape()
            elif choice == '7':
                view_financial_report(user)
                wait_for_escape()
            elif choice == '8':
                monthly_expense_analytics(user)
                wait_for_escape()
            elif choice == '9':
                monthly_budget = set_budget()
                wait_for_escape()    
            elif choice == '10':
                 
                print("Thank you ")
                ## want to clear screen after 5s and exit
                

               ## clear_screen()                
               
                break
            else:
                print("Invalid choice. Please enter a number between 1 and 10.")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"Unexpected error: {e}")
            


if __name__ == "__main__":
    main()
