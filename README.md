# Personal Finance Management System

A command-line Python application to manage personal finances with support for Savings, Current, and Loan accounts.

## Features

- User login with basic authentication
- Create and manage multiple account types:
  - Savings Account
  - Current Account
  - Loan Account (with linked EMI deduction account)
- Deposit and withdraw funds
- View account statements (full or month-wise)
- Apply monthly account updates
- Generate full financial report
- Monthly expense analytics
- Set monthly budget and get overspending warning

## Tech Stack

- Python 3
- Console-based UI
- Modular account architecture (`accounts/` package)

## Project Structure

- `main.py` — entry point and menu-driven workflow
- `user.py` — user and account registry logic
- `accounts/` — account implementations (`savings`, `current`, `loan`)
- `exceptions.py` — custom finance-related exceptions
- `utils.py` — reporting, formatting, and helper utilities

## Getting Started (Windows)

1. Open terminal in project folder:
   - `e:\finance_system`
2. (Optional) Create and activate virtual environment:
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1`
3. Install dependencies (if `requirements.txt` exists):
   - `pip install -r requirements.txt`
4. Run the app:
   - `python main.py`

## Demo Login

Use the default credentials currently defined in `main.py`:

- **User ID:** `001`
- **Password:** `1234`

## Menu Options

1. View all accounts  
2. Create new account  
3. Deposit to account  
4. Withdraw from account  
5. View account statement  
6. Apply monthly updates to all accounts  
7. View full financial report  
8. Monthly Expense Analytics  
9. Set Monthly Budget  
10. Exit  

## Notes

- The app currently seeds sample accounts on startup.
- ESC key behavior is implemented using `msvcrt` (Windows-friendly).
- Screen clearing uses `cls` on Windows.