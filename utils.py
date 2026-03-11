import csv
from transaction import Transaction


def load_transactions_from_file(filepath: str) -> list:
    transactions = []

    try:
        with open(filepath, "r") as file:
            reader = csv.reader(file) # CHAT GPT

            for row in reader:
                try:
                    if not row:
                        continue

                    data = ",".join(row)
                    transaction = Transaction.from_string(data)
                    transactions.append(transaction)

                except Exception as e:
                    print(f"Invalid row skipped: {row} -> {e}")

    except FileNotFoundError:
        print("CSV file not found.")

    return transactions


def filter_transactions(transactions, **kwargs):
    result = transactions
    

    if 'type' in kwargs:
        result = [t for t in result if t.type == kwargs['type']]

    if 'min_amount' in kwargs:
        result = [t for t in result if t.amount >= kwargs['min_amount']]

    if 'max_amount' in kwargs:
        result = [t for t in result if t.amount <= kwargs['max_amount']]

    if 'tag' in kwargs:
        result = [t for t in result if kwargs['tag'] in t.tags]

    if 'description' in kwargs:
        result = [t for t in result if kwargs['description'].lower() in t.description.lower()]

    return result

# filtered = filter_transactions(transactions, type='debit', min_amount=1000, tag='withdrawal')


def generate_report(user):
    report = {
        'user': {
            'user_id': user.user_id,
            'name': user.name,
            'email': user.email
        },
        'total_balance': user.total_balance(),
        'net_worth': user.net_worth(),
        'account_summaries': [summary._asdict() for summary in user.get_all_summaries()],
        'top_5_transactions': []
    }

    all_transactions = []

    for summary in user.get_all_summaries():    ## chat gpt
        account = user.get_account(summary.account_id)
        all_transactions.extend(account.history)

    top_5 = sorted(all_transactions, key=lambda t: t.amount, reverse=True)[:5]

    report['top_5_transactions'] = [t.to_dict() for t in top_5]

    return report


def format_currency(amount):
    if amount < 0:
        return f"-Rs. {abs(amount):,.2f}"
    return f"Rs. {amount:,.2f}"