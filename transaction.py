from datetime import datetime
import csv  

class Transaction:
    _counter = 0
    
    filepath = "data/sample_transactions.csv" 

    def __init__(self, transaction_id, amount, txn_type, description, timestamp, tags=None):
        self.transaction_id = transaction_id
        self.amount = amount
        self.type = txn_type
        self.description = description
        self.timestamp = timestamp
        self.tags = set(tags or [])
        
        self.add_record_to_csv(Transaction.filepath)   # CHAT GPT

    
    @staticmethod
    def from_string(data: str):
        amount, t_type, desc, tags = data.split(",")

        amount = float(amount.strip())  
        t_type = t_type.strip()
        desc = desc.strip()
        tags_set = set(tags.strip().split("|"))

        Transaction._validate_transaction_data(amount, t_type)

        return Transaction.create(amount, t_type, desc, tags_set)    ## CHAT GPT
    # @staticmethod
    # def from_string(data: str):
    #     amount, t_type, desc, tags = data.split(",")

    #     tags_set = set(tags.split("|"))

    #     return Transaction.create(float(amount), t_type, desc, tags_set)
    # # def from_string(data: str):
               
    #    if not data.strip():
    #       return []
    #    return [t.strip() for t in data.split("|") if t.strip()]    #chatgpt

    # @staticmethod
    # def _validate_transaction_data(amount: float, txn_type: str) -> None:
              
    #             if amount <= 0:
    #                 raise ValueError("Amount must be positive")
    #             if txn_type not in ("debit", "credit"):
    #                 raise ValueError("Type must be 'debit' or 'credit'")
    @staticmethod
    def _validate_transaction_data(amount: float, txn_type: str) -> None:
        if amount <= 0:
               raise ValueError("Amount must be positive")

        if txn_type.lower() not in ("debit", "credit"):  
               raise ValueError("Type must be 'debit' or 'credit'")

    @classmethod
    def create(cls, amount, txn_type, description, tags=None) -> "Transaction":
        cls._counter += 1
        transaction_id = f"T{cls._counter:02d}"
        timestamp = datetime.now()
        return cls(transaction_id, amount, txn_type, description, timestamp, tags=tags)

    def __str__(self):
        return f"[{self.transaction_id}] {self.type.upper()} Rs. - {self.amount} - {self.description}"

    def __repr__(self):
        return (
            f"Transaction(transaction_id={self.transaction_id}, "
            f"amount={self.amount}, type={self.type}, "
            f"description={self.description}, timestamp={self.timestamp}, "
            f"tags={sorted(self.tags)})"
        )
    
    def to_dict(self):
        return {
            "transaction_id": self.transaction_id,
            "amount": self.amount,
            "type": self.type,
            "description": self.description,
            "timestamp": self.timestamp.isoformat(), ##isoformat() chat gpt
            "tags": sorted(self.tags),
        }
    def add_record_to_csv(self, filename):
        with open(filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.amount,
                self.type,
                self.description,
                " | ".join(sorted(self.tags))
            ])  
        
